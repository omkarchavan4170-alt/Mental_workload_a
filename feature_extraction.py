# Imports
from matplotlib import pyplot as plt
import numpy as np
import scipy.signal as ss
import pandas as pd
import networkx as nx

# ------------------------- author: Minsi Hu -------------------------

# ----------------------- program description: -----------------------
#              Reads in EEG data and extracts features to 
#                      be used in classification
#              Modified to treat continuous features as waves over time.
# --------------------------------------------------------------------

# GLOBAL VARIABLES
DISABLE_PLI = True # Set to true if you only want coherence features
DISABLE_COH = False # Set to true if you only want pli features
FEATURE_TYPE = "COH" # Set for file names prefix ("PLI", "COH", "PLI_COH")
SAVE_FEATURES = True # Set to True to output the extracted wave arrays

"""
The pli(num_sensors, data) function
  Computes PLI Connectivity
"""
def pli(num_sensors, data):
  # Declare empty connectivity matrix
  pli_m = np.zeros([num_sensors, num_sensors], dtype=float)
  
  # Computing hilbert transform to extract complex components from data
  data_hilbert = np.imag(ss.hilbert(data))

  # Compute the instantaneous phase angle of data points in radians
  phase = np.arctan(data_hilbert/data)

  # Find number of data points which is the number of rows
  num_points = np.shape(data)[0]
  
  # Fill connectivity matrix by computing pli for every pair of sensors
  for i in range(num_sensors):
    for k in range(num_sensors):
      pli_m[i,k] = np.abs(np.sum(np.sign(phase[:,i]-phase[:,k])))/num_points

  # Keeping unique information
  pli_v = pli_m[np.triu_indices(pli_m.shape[0], k=1)]

  # Compute graph features
  pli_g = get_graph_features(pli_m)

  return pli_m, pli_v, pli_g

"""
The coherence(num_sensors, data, f_min, f_max, sfreq) function
  Computes coherence statistic
"""
def coherence(num_sensors, data, f_min, f_max, sfreq):
  # Declare empty connectivity_matrix
  coh_m = np.zeros([num_sensors, num_sensors], dtype=float)
  
  # Fill connectivity matrix by computing coherence for every pair of sensors
  for i in range(num_sensors):
    for k in range(num_sensors):
      f, Cxy = ss.coherence(data[:,i], data[:,k], fs = sfreq)
      coh_m[i,k] = np.mean(Cxy[np.where((f >= f_min) & (f <= f_max))])
  
  # Keeping unique information
  coh_v = coh_m[np.triu_indices(coh_m.shape[0], k=1)]

  # Compute graph features
  coh_g = get_graph_features(coh_m)

  return coh_m, coh_v, coh_g

"""
The get_graph_features(matrix) function
  Computes graph features from an adjacency matrix
"""
def get_graph_features(matrix):
  G = nx.from_numpy_array(matrix)
  features = []

  features += [nx.average_shortest_path_length(G, weight='weight')]

  for i in range(0, 14):
    features += [nx.closeness_centrality(G, u=i, distance='weight')]
    features += [nx.clustering(G, nodes=i, weight='weight')]

  return np.array(features) 

"""
The plot_m() function
  Plots the adjacency matrix given in argument and saves it to file
"""
def plot_m(matrix, title, filename):
  cax = plt.matshow(matrix)
  plt.title(title)
  plt.colorbar(cax)
  plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], 
             ["AF3", "F7", "F3", "FC5", "T7", "P7", "O1", 
              "O2", "P8", "T8", "FC6", "F4", "F8", "AF4"])
  plt.yticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], 
             ["AF3", "F7", "F3", "FC5", "T7", "P7", "O1", 
              "O2", "P8", "T8", "FC6", "F4", "F8", "AF4"])
  plt.tick_params(axis='both', which='both', labelsize=6)
  plt.savefig(f"./matrices/{filename}.png", dpi=500, bbox_inches="tight")
  plt.clf()

"""
ADDED FEATURE: The plot_feature_waves() function
  Plots the extracted connectivity features as continuous time-series waves
"""
def plot_feature_waves(df_data, title, filename):
  plt.figure(figsize=(10, 4))
  
  # Calculate the mean trend across all feature elements for each time window
  mean_wave = df_data.mean(axis=1)
  time_points = np.arange(len(mean_wave)) * 5  # 5-second steps
  
  plt.plot(time_points, mean_wave, label="Mean Global Connectivity", color='dodgerblue', linewidth=2)
  plt.title(f"Feature Connectivity Wave Over Time ({title})")
  plt.xlabel("Time (Seconds)")
  plt.ylabel("Connectivity Amplitude")
  plt.grid(True, linestyle='--', alpha=0.6)
  plt.legend()
  plt.savefig(f"./features/{filename}_wave.png", dpi=300, bbox_inches="tight")
  plt.clf()
  print(f"Saved feature wave plot to: ./features/{filename}_wave.png")

"""
The main() function
  Iterates over the full file recording lengths to transform stationary vectors 
  into ongoing rolling waveform features.
"""
def main():
  for i in range(48,49):
    print(f"Creating sequential wave features from Subject {i}...")

    key_hi = f"sub{i:02}_hi"
    key_lo = f"sub{i:02}_lo"

    # Read in the data
    data_hi = pd.read_csv(
      f"./data/STEW Dataset/{key_hi}.txt", sep="   ", header=None, 
      engine="python")
    data_lo = pd.read_csv(
      f"./data/STEW Dataset/{key_lo}.txt", sep="   ", header=None, 
      engine="python")
    
    # Create butterworth filter: bandpass 1-50hz, 6th order, 128hz sampling
    sos = ss.butter(
      N=6, Wn=[1, 50], btype='bandpass', analog=False, output='sos', fs=128)
    
    # Apply the filter to clean the data
    data_hi = ss.sosfilt(sos, data_hi)
    data_lo = ss.sosfilt(sos, data_lo)

    df_hi = pd.DataFrame()
    df_lo = pd.DataFrame()

    # MODIFICATION: Process the complete data range (19200 rows) instead of stopping at 640
    # This transforms individual metrics into an evolving time-series wave profile.
    total_rows = min(data_hi.shape[0], data_lo.shape[0])
    
    for t in range(0, total_rows, 640):
      # Safe check to ensure a full 5-second segment is available
      if t + 640 > total_rows:
        break

      interval_hi = data_hi[t:t+640,:]
      interval_lo = data_lo[t:t+640,:]

      # Compute the PLI connectivity
      pli_m_hi, pli_v_hi, pli_g_hi = pli(14, interval_hi)
      pli_m_lo, pli_v_lo, pli_g_lo = pli(14, interval_lo)

      # Compute the coherence connectivity across bands
      coh_m1_hi, coh_v1_hi, coh_g1_hi = coherence(14, interval_hi, 4, 8, 128)
      coh_m1_lo, coh_v1_lo, coh_g1_lo = coherence(14, interval_lo, 4, 8, 128)

      coh_m2_hi, coh_v2_hi, coh_g2_hi = coherence(14, interval_hi, 8, 11, 128)
      coh_m2_lo, coh_v2_lo, coh_g2_lo = coherence(14, interval_lo, 8, 11, 128)

      coh_m3_hi, coh_v3_hi, coh_g3_hi = coherence(14, interval_hi, 11, 13, 128)
      coh_m3_lo, coh_v3_lo, coh_g3_lo = coherence(14, interval_lo, 11, 13, 128)

      coh_m4_hi, coh_v4_hi, coh_g4_hi = coherence(14, interval_hi, 13, 30, 128)
      coh_m4_lo, coh_v4_lo, coh_g4_lo = coherence(14, interval_lo, 13, 30, 128)

      coh_m5_hi, coh_v5_hi, coh_g5_hi = coherence(14, interval_hi, 30, 40, 128)
      coh_m5_lo, coh_v5_lo, coh_g5_lo = coherence(14, interval_lo, 30, 40, 128)

      # Smush all connectivity vectors into a single time point vector
      combined_hi = None
      combined_lo = None
      if DISABLE_PLI:
        combined_hi = np.concatenate((coh_v1_hi, coh_v2_hi, coh_v3_hi, coh_v4_hi, coh_v5_hi, coh_g1_hi, coh_g2_hi, coh_g3_hi, coh_g4_hi, coh_g5_hi), axis=0)
        combined_lo = np.concatenate((coh_v1_lo, coh_v2_lo, coh_v3_lo, coh_v4_lo, coh_v5_lo, coh_g1_lo, coh_g2_lo, coh_g3_lo, coh_g4_lo, coh_g5_lo), axis=0)
      elif DISABLE_COH: 
        combined_hi = np.concatenate((pli_v_hi, pli_g_hi), axis=0)
        combined_lo = np.concatenate((pli_v_lo, pli_g_lo), axis=0)
      else:
        combined_hi = np.concatenate((pli_v_hi, coh_v1_hi, coh_v2_hi, coh_v3_hi, coh_v4_hi, coh_v5_hi, pli_g_hi, coh_g1_hi, coh_g2_hi, coh_g3_hi, coh_g4_hi, coh_g5_hi), axis=0)
        combined_lo = np.concatenate((pli_v_lo, coh_v1_lo, coh_v2_lo, coh_v3_lo, coh_v4_lo, coh_v5_lo, pli_g_lo, coh_g1_lo, coh_g2_lo, coh_g3_lo, coh_g4_lo, coh_g5_lo), axis=0)
      
      # Assign vectors to dataframe columns
      time_label = f"{5*t/640:.1f}-{5 + 5*t/640:.1f}s"
      df_hi[time_label] = combined_hi
      df_lo[time_label] = combined_lo

    # Transpose the dataframes so time-series frames are row instances (waves)
    df_hi = df_hi.T
    df_lo = df_lo.T

    # ADDED ACTION: Automatically visualize the structural metrics as continuous waves
    plot_feature_waves(df_hi, "High Workload", key_hi)
    plot_feature_waves(df_lo, "Low Workload", key_lo)

    # Save the features to file
    if SAVE_FEATURES:
      print(f"Saving rolling wave features from Subject {i}!")
      df_hi.to_csv(f"./features/{FEATURE_TYPE}_{key_hi}.csv")
      df_lo.to_csv(f"./features/{FEATURE_TYPE}_{key_lo}.csv")

if __name__ == "__main__":
  main()
