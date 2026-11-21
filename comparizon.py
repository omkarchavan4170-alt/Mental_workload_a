
import os
import glob
import numpy as np
import pandas as pd
import torch
import torch.nn as nn

from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from xgboost import XGBClassifier


# CONFIGURATION
SEED = 42
SEQ_LEN = 4
TOP_FEATURES = 50
EPOCHS = 30
BATCH_SIZE = 32
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

np.random.seed(SEED)
torch.manual_seed(SEED)


# CNN MODEL
class CNN(nn.Module):
    def __init__(self, features):
        super().__init__()

        self.conv = nn.Sequential(
            nn.Conv1d(features, 64, 2, padding=1),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Dropout(0.3),

            nn.Conv1d(64, 32, 2, padding=1),
            nn.BatchNorm1d(32),
            nn.ReLU(),

            nn.AdaptiveAvgPool1d(1)
        )

        self.fc = nn.Sequential(
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Dropout(0.4),
            nn.Linear(16, 1)
        )

    def forward(self, x):
        x = self.conv(x.transpose(1, 2))
        return self.fc(x.squeeze(-1))


# LOAD DATA
def load_data():

    X, y, groups, segments = [], [], [], []

    files = sorted(glob.glob("./features/COH_sub*.csv"))

    if not files:
        raise FileNotFoundError("No STEW feature CSV files found.")

    feature_names = None

    for segment, path in enumerate(files):

        parts = os.path.basename(path).replace(".csv", "").split("_")

        subject = int(parts[1].replace("sub", ""))

        if parts[2] == "hi":
            label = 1
        elif parts[2] == "lo":
            label = 0
        else:
            raise ValueError(f"Unknown label: {path}")

        df = pd.read_csv(path, index_col=0)
        df = df.apply(pd.to_numeric, errors="coerce")
        df = df.replace([np.inf, -np.inf], np.nan).dropna()

        if df.empty:
            continue

        if feature_names is None:
            feature_names = df.columns.tolist()
        elif df.columns.tolist() != feature_names:
            raise ValueError(f"Feature mismatch: {path}")

        data = df.to_numpy(dtype=np.float32)

        X.append(data)
        y.append(np.full(len(data), label))
        groups.append(np.full(len(data), subject))
        segments.append(np.full(len(data), segment))

    return (
        np.vstack(X),
        np.concatenate(y),
        np.concatenate(groups),
        np.concatenate(segments)
    )


# CREATE CHRONOLOGICAL SEQUENCES
def create_sequences(X, y, groups, segments):

    X_seq, y_seq, groups_seq = [], [], []

    for segment in np.unique(segments):

        idx = np.where(segments == segment)[0]

        data = X[idx]
        labels = y[idx]
        subjects = groups[idx]

        if len(np.unique(labels)) != 1 or len(np.unique(subjects)) != 1:
            raise ValueError("Mixed subject or label in a recording.")

        if len(data) < SEQ_LEN:
            continue

        for i in range(len(data) - SEQ_LEN + 1):

            X_seq.append(data[i:i + SEQ_LEN])
            y_seq.append(labels[0])
            groups_seq.append(subjects[0])

    return (
        np.asarray(X_seq, dtype=np.float32),
        np.asarray(y_seq, dtype=np.int64),
        np.asarray(groups_seq, dtype=np.int64)
    )


# TRAIN CNN
def train_cnn(X_train, y_train, X_test):

    model = CNN(X_train.shape[2]).to(DEVICE)

    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=0.001,
        weight_decay=1e-4
    )

    loss_fn = nn.BCEWithLogitsLoss()

    dataset = TensorDataset(
        torch.tensor(X_train, dtype=torch.float32),
        torch.tensor(y_train.reshape(-1, 1), dtype=torch.float32)
    )

    loader = DataLoader(
        dataset,
        batch_size=BATCH_SIZE,
        shuffle=True
    )

    model.train()

    for epoch in range(EPOCHS):

        for xb, yb in loader:

            xb, yb = xb.to(DEVICE), yb.to(DEVICE)

            optimizer.zero_grad()
            loss = loss_fn(model(xb), yb)
            loss.backward()
            optimizer.step()

    model.eval()

    with torch.no_grad():

        logits = model(
            torch.tensor(X_test, dtype=torch.float32).to(DEVICE)
        )

        predictions = (logits >= 0).int().cpu().numpy().flatten()

    return predictions


# EVALUATION METRICS
def evaluate(y_true, y_pred):

    return {
        "Accuracy": accuracy_score(y_true, y_pred) * 100,
        "Precision": precision_score(y_true, y_pred, zero_division=0) * 100,
        "Recall": recall_score(y_true, y_pred, zero_division=0) * 100,
        "F1": f1_score(y_true, y_pred, zero_division=0) * 100
    }


# MAIN PIPELINE
def main():

    print("Loading STEW dataset...")

    X, y, groups, segments = load_data()

    X, y, groups = create_sequences(X, y, groups, segments)

    print("Sequence shape:", X.shape)
    print("Subjects:", len(np.unique(groups)))

    models = {
        "Random Forest": RandomForestClassifier(
            n_estimators=150,
            max_depth=6,
            min_samples_leaf=2,
            random_state=SEED,
            n_jobs=-1
        ),

        "SVM": SVC(
            C=2.0,
            kernel="rbf",
            gamma="scale"
        ),

        "KNN": KNeighborsClassifier(
            n_neighbors=7,
            weights="distance"
        ),

        "XGBoost": XGBClassifier(
            n_estimators=80,
            max_depth=3,
            learning_rate=0.05,
            subsample=0.8,
            eval_metric="logloss",
            random_state=SEED,
            n_jobs=-1,
            verbosity=0
        )
    }

    results = []

    logo = LeaveOneGroupOut()

    for fold, (train_idx, test_idx) in enumerate(
        logo.split(X, y, groups), 1
    ):

        print(f"Fold [{fold}/{len(np.unique(groups))}]")

        X_train, X_test = X[train_idx], X[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]

        if len(np.unique(y_train)) != 2:
            raise ValueError("Training data must contain both classes.")

        n_train, steps, features = X_train.shape
        n_test = X_test.shape[0]

        # NORMALIZATION
        scaler = StandardScaler()

        X_train = scaler.fit_transform(
            X_train.reshape(-1, features)
        )

        X_test = scaler.transform(
            X_test.reshape(-1, features)
        )

        # FEATURE SELECTION
        selector = SelectKBest(
            f_classif,
            k=min(TOP_FEATURES, features)
        )

        y_train_steps = np.repeat(y_train, steps)

        X_train = selector.fit_transform(X_train, y_train_steps)
        X_test = selector.transform(X_test)

        selected = X_train.shape[1]

        X_train = X_train.reshape(n_train, steps, selected)
        X_test = X_test.reshape(n_test, steps, selected)

        # TRADITIONAL ML
        X_train_ml = X_train.mean(axis=1)
        X_test_ml = X_test.mean(axis=1)

        subject = groups[test_idx][0]

        for name, model in models.items():

            model.fit(X_train_ml, y_train)
            pred = model.predict(X_test_ml)

            results.append({
                "Subject": subject,
                "Model": name,
                **evaluate(y_test, pred)
            })

        # CNN
        pred = train_cnn(X_train, y_train, X_test)

        results.append({
            "Subject": subject,
            "Model": "1D-CNN",
            **evaluate(y_test, pred)
        })

    # FINAL REPORT
    df = pd.DataFrame(results)

    summary = df.groupby("Model").agg({
        "Accuracy": ["mean", "std"],
        "Precision": "mean",
        "Recall": "mean",
        "F1": "mean"
    })

    print("\nSTEW EEG WORKLOAD CLASSIFICATION")
    print(summary.round(2))

    os.makedirs("results", exist_ok=True)

    df.to_csv("results/subject_results.csv", index=False)
    summary.to_csv("results/model_summary.csv")

    print("\nResults saved in results/")


if __name__ == "__main__":
    main()
