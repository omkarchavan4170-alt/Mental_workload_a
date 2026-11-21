import os
import glob
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
import pandas as pd

from sklearn.model_selection import LeaveOneGroupOut
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier

# Set random seeds for reproducibility
np.random.seed(42)
torch.manual_seed(42)

# -------------------------------------------------------------
# 1. OPTIMIZED DEEP LEARNING ARCHITECTURE (True Sequential 1D-CNN)
# -------------------------------------------------------------
class WorkloadSequential1DCNN(nn.Module):
    def __init__(self, input_features, sequence_length=4):
        super(WorkloadSequential1DCNN, self).__init__()
        # Input shape expected: (Batch, Features, Sequence_Length)
        self.conv_block = nn.Sequential(
            nn.Conv1d(in_channels=input_features, out_channels=64, kernel_size=2, padding=1),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Conv1d(64, 32, kernel_size=2, padding=1),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            nn.AdaptiveAvgPool1d(1)
        )
        self.fc_block = nn.Sequential(
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Dropout(0.4),
            nn.Linear(16, 1),
            nn.Sigmoid()
        )
        
    def forward(self, x):
        # x shape: (Batch, Sequence_Length, Features) -> swap to (Batch, Features, Sequence_Length)
        x = x.transpose(1, 2)
        x = self.conv_block(x)
        x = x.squeeze(-1)
        return self.fc_block(x)

# -------------------------------------------------------------
# 2. DATASET PARSER WITH TIMESTEP SEGMENTATION
# -------------------------------------------------------------
def load_all_wave_features(feature_dir="./features/"):
    X, y, groups = [], [], []
    
    file_paths = glob.glob(os.path.join(feature_dir, "COH_sub*.csv"))
    if not file_paths:
        raise FileNotFoundError("No processed feature CSV files found in ./features/")
        
    for path in file_paths:
        filename = os.path.basename(path)
        parts = filename.replace(".csv", "").split("_")
        
        sub_id = int(parts[1].replace("sub", ""))
        label = 1 if parts[2] == "hi" else 0
        
        df = pd.read_csv(path, index_col=0)
        X.append(df.values)
        y.append(np.full(df.shape[0], label))
        groups.append(np.full(df.shape[0], sub_id))
        
    return np.vstack(X), np.concatenate(y), np.concatenate(groups)

# -------------------------------------------------------------
# 3. HIGH-PERFORMANCE SEQUENTIAL TRANSFORMATION
# -------------------------------------------------------------
def create_sequences(X, y, groups, seq_len=4):
    """Chunks tabular 5s windows into chronological blocks for temporal learning"""

    X_seq, y_seq, groups_seq = [], [], []

    unique_subs = np.unique(groups)
    unique_labels = np.unique(y)

    for sub in unique_subs:
        for lbl in unique_labels:

            mask = (groups == sub) & (y == lbl)
            X_sub_lbl = X[mask]

            if len(X_sub_lbl) < seq_len:
                continue

            for i in range(len(X_sub_lbl) - seq_len + 1):
                X_seq.append(X_sub_lbl[i:i + seq_len])
                y_seq.append(lbl)
                groups_seq.append(sub)

    return (
        np.array(X_seq),
        np.array(y_seq),
        np.array(groups_seq)
    )


# -------------------------------------------------------------
# 4. LOSO BENCHMARK ENGINE
# -------------------------------------------------------------
def main():
    print("Executing Feature Ingestion Pipeline...")
    X_raw, y_raw, groups_raw = load_all_wave_features()
    
    # Set sequence length to 4 time steps (20 seconds of continuous brain activity tracking)
    SEQ_LEN = 4 
    X_seq, y, groups = create_sequences(X_raw, y_raw, groups_raw, seq_len=SEQ_LEN)
    print(f"Dataset Formatted. Sequence Shape: {X_seq.shape} (Batches, TimeSteps, Features)")
    
    logo = LeaveOneGroupOut()
    unique_subs = np.unique(groups)
    
    results = {
        "Random Forest": [],
        "SVM": [],
        "KNN": [],
        "XGBoost": [],
        "1D-CNN (DL)": []
    }
    
    for fold, test_sub in enumerate(unique_subs, 1):
        train_mask = groups != test_sub
        test_mask = groups == test_sub
        
        X_train_raw, X_test_raw = X_seq[train_mask], X_seq[test_mask]
        y_train, y_test = y[train_mask], y[test_mask]
        
        # Flatten time steps for standard machine learning scaling and selection
        N_train, Steps, Feats = X_train_raw.shape
        N_test = X_test_raw.shape[0]
        
        X_train_flat = X_train_raw.reshape(-1, Feats)
        X_test_flat = X_test_raw.reshape(-1, Feats)
        
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train_flat)
        X_test_scaled = scaler.transform(X_test_flat)
        
        # Re-arrange back to sequences for an even split
        y_train_flat = np.repeat(y_train, Steps)
        
        # HIGH SPEED FEATURE SELECTION: Select top 50 features via ANOVA F-test
        selector = SelectKBest(score_func=f_classif, k=50)
        X_train_sel_flat = selector.fit_transform(X_train_scaled, y_train_flat)
        X_test_sel_flat = selector.transform(X_test_scaled)
        
        # Reshape data structures back to 3D time steps
        X_train_sel_3D = X_train_sel_flat.reshape(N_train, Steps, 50)
        X_test_sel_3D = X_test_sel_flat.reshape(N_test, Steps, 50)
        
        # Average across the time window steps to build optimal tabular inputs for ML
        X_train_ml = X_train_sel_3D.mean(axis=1)
        X_test_ml = X_test_sel_3D.mean(axis=1)
        
        # --- 1. Random Forest ---
        rf = RandomForestClassifier(n_estimators=150, max_depth=6, min_samples_leaf=2, random_state=42, n_jobs=-1)
        rf.fit(X_train_ml, y_train)
        results["Random Forest"].append(accuracy_score(y_test, rf.predict(X_test_ml)))
        
        # --- 2. Support Vector Machine (SVM) ---
        svm = SVC(C=2.0, kernel='rbf', gamma='scale', random_state=42)
        svm.fit(X_train_ml, y_train)
        results["SVM"].append(accuracy_score(y_test, svm.predict(X_test_ml)))
        
        # --- 3. K-Nearest Neighbors (KNN) ---
        knn = KNeighborsClassifier(n_neighbors=7, weights='distance')
        knn.fit(X_train_ml, y_train)
        results["KNN"].append(accuracy_score(y_test, knn.predict(X_test_ml)))
        
        # --- 4. XGBoost ---
        xgb = XGBClassifier(n_estimators=80, max_depth=3, learning_rate=0.05, subsample=0.8, eval_metric='logloss', random_state=42)
        xgb.fit(X_train_ml, y_train)
        results["XGBoost"].append(accuracy_score(y_test, xgb.predict(X_test_ml)))
        
        # --- 5. PyTorch 1D-CNN (Deep Learning Engine) ---
        train_loader = DataLoader(
            TensorDataset(torch.FloatTensor(X_train_sel_3D), torch.FloatTensor(y_train)), 
            batch_size=32, shuffle=True
        )
        
        model = WorkloadSequential1DCNN(input_features=50, sequence_length=Steps)
        criterion = nn.BCELoss()
        optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-3)
        
        model.train()
        for epoch in range(12):  # 12 steady training iterations
            for batch_x, batch_y in train_loader:
                optimizer.zero_grad()
                out = model(batch_x).squeeze(-1)
                loss = criterion(out, batch_y)
                loss.backward()
                optimizer.step()
                
        model.eval()
        with torch.no_grad():
            dl_out = model(torch.FloatTensor(X_test_sel_3D)).squeeze(-1)
            dl_preds = (dl_out >= 0.5).float().numpy()
            results["1D-CNN (DL)"].append(accuracy_score(y_test, dl_preds))
            
        print(f"Fold [{fold}/{len(unique_subs)}] - Subject {test_sub:02d} Evaluated. Current Highest Architecture Mode Score: {max([results[m][-1] for m in results])*100:.1f}%")

    # -------------------------------------------------------------
    # 5. FINAL COMPARISON REPORT
    # -------------------------------------------------------------
    print("\n" + "="*60)
    print("     OPTIMIZED EEG N-BACK WORKLOAD COGNITIVE REPORT     ")
    print("="*60)
    summary_data = []
    for model_name, acc_list in results.items():
        summary_data.append({
            "Model Architecture": model_name,
            "Mean Accuracy": f"{np.mean(acc_list) * 100:.2f}%",
            "Std Dev": f"±{np.std(acc_list) * 100:.2f}%",
            "Max Fold": f"{np.max(acc_list) * 100:.1f}%"
        })
        
    df_summary = pd.DataFrame(summary_data)
    print(df_summary.to_string(index=False))
    print("="*60)

if __name__ == "__main__":
    main()
