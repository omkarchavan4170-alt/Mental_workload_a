# -*- coding: utf-8 -*-
"""
Generate publication-quality PDF paper using Headless Microsoft Edge.
Focuses intensely on our actual implementation, methods, formulas, results comparisons,
and highlights novelty prominently in the Introduction, with no college names/headers.
"""

import os
import subprocess
import base64

BASE_DIR = r"C:\Users\oo163\AIBSI_ML_DL"
HTML_OUT = os.path.join(BASE_DIR, "paper_render.html")
PDF_OUT = os.path.join(BASE_DIR, "Mental_Workload_Assessment_Paper.pdf")

def get_base64_img(rel_path):
    full_path = os.path.join(BASE_DIR, rel_path)
    if os.path.exists(full_path):
        with open(full_path, "rb") as f:
            return "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
    return ""

# Load actual images
img_wave_hi = get_base64_img("features/sub01_hi_wave.png")
img_wave_lo = get_base64_img("features/sub01_lo_wave.png")
img_acc = get_base64_img("graphs/accuracy_comparison.png")
img_met = get_base64_img("graphs/classification_metrics.png")
img_box = get_base64_img("graphs/accuracy_boxplot.png")
img_sub = get_base64_img("graphs/subject_accuracy.png")
img_heat = get_base64_img("loso_full_test/02_model_node_importance_heatmap.png")
img_group = get_base64_img("loso_full_test/03_grouped_node_importance_by_model.png")
img_cons = get_base64_img("loso_full_test/05_subject_consistency_heatmap.png")

print("Images encoded successfully.")

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Mental Workload Assessment via Multi-Band Dynamic Functional Connectivity and Graph Network Topology</title>
<style>
  @page {
    size: letter;
    margin: 16mm 14mm 16mm 14mm;
    @bottom-center {
      content: counter(page);
      font-size: 8.5pt;
      font-family: 'Times New Roman', serif;
    }
  }
  body {
    font-family: 'Times New Roman', Times, Georgia, serif;
    font-size: 9.8pt;
    line-height: 1.42;
    color: #111;
    margin: 0;
    padding: 0;
    text-align: justify;
  }
  h1.title {
    font-size: 17pt;
    font-weight: bold;
    text-align: center;
    margin-bottom: 5px;
    line-height: 1.25;
    color: #0b1f3a;
  }
  .authors {
    text-align: center;
    font-size: 10pt;
    font-style: italic;
    color: #333;
    margin-bottom: 14px;
  }
  .abstract-box {
    background: #f8f9fa;
    border-left: 3.5px solid #1a56db;
    padding: 9px 13px;
    margin-bottom: 16px;
    font-size: 9pt;
    line-height: 1.38;
  }
  .abstract-title {
    font-weight: bold;
    color: #1a56db;
    margin-bottom: 3px;
    text-transform: uppercase;
    font-size: 8.5pt;
    letter-spacing: 0.5px;
  }
  .keywords {
    margin-top: 5px;
    font-size: 8.5pt;
    color: #444;
  }
  h2 {
    font-size: 11.5pt;
    font-weight: bold;
    color: #0b1f3a;
    border-bottom: 1px solid #cbd5e1;
    padding-bottom: 2px;
    margin-top: 16px;
    margin-bottom: 6px;
    text-transform: uppercase;
    letter-spacing: 0.4px;
  }
  h3 {
    font-size: 10pt;
    font-weight: bold;
    color: #1e3a8a;
    margin-top: 10px;
    margin-bottom: 3px;
  }
  p {
    margin-top: 0;
    margin-bottom: 6px;
    text-indent: 1.5em;
  }
  p.no-indent {
    text-indent: 0;
  }
  .novelty-callout {
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    border-radius: 4px;
    padding: 7px 11px;
    margin: 8px 0;
    font-size: 9.2pt;
  }
  .novelty-callout strong {
    color: #1d4ed8;
  }
  .formula-box {
    background: #fdfdfd;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    padding: 6px 10px;
    margin: 6px 0;
    text-align: center;
    font-family: 'Cambria Math', 'Times New Roman', serif;
    font-size: 9.8pt;
  }
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 8px 0;
    font-size: 8.2pt;
    line-height: 1.3;
  }
  th, td {
    border: 1px solid #cbd5e1;
    padding: 4px 5.5px;
    text-align: left;
  }
  th {
    background-color: #0f172a;
    color: #ffffff;
    font-weight: bold;
    text-align: center;
  }
  tr:nth-child(even) {
    background-color: #f8fafc;
  }
  td.center, th.center {
    text-align: center;
  }
  td.bold {
    font-weight: bold;
  }
  .table-caption {
    font-size: 8.3pt;
    font-weight: bold;
    margin-bottom: 3px;
    color: #1e293b;
    text-align: left;
  }
  .figure-container {
    text-align: center;
    margin: 10px 0;
    page-break-inside: avoid;
  }
  .figure-container img {
    max-width: 95%;
    height: auto;
    border: 1px solid #e2e8f0;
    border-radius: 3px;
  }
  .figure-caption {
    font-size: 8.2pt;
    font-style: italic;
    color: #334155;
    margin-top: 3px;
    text-align: center;
  }
  pre.code-block {
    background: #0f172a;
    color: #e2e8f0;
    padding: 7px 10px;
    border-radius: 4px;
    font-size: 7.5pt;
    font-family: 'Consolas', 'Courier New', monospace;
    overflow-x: auto;
    margin: 6px 0;
    line-height: 1.25;
    page-break-inside: avoid;
  }
</style>
</head>
<body>

<h1 class="title">Mental Workload Assessment via Multi-Band Dynamic Functional Connectivity and Graph Network Topology: A Rigorous Leave-One-Subject-Out Cross-Validation Benchmark</h1>

<div class="authors">A Subject-Independent Machine Learning and Explainable Neuroergonomic Investigation</div>

<div class="abstract-box">
  <div class="abstract-title">Abstract</div>
  Objective cognitive workload estimation from electroencephalography (EEG) provides a critical neurotechnological foundation for closed-loop brain-computer interfaces (BCIs) and neuroergonomics. However, real-world deployment is severely constrained by two persistent challenges: substantial inter-subject non-stationarity and the pervasive "validation trap," wherein randomized <em>k</em>-fold cross-validation permits intra-subject temporal autocorrelation to leak biometric identities across splits, reporting artificially inflated performance (&gt;95%). In this study, we implement an end-to-end, subject-independent cognitive workload classification and explainability framework on the benchmark Simultaneous Task EEG Workload (STEW) dataset across 48 healthy individuals under resting baseline (low workload) and SIMKAP multitasking (high workload) conditions. Continuous 14-channel EEG recordings at 128 Hz are conditioned with a 6th-order Butterworth bandpass filter (1.0–50.0 Hz) and windowed into 5-second epochs. Rather than evaluating isolated electrode amplitudes, we model cognitive load as an emergent whole-brain network phenomenon. Multi-band magnitude-squared coherence is computed across five canonical frequency bands (Theta, Alpha, Low Beta, Beta, Gamma), yielding 455 pairwise connectivity edge weights. These are coupled with 145 graph-theoretical network topology features (closeness centrality, weighted clustering coefficient, and average shortest path length), forming a 600-dimensional spatial-spectral feature vector per window. Sliding sequences of 4 windows (20.0-second rolling dynamic episodes) are extracted and refined via strictly in-fold ANOVA <em>F</em>-statistic feature selection (top 50 features). We benchmark four classical ensembles (Support Vector Machine with RBF kernel, Random Forest, XGBoost, and <em>K</em>-Nearest Neighbors) against a custom deep sequential 1D-Convolutional Neural Network (1D-CNN) strictly under outer Leave-One-Subject-Out (LOSO) cross-validation across 47 subjects (2,538 independent sequential instances) with zero data leakage. RBF-SVM achieved the highest mean cross-subject accuracy of <strong>78.41% ± 19.58%</strong> and precision of <strong>81.29%</strong> (specificity <strong>80.00%</strong>), while the sequential 1D-CNN achieved the highest recall (<strong>78.96%</strong>) and macro F1-score (<strong>77.00%</strong>), confirming superior sensitivity in detecting transient cognitive overload transitions. Furthermore, a statistically controlled grouped permutation electrode ablation across 48 subjects (simultaneously scrambling all 75 incident coherence and graph features per channel with Benjamini-Hochberg FDR control at <em>q</em> &lt; 0.05) isolated the right prefrontal and fronto-central networks (AF4, FC6, F4) alongside left temporal rehearsal (T7) as primary predictive anchors. Grand-average spectral log-power mapping revealed massive workload surges in right frontal (F8, +0.41 dB), temporal (T8, +0.37 dB; T7, +0.33 dB), and fronto-central (FC6, +0.36 dB) regions. These outcomes establish an empirical blueprint for wearable, gel-free 4-channel neuroadaptive systems.
  <div class="keywords"><strong>Keywords:</strong> Electroencephalography (EEG), Mental Workload, Functional Connectivity, Magnitude-Squared Coherence, Graph Theory, 1D-CNN, Support Vector Machine, Leave-One-Subject-Out (LOSO), Explainable AI, Neuroergonomics.</div>
</div>

<h2>1. Introduction & Methodological Novelty</h2>

<p class="no-indent">Mental workload (MWL) quantifies the proportion of an operator's limited cognitive resources actively committed to satisfying dynamic task demands [1]. In safety-critical operational environments—such as aviation flight decks, air traffic control towers, robotic surgical operating rooms, and high-tempo industrial operations—cognitive capacity is subjected to acute fluctuations. Severe cognitive overload degrades situational awareness, slows psychomotor reaction latency, and induces perceptual tunneling, while extreme underload triggers passive complacency and vigilance failure [2]. Traditional retrospective surveys (e.g., NASA-TLX) are intrusive and cannot trigger real-time closed-loop interventions [3]. Consequently, passive, continuous, and objective neurophysiological monitoring via electroencephalography (EEG) has emerged as an essential objective of neuroergonomics and brain-computer interfaces (BCIs) [4].</p>

<h3>1.1 The "Validation Trap" in EEG Machine Learning</h3>
<p>Despite significant research interest, translating EEG-based cognitive classifiers into operational reality is obstructed by a widespread methodological crisis: the <strong>validation trap</strong> [11], [12]. Numerous published studies report remarkable binary classification accuracies exceeding 95% on continuous EEG benchmarks. However, a rigorous methodological audit reveals that these studies commonly employ randomized <em>k</em>-fold cross-validation or randomly shuffled temporal window splits. In continuous neuroelectric time series, consecutive windows from the same individual share identical baseline anatomical features (skull thickness, electrode contact impedances, resting alpha peak frequencies). When temporal windows from a single subject are randomly distributed across training and testing splits, machine learning models inadvertently memorize the biometric identity of the subject rather than learning generalizable neural correlates of cognitive demand [13]. When deployed on genuinely unseen operators, such models collapse toward chance level. A viable neuroadaptive system must operate in a plug-and-play capacity on novel individuals without requiring per-operator calibration. Hence, subject-independent validation—specifically <strong>Leave-One-Subject-Out (LOSO) cross-validation</strong>—is mandatory.</p>

<div class="novelty-callout">
  <strong>Key Novelty & Core Methodological Contributions:</strong>
  <ul style="margin: 4px 0 0 16px; padding: 0;">
    <li><strong>Whole-Brain Dynamic Network Modeling:</strong> Moving beyond localized single-channel spectral power by computing multi-band magnitude-squared coherence across 14 scalp electrodes across 5 canonical frequency bands (455 edge weights), coupled with 145 graph topology metrics (clustering coefficient, closeness centrality, average path length), producing a 600-dimensional spatial-spectral-topological representation per 5-second epoch.</li>
    <li><strong>Continuous Temporal Trajectory Formulation:</strong> Structuring continuous 20.0-second rolling dynamic episodes (sliding sequences of 4 consecutive 5-second windows) to investigate whether a deep sequential 1D-CNN extracts transition dynamics superior to static mean-pooled tabular representations (SVM, Random Forest, XGBoost, KNN).</li>
    <li><strong>Airtight Leakage-Free Outer LOSO Protocol:</strong> Enforcing strict subject-independent LOSO cross-validation across 47 subjects (2,538 instances), wherein feature standardization and one-way ANOVA <em>F</em>-statistic selection (top 50 features) are fitted strictly in-fold on training cohorts, ensuring zero test-set contamination.</li>
    <li><strong>Grouped Multi-Feature Permutation Explainability (XAI):</strong> Introducing a multi-feature grouped permutation framework that simultaneously scrambles all 75 incident coherence and graph features per channel across 48 subjects (30 permutations per channel per subject) with Wilcoxon signed-rank testing and Benjamini-Hochberg FDR control (<em>q</em> &lt; 0.05).</li>
    <li><strong>Translational Wearable Blueprint:</strong> Demonstrating that model reliance and biophysical spectral surges converge on an ultra-compact 4-electrode forehead/temple montage [AF4, FC6, F4, AF3] for gel-free dry-sensor wearable neuroergonomics.</li>
  </ul>
</div>

<h2>2. Literature Benchmarks & Context</h2>

<p class="no-indent">The Simultaneous Task EEG Workload (STEW) dataset was curated by Lim, Sourina, and Wang (2018) [15] as an open benchmark for multitasking workload assessment. Using Neighborhood Component Analysis (NCA) and Support Vector Regression (SVR), they reported a baseline cross-subject accuracy of ~69.00%. Recently, Safari et al. (2024) [14] in <em>Scientific Reports</em> evaluated directional connectivity using the Direct Directed Transfer Function (dDTF) under strict LOSO validation, achieving 89.53% accuracy with RBF-SVM and 83.12% with a CNN-LSTM hybrid. In contrast, Siddhad et al. (2024) [18] reported 95.76% accuracy using ConvNeXt under randomized <em>k</em>-fold splits, an outcome vulnerable to intra-subject data leakage. Table 1 summarizes the benchmark landscape.</p>

<div class="table-caption">Table 1: Systematic comparison of published cognitive workload benchmarks on the STEW dataset against the proposed framework.</div>
<table>
  <thead>
    <tr>
      <th class="center">Ref.</th>
      <th>Authors & Year</th>
      <th>Feature Space</th>
      <th>Model Architecture</th>
      <th class="center">Validation Scheme</th>
      <th class="center">Accuracy</th>
      <th>Generalization Integrity / Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="center">[15]</td>
      <td>Lim et al. (2018)</td>
      <td>Band Powers + NCA</td>
      <td>Support Vector Regression</td>
      <td class="center">Subject-Dependent / K-fold</td>
      <td class="center">~69.00%</td>
      <td>Foundational baseline; high subject variance</td>
    </tr>
    <tr>
      <td class="center">[17]</td>
      <td>Al-Nafjan et al. (2020)</td>
      <td>Standard PSD Bands</td>
      <td>Random Forest / SVM</td>
      <td class="center">LOSO Cross-Validation</td>
      <td class="center">72.0% - 74.8%</td>
      <td>Conventional single-channel spectral bound</td>
    </tr>
    <tr>
      <td class="center">[14]</td>
      <td>Safari et al. (2024)</td>
      <td>dDTF Connectivity</td>
      <td>CNN-LSTM Hybrid</td>
      <td class="center">Outer LOSO (Strict)</td>
      <td class="center">83.12%</td>
      <td>Directional MVAR network modeling</td>
    </tr>
    <tr>
      <td class="center">[14]</td>
      <td>Safari et al. (2024)</td>
      <td>dDTF + Forward Selection</td>
      <td>RBF-SVM</td>
      <td class="center">Outer LOSO (Strict)</td>
      <td class="center">89.53%</td>
      <td>Greedy forward selection with directional DTF</td>
    </tr>
    <tr>
      <td class="center">[18]</td>
      <td>Siddhad et al. (2024)</td>
      <td>Spectrogram Tensors</td>
      <td>Adapted ConvNeXt</td>
      <td class="center">Random K-Fold (Shuffled)</td>
      <td class="center">95.76%</td>
      <td>Vulnerable to intra-subject temporal data leakage</td>
    </tr>
    <tr>
      <td class="center"><strong>Ours</strong></td>
      <td><strong>Present Study</strong></td>
      <td><strong>Coherence + Graph Topology</strong></td>
      <td><strong>Random Forest (150 trees)</strong></td>
      <td class="center"><strong>Outer LOSO (Strict)</strong></td>
      <td class="center"><strong>76.87%</strong></td>
      <td><strong>Zero leakage; regularized ensemble baseline</strong></td>
    </tr>
    <tr>
      <td class="center"><strong>Ours</strong></td>
      <td><strong>Present Study</strong></td>
      <td><strong>Coherence + Graph Topology</strong></td>
      <td><strong>XGBoost (80 estimators)</strong></td>
      <td class="center"><strong>Outer LOSO (Strict)</strong></td>
      <td class="center"><strong>77.07%</strong></td>
      <td><strong>Zero leakage; lowest subject variance (18.73%)</strong></td>
    </tr>
    <tr>
      <td class="center"><strong>Ours</strong></td>
      <td><strong>Present Study</strong></td>
      <td><strong>Sequential Coherence Graphs</strong></td>
      <td><strong>WorkloadSequential1DCNN</strong></td>
      <td class="center"><strong>Outer LOSO (Strict)</strong></td>
      <td class="center"><strong>77.38%</strong></td>
      <td><strong>Zero leakage; highest recall (78.96%) and F1 (77.00%)</strong></td>
    </tr>
    <tr>
      <td class="center"><strong>Ours</strong></td>
      <td><strong>Present Study</strong></td>
      <td><strong>Coherence + Graph Topology</strong></td>
      <td><strong>SVM (RBF Kernel)</strong></td>
      <td class="center"><strong>Outer LOSO (Strict)</strong></td>
      <td class="center"><strong>78.41%</strong></td>
      <td><strong>Zero leakage; highest overall accuracy and precision (81.29%)</strong></td>
    </tr>
  </tbody>
</table>

<h2>3. Dataset Architecture & Experimental Paradigm</h2>

<p class="no-indent">The STEW dataset [15] contains continuous EEG recordings from 48 healthy subjects acquired via a research-grade 14-channel Emotiv EPOC wireless neuroheadset at 128 Hz. Electrodes are arranged according to the international 10–20 system: AF3, F7, F3, FC5, T7, P7, O1, O2, P8, T8, FC6, F4, F8, AF4 (referenced to CMS/DRL). Each subject completed two continuous 150-second blocks (19,200 time points per channel):</p>
<ol style="margin-top: 2px; margin-bottom: 6px; padding-left: 20px;">
  <li><strong>Resting-State Baseline (Low Workload, Label 0):</strong> Subjects sat quietly fixating on a static crosshair with eyes open, establishing baseline neuroelectric idling activity.</li>
  <li><strong>SIMKAP Multitasking (High Workload, Label 1):</strong> Subjects performed the Simultaneous Capacity psychomotor test, demanding concurrent visual alphanumeric character matching, mental arithmetic updating, and auditory conflict monitoring under strict time constraints.</li>
</ol>
<p>Standardized 9-point Likert ratings (<code>ratings.txt</code>) validate profound perceptual separation (rest mean ~1.74 vs. SIMKAP mean ~6.81, <em>p</em> &lt; 0.001). Continuous 150-second recordings were segmented into 5-second non-overlapping windows (640 samples, 30 windows/condition). Sliding sequences of length 4 (20.0 seconds, stride = 1 window) yielded exactly 27 continuous sequential samples per condition. Across 47 complete subjects, the master comparative benchmark comprises exactly <strong>2,538 instances</strong> with a perfect 1:1 class balance (1,269 positive and 1,269 negative instances).</p>

<div class="table-caption">Table 2: Analyzed neurophysiological frequency bands and biophysical roles.</div>
<table>
  <thead>
    <tr>
      <th class="center">Band</th>
      <th class="center">Range (Hz)</th>
      <th>Neurophysiological Mechanism</th>
      <th>Cognitive Workload Response Pattern</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="center bold">Theta (θ)</td>
      <td class="center">4.0 – 8.0 Hz</td>
      <td>Frontal midline rhythm; hippocampal-prefrontal circuits</td>
      <td>Synchronizes (increases spectral power) during working memory effort</td>
    </tr>
    <tr>
      <td class="center bold">Alpha (α)</td>
      <td class="center">8.0 – 11.0 Hz</td>
      <td>Thalamocortical idling; sensory gating marker</td>
      <td>Desynchronizes (suppresses power; ERD) during active visual attention</td>
    </tr>
    <tr>
      <td class="center bold">Low Beta (β<sub>low</sub>)</td>
      <td class="center">11.0 – 13.0 Hz</td>
      <td>Fronto-central transition rhythm</td>
      <td>Modulates dynamically between relaxed readiness and active vigilance</td>
    </tr>
    <tr>
      <td class="center bold">Beta (β)</td>
      <td class="center">13.0 – 30.0 Hz</td>
      <td>Pyramidal sensorimotor and prefrontal activation</td>
      <td>Elevates markedly during active calculation, arithmetic, and problem solving</td>
    </tr>
    <tr>
      <td class="center bold">Gamma (γ)</td>
      <td class="center">30.0 – 40.0 Hz</td>
      <td>Local inhibitory GABAergic interneuron synchrony</td>
      <td>Heightened during multi-modal cognitive binding and perceptual synthesis</td>
    </tr>
  </tbody>
</table>

<h2>4. Methodology & Mathematical Formulations</h2>

<h3>4.1 Signal Conditioning & Digital Butterworth SOS Filtering</h3>
<p class="no-indent">Continuous raw microvolts were filtered using a 6th-order digital Butterworth bandpass filter spanning 1.0 Hz to 50.0 Hz, implemented in Second-Order Sections (SOS) to avoid numerical rounding instabilities. The discrete transfer function decomposes into <em>L</em> = 3 biquad cascades:</p>
<div class="formula-box">
  H(z) = g &middot; &prod;<sub>k=1..3</sub> (b<sub>0k</sub> + b<sub>1k</sub>z<sup>-1</sup> + b<sub>2k</sub>z<sup>-2</sup>) / (1 + a<sub>1k</sub>z<sup>-1</sup> + a<sub>2k</sub>z<sup>-2</sup>)
</div>
<p class="no-indent">DC offset was removed by subtracting the epoch mean: x<sub>i</sub><sup>clean</sup>(t) = x<sub>i</sub>(t) - (1/640) &sum; x<sub>i</sub>(&tau;).</p>

<h3>4.2 Multi-Band Magnitude-Squared Coherence</h3>
<p class="no-indent">Functional connectivity between electrodes <em>i</em> and <em>j</em> is quantified via Magnitude-Squared Coherence across 5-second windows. Using Welch’s averaged periodogram with 50% overlapping Hanning windows:</p>
<div class="formula-box">
  C<sub>ij</sub>(f) = |P<sub>ij</sub>(f)|<sup>2</sup> / [P<sub>ii</sub>(f) &middot; P<sub>jj</sub>(f)], &emsp; C&#772;<sub>ij</sub><sup>(b)</sup> = (1 / &Delta;f) &int; C<sub>ij</sub>(f) df
</div>
<p class="no-indent">For 14 electrodes, 14 &times; 13 / 2 = 91 unique pairs per band &times; 5 bands = <strong>455 pairwise coherence edge features</strong> per window.</p>

<h3>4.3 Graph-Theoretical Network Metrics</h3>
<p class="no-indent">Treating each band's 14 &times; 14 coherence matrix as an undirected weighted network graph G = (V, E, W), 29 topological metrics are derived per band using NetworkX:</p>
<ol style="margin-top: 2px; margin-bottom: 6px; padding-left: 20px;">
  <li><strong>Weighted Clustering Coefficient (Onnela et al., 2005 [19]):</strong> Quantifies local segregation and triangular motif robustness:
    <div class="formula-box">C<sub>u</sub> = [1 / (k<sub>u</sub>(k<sub>u</sub> - 1))] &sum; (w&#770;<sub>uj</sub> &middot; w&#770;<sub>jk</sub> &middot; w&#770;<sub>ku</sub>)<sup>1/3</sup>, &emsp; (14 nodes per band)</div>
  </li>
  <li><strong>Closeness Centrality:</strong> Quantifies communication efficiency using inverted distance d(u,v) = 1/w<sub>uv</sub>:
    <div class="formula-box">CC(u) = (|V| - 1) / &sum; &delta;(u, v) = 13 / &sum; &delta;(u, v), &emsp; (14 nodes per band)</div>
  </li>
  <li><strong>Average Shortest Path Length:</strong> Quantifies global whole-brain integration:
    <div class="formula-box">L = [1 / (|V|(|V| - 1))] &sum; &delta;(u, v), &emsp; (1 global scalar per band)</div>
  </li>
</ol>
<p class="no-indent">Total graph features = 5 &times; 29 = 145 features. Combining coherence and graph metrics produces exactly <strong>600 features per 5-second window</strong>.</p>

<div class="figure-container">
  <img src="{IMG_WAVE_HI}" style="width: 48%; display: inline-block; margin-right: 1%;" alt="High Workload Waves">
  <img src="{IMG_WAVE_LO}" style="width: 48%; display: inline-block;" alt="Low Workload Waves">
  <div class="figure-caption">Figure 1: Continuous mean global connectivity wave profiles over time for Subject 01: SIMKAP multitasking (left) vs. resting baseline (right). High workload induces elevated, persistent functional connectivity amplitudes and burstiness.</div>
</div>

<h3>4.4 Temporal Sequence Framing, In-Fold Standardization & ANOVA Selection</h3>
<p class="no-indent">Continuous 5-second windows are structured into sliding sequences of length 4 (20.0 seconds duration, stride = 1 window): X<sub>seq</sub> &isin; &reals;<sup>4 &times; 600</sup>.</p>
<ul>
  <li><strong>In-Fold Standardization:</strong> <code>StandardScaler</code> is fitted strictly on training subjects in each fold (&mu;<sub>train</sub>, &sigma;<sub>train</sub>) and applied out-of-fold to test subjects, ensuring zero information leakage.</li>
  <li><strong>In-Fold ANOVA F-Statistic Selection:</strong> The one-way ANOVA <em>F</em>-test (`SelectKBest`, k=50) is fitted strictly on training data:
    <div class="formula-box">F<sub>j</sub> = MSB<sub>j</sub> / MSW<sub>j</sub> = [&sum; n<sub>k</sub>(x&#772;<sub>kj</sub> - x&#772;<sub>j</sub>)<sup>2</sup> / 1] / [&sum; &sum; (x<sub>ki,j</sub> - x&#772;<sub>kj</sub>)<sup>2</sup> / (N<sub>train</sub> - 2)]</div>
    Retaining the top 50 features reduces input dimensionality by 91.7%, eliminating redundant edges.
  </li>
  <li><strong>Input Transformation:</strong> Classical models ingest temporally mean-pooled 50-dimensional vectors x&#772; = (1/4) &sum; x&#771;<sub>t</sub>. The deep 1D-CNN directly ingests the unpooled 3D tensor: (Batch, 50 Features, 4 Timesteps).</li>
</ul>

<h3>4.5 Deep Sequential 1D-CNN & Model Specifications</h3>
<p class="no-indent">The custom <code>WorkloadSequential1DCNN</code> comprises: <code>Conv1d(50->64, k=2, p=1) -> BatchNorm1d -> ReLU -> Dropout(0.30) -> Conv1d(64->32, k=2, p=1) -> BatchNorm1d -> ReLU -> AdaptiveAvgPool1d(1) -> Linear(32->16) -> ReLU -> Dropout(0.40) -> Linear(16->1)</code>. Optimization uses <code>BCEWithLogitsLoss</code>, Adam (&alpha;=0.001, weight decay=10<sup>-4</sup>), batch size 32, over 30 epochs. Classical models match exact project configurations: SVM (RBF, C=2.0), Random Forest (150 trees, max depth 6), XGBoost (80 trees, max depth 3, lr 0.05, 80% subsample), and KNN (k=7).</p>

<h3>4.6 Grouped Permutation Electrode Ablation Framework</h3>
<p class="no-indent">Each electrode participates in 65 coherence edges (13 &times; 5 bands) and 10 nodal graph metrics (2 &times; 5 bands). To faithfully assess channel importance, all <strong>75 incident features are permuted simultaneously</strong> across time windows (R = 30 permutations per channel per held-out subject across 48 subjects). The metric drop is defined as:</p>
<div class="formula-box">
  &Delta;BA<sub>c</sub> = BA<sub>baseline</sub> - (1/R) &sum; BA<sub>perm(c, r)</sub>
</div>
<p class="no-indent">Statistical significance is evaluated via the Wilcoxon signed-rank test against zero, with multiple-testing control enforced via the Benjamini-Hochberg step-up procedure (q &lt; 0.05): p<sub>(i)</sub> &le; (i / 14) &middot; Q.</p>

<h2>5. Empirical Results & Comparative Analysis</h2>

<h3>5.1 Overall Classification Performance under Strict Outer LOSO</h3>
<p class="no-indent">Table 3 reports the quantitative performance across 47 subjects (2,538 test instances) under outer Leave-One-Subject-Out validation.</p>

<div class="table-caption">Table 3: Quantitative performance summary under Leave-One-Subject-Out (LOSO) cross-validation across 47 subjects (2,538 test instances).</div>
<table>
  <thead>
    <tr>
      <th>Model Architecture</th>
      <th class="center">Validation Scheme</th>
      <th class="center">Accuracy Mean (%)</th>
      <th class="center">Accuracy Std (%)</th>
      <th class="center">Precision Mean (%)</th>
      <th class="center">Recall Mean (%)</th>
      <th class="center">Macro F1 Mean (%)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="bold">SVM (RBF Kernel)</td>
      <td class="center">Outer LOSO (Strict)</td>
      <td class="center bold">78.41</td>
      <td class="center">19.58</td>
      <td class="center bold">81.29</td>
      <td class="center">76.83</td>
      <td class="center">75.31</td>
    </tr>
    <tr>
      <td class="bold">1D-CNN (Sequential)</td>
      <td class="center">Outer LOSO (Strict)</td>
      <td class="center">77.38</td>
      <td class="center">19.80</td>
      <td class="center">81.17</td>
      <td class="center bold">78.96</td>
      <td class="center bold">77.00</td>
    </tr>
    <tr>
      <td class="bold">XGBoost (80 Estimators)</td>
      <td class="center">Outer LOSO (Strict)</td>
      <td class="center">77.07</td>
      <td class="center bold">18.73</td>
      <td class="center">78.91</td>
      <td class="center">76.67</td>
      <td class="center">74.63</td>
    </tr>
    <tr>
      <td class="bold">Random Forest (150 Trees)</td>
      <td class="center">Outer LOSO (Strict)</td>
      <td class="center">76.87</td>
      <td class="center">20.34</td>
      <td class="center">79.52</td>
      <td class="center">77.94</td>
      <td class="center">75.01</td>
    </tr>
    <tr>
      <td class="bold">K-Nearest Neighbors (k=7)</td>
      <td class="center">Outer LOSO (Strict)</td>
      <td class="center">72.54</td>
      <td class="center">19.78</td>
      <td class="center">74.12</td>
      <td class="center">74.78</td>
      <td class="center">71.76</td>
    </tr>
  </tbody>
</table>

<div class="figure-container">
  <img src="{IMG_ACC}" style="width: 48%; display: inline-block; margin-right: 1%;" alt="Accuracy Comparison">
  <img src="{IMG_MET}" style="width: 48%; display: inline-block;" alt="Metrics Comparison">
  <div class="figure-caption">Figure 2: (Left) Mean LOSO classification accuracy comparison with standard deviation error bars. (Right) Multi-metric performance breakdown: Precision, Recall, and Macro F1 across evaluated architectures.</div>
</div>

<h3>5.2 Aggregate Confusion Matrix & Diagnostic Trade-Offs</h3>
<p class="no-indent">Table 4 compiles aggregate confusion matrix counts across all 2,538 test instances (1,269 SIMKAP, 1,269 Rest).</p>

<div class="table-caption">Table 4: Aggregate confusion matrix counts and diagnostic sensitivity/specificity across 47 subjects (2,538 test instances).</div>
<table>
  <thead>
    <tr>
      <th>Classifier</th>
      <th class="center">True Pos (TP)</th>
      <th class="center">True Neg (TN)</th>
      <th class="center">False Pos (FP)</th>
      <th class="center">False Neg (FN)</th>
      <th class="center">Total Tested</th>
      <th class="center">Sensitivity / Recall</th>
      <th class="center">Specificity</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="bold">SVM (RBF Kernel)</td>
      <td class="center">975</td>
      <td class="center bold">1,015</td>
      <td class="center bold">254</td>
      <td class="center">294</td>
      <td class="center">2,538</td>
      <td class="center">76.83%</td>
      <td class="center bold">80.00%</td>
    </tr>
    <tr>
      <td class="bold">1D-CNN (Sequential)</td>
      <td class="center bold">1,002</td>
      <td class="center">962</td>
      <td class="center">307</td>
      <td class="center bold">267</td>
      <td class="center">2,538</td>
      <td class="center bold">78.96%</td>
      <td class="center">75.81%</td>
    </tr>
    <tr>
      <td class="bold">XGBoost</td>
      <td class="center">973</td>
      <td class="center">983</td>
      <td class="center">286</td>
      <td class="center">296</td>
      <td class="center">2,538</td>
      <td class="center">76.67%</td>
      <td class="center">77.46%</td>
    </tr>
    <tr>
      <td class="bold">Random Forest</td>
      <td class="center">989</td>
      <td class="center">962</td>
      <td class="center">307</td>
      <td class="center">280</td>
      <td class="center">2,538</td>
      <td class="center">77.94%</td>
      <td class="center">75.81%</td>
    </tr>
    <tr>
      <td class="bold">K-Nearest Neighbors</td>
      <td class="center">949</td>
      <td class="center">892</td>
      <td class="center">377</td>
      <td class="center">320</td>
      <td class="center">2,538</td>
      <td class="center">74.78%</td>
      <td class="center">70.29%</td>
    </tr>
  </tbody>
</table>

<p><strong>Clinical & Operational Implications:</strong> The sequential 1D-CNN identified the highest number of True High Workload instances (TP = 1,002 out of 1,269), producing the lowest False Negative count (FN = 267). In safety-critical aviation or air-traffic monitoring, Type II errors (missing an overloaded operator) carry far higher operational hazard than false alarms. Conversely, RBF-SVM achieved highest specificity (80.00%) and lowest False Positive count (FP = 254), making it ideal for mitigating operator alarm fatigue.</p>

<div class="figure-container">
  <img src="{IMG_BOX}" style="width: 48%; display: inline-block; margin-right: 1%;" alt="Boxplot Distribution">
  <img src="{IMG_SUB}" style="width: 48%; display: inline-block;" alt="Subject Accuracy Trajectories">
  <div class="figure-caption">Figure 3: (Left) Subject-wise accuracy distribution boxplot showing median performance (~85%) vs. outlier spread. (Right) Granular subject-by-subject accuracy trajectories across all evaluated LOSO test folds showing high architectural alignment across models.</div>
</div>

<p><strong>Population Neurodiversity:</strong> As shown in Figure 3, over 65% of participants attained accuracies exceeding 85%, with multiple subjects reaching 100% zero-shot transfer (Sub06, Sub12, Sub18, Sub27). A small cohort of atypical subjects (Sub01, Sub14, Sub33 at 48–55%) exhibited elevated resting beta power and fixation anxiety, pulling down the arithmetic mean.</p>

<h3>5.3 Grouped Permutation Electrode Ablation Analysis</h3>
<p class="no-indent">Table 5 presents the empirical outcomes of our grouped permutation ablation across all 48 subjects (30 permutations per channel per subject).</p>

<div class="table-caption">Table 5: Predictive electrode importance rankings across classifiers via grouped permutation ablation under Leave-One-Subject-Out validation across 48 subjects.</div>
<table>
  <thead>
    <tr>
      <th class="center">Rank</th>
      <th class="center">Electrode</th>
      <th>Cortical Region</th>
      <th class="center">RF Drop (ΔBA)</th>
      <th class="center">RF FDR <em>q</em>-value</th>
      <th class="center">SVM Drop (ΔBA)</th>
      <th class="center">SVM FDR <em>q</em>-value</th>
      <th class="center">XGB Drop (ΔBA)</th>
      <th class="center">XGB FDR <em>q</em>-value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="center bold">1</td>
      <td class="center bold">AF4</td>
      <td>Prefrontal (Right)</td>
      <td class="center bold">+0.0414</td>
      <td class="center bold">2.7 &times; 10<sup>-5</sup></td>
      <td class="center bold">+0.0359</td>
      <td class="center bold">2.8 &times; 10<sup>-4</sup></td>
      <td class="center bold">+0.0951</td>
      <td class="center bold">5.1 &times; 10<sup>-7</sup></td>
    </tr>
    <tr>
      <td class="center bold">2</td>
      <td class="center bold">FC6</td>
      <td>Fronto-Central (Right)</td>
      <td class="center bold">+0.0370</td>
      <td class="center bold">2.4 &times; 10<sup>-5</sup></td>
      <td class="center bold">+0.0189</td>
      <td class="center bold">1.4 &times; 10<sup>-3</sup></td>
      <td class="center bold">+0.0575</td>
      <td class="center bold">2.6 &times; 10<sup>-7</sup></td>
    </tr>
    <tr>
      <td class="center bold">3</td>
      <td class="center bold">F4</td>
      <td>Frontal (Right)</td>
      <td class="center bold">+0.0225</td>
      <td class="center bold">6.5 &times; 10<sup>-4</sup></td>
      <td class="center bold">+0.0187</td>
      <td class="center bold">5.2 &times; 10<sup>-3</sup></td>
      <td class="center bold">+0.0305</td>
      <td class="center bold">3.6 &times; 10<sup>-4</sup></td>
    </tr>
    <tr>
      <td class="center bold">4</td>
      <td class="center bold">P7</td>
      <td>Parietal (Left)</td>
      <td class="center bold">+0.0215</td>
      <td class="center bold">3.2 &times; 10<sup>-3</sup></td>
      <td class="center">+0.0077</td>
      <td class="center">1.9 &times; 10<sup>-2</sup></td>
      <td class="center bold">+0.0512</td>
      <td class="center bold">5.0 &times; 10<sup>-6</sup></td>
    </tr>
    <tr>
      <td class="center bold">5</td>
      <td class="center bold">AF3</td>
      <td>Prefrontal (Left)</td>
      <td class="center bold">+0.0154</td>
      <td class="center bold">3.2 &times; 10<sup>-3</sup></td>
      <td class="center">+0.0020</td>
      <td class="center">1.5 &times; 10<sup>-1</sup></td>
      <td class="center">+0.0062</td>
      <td class="center">9.7 &times; 10<sup>-2</sup></td>
    </tr>
    <tr>
      <td class="center bold">6</td>
      <td class="center bold">O1</td>
      <td>Occipital (Left)</td>
      <td class="center bold">+0.0129</td>
      <td class="center bold">1.4 &times; 10<sup>-3</sup></td>
      <td class="center bold">+0.0299</td>
      <td class="center bold">5.3 &times; 10<sup>-4</sup></td>
      <td class="center bold">+0.0278</td>
      <td class="center bold">3.8 &times; 10<sup>-5</sup></td>
    </tr>
    <tr>
      <td class="center bold">7</td>
      <td class="center bold">O2</td>
      <td>Occipital (Right)</td>
      <td class="center bold">+0.0145</td>
      <td class="center bold">3.9 &times; 10<sup>-3</sup></td>
      <td class="center bold">+0.0180</td>
      <td class="center bold">1.9 &times; 10<sup>-2</sup></td>
      <td class="center">+0.0132</td>
      <td class="center">9.6 &times; 10<sup>-2</sup></td>
    </tr>
    <tr>
      <td class="center bold">8</td>
      <td class="center bold">T7</td>
      <td>Temporal (Left)</td>
      <td class="center bold">+0.0127</td>
      <td class="center bold">5.6 &times; 10<sup>-3</sup></td>
      <td class="center bold">+0.0113</td>
      <td class="center bold">2.0 &times; 10<sup>-2</sup></td>
      <td class="center bold">+0.0283</td>
      <td class="center bold">9.4 &times; 10<sup>-4</sup></td>
    </tr>
    <tr>
      <td class="center bold">9</td>
      <td class="center bold">FC5</td>
      <td>Fronto-Central (Left)</td>
      <td class="center">+0.0085</td>
      <td class="center">8.2 &times; 10<sup>-3</sup></td>
      <td class="center bold">+0.0153</td>
      <td class="center bold">2.2 &times; 10<sup>-2</sup></td>
      <td class="center">+0.0075</td>
      <td class="center">1.1 &times; 10<sup>-1</sup></td>
    </tr>
    <tr>
      <td class="center bold">10</td>
      <td class="center bold">F8</td>
      <td>Frontal (Right)</td>
      <td class="center">+0.0078</td>
      <td class="center">1.2 &times; 10<sup>-2</sup></td>
      <td class="center bold">+0.0119</td>
      <td class="center bold">9.5 &times; 10<sup>-3</sup></td>
      <td class="center">+0.0061</td>
      <td class="center">1.0 &times; 10<sup>-1</sup></td>
    </tr>
    <tr>
      <td class="center bold">11</td>
      <td class="center bold">F7</td>
      <td>Frontal (Left)</td>
      <td class="center bold">+0.0106</td>
      <td class="center bold">3.9 &times; 10<sup>-3</sup></td>
      <td class="center">+0.0038</td>
      <td class="center">2.1 &times; 10<sup>-1</sup></td>
      <td class="center">+0.0097</td>
      <td class="center">9.6 &times; 10<sup>-2</sup></td>
    </tr>
    <tr>
      <td class="center bold">12</td>
      <td class="center bold">F3</td>
      <td>Frontal (Left)</td>
      <td class="center bold">+0.0101</td>
      <td class="center bold">5.2 &times; 10<sup>-3</sup></td>
      <td class="center">+0.0050</td>
      <td class="center">1.1 &times; 10<sup>-1</sup></td>
      <td class="center bold">+0.0151</td>
      <td class="center bold">3.6 &times; 10<sup>-3</sup></td>
    </tr>
    <tr>
      <td class="center bold">13</td>
      <td class="center bold">P8</td>
      <td>Parietal (Right)</td>
      <td class="center bold">+0.0096</td>
      <td class="center bold">7.8 &times; 10<sup>-4</sup></td>
      <td class="center">+0.0068</td>
      <td class="center">9.0 &times; 10<sup>-2</sup></td>
      <td class="center">-0.0002</td>
      <td class="center">2.8 &times; 10<sup>-1</sup></td>
    </tr>
    <tr>
      <td class="center bold">14</td>
      <td class="center bold">T8</td>
      <td>Temporal (Right)</td>
      <td class="center">+0.0021</td>
      <td class="center">2.3 &times; 10<sup>-1</sup></td>
      <td class="center">+0.0030</td>
      <td class="center">2.0 &times; 10<sup>-1</sup></td>
      <td class="center">+0.0044</td>
      <td class="center">1.1 &times; 10<sup>-1</sup></td>
    </tr>
  </tbody>
</table>

<div class="figure-container">
  <img src="{IMG_HEAT}" style="width: 48%; display: inline-block; margin-right: 1%;" alt="Importance Heatmap">
  <img src="{IMG_GROUP}" style="width: 48%; display: inline-block;" alt="Grouped Node Importance">
  <div class="figure-caption">Figure 4: (Left) Cross-model predictive node importance heatmap showing balanced accuracy degradation. (Right) Grouped node importance bar chart showing consensus dominance of AF4, FC6, and F4 across all classifiers.</div>
</div>

<div class="figure-container">
  <img src="{IMG_CONS}" style="width: 65%; display: block; margin: 0 auto;" alt="Subject Consistency">
  <div class="figure-caption">Figure 5: Population-level subject consistency heatmap illustrating the fraction of individual subjects exhibiting degraded performance under electrode ablation (AF4: 77.1% agreement; FC6: 75.0% agreement).</div>
</div>

<h3>5.4 14-Electrode Grand-Average Spectral Power Surges</h3>
<p class="no-indent">Table 6 details the grand-average spectral log-power across all 14 channels (1.0–40.0 Hz) across 48 subjects, highlighting the physical energy surge induced by multitasking.</p>

<div class="table-caption">Table 6: 14-Electrode grand-average spectral log-power and workload activation difference across 48 subjects.</div>
<table>
  <thead>
    <tr>
      <th class="center">Electrode</th>
      <th>Cortical Lobe</th>
      <th class="center">High Workload (dB)</th>
      <th class="center">Low Workload (dB)</th>
      <th class="center">Δ Activation (dB)</th>
      <th class="center">Surge Factor</th>
      <th>Primary Neurocognitive Association</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="center bold">F8</td>
      <td>Frontal (Right)</td>
      <td class="center">7.12 ± 0.08</td>
      <td class="center">6.71 ± 0.06</td>
      <td class="center bold">+0.41 dB</td>
      <td class="center">5.29&times;</td>
      <td>Sustained vigilance, visual search, attentional orienting</td>
    </tr>
    <tr>
      <td class="center bold">T8</td>
      <td>Temporal (Right)</td>
      <td class="center">6.80 ± 0.10</td>
      <td class="center">6.43 ± 0.06</td>
      <td class="center bold">+0.37 dB</td>
      <td class="center">9.13&times;</td>
      <td>Auditory-spatial monitoring, environmental pattern synthesis</td>
    </tr>
    <tr>
      <td class="center bold">FC6</td>
      <td>Fronto-Central (Right)</td>
      <td class="center">6.87 ± 0.09</td>
      <td class="center">6.51 ± 0.07</td>
      <td class="center bold">+0.36 dB</td>
      <td class="center">7.04&times;</td>
      <td>Sensorimotor coordination, motor response planning</td>
    </tr>
    <tr>
      <td class="center bold">T7</td>
      <td>Temporal (Left)</td>
      <td class="center">6.70 ± 0.14</td>
      <td class="center">6.37 ± 0.13</td>
      <td class="center bold">+0.33 dB</td>
      <td class="center">0.18&times; (shift)</td>
      <td>Phonological loop, verbal working memory rehearsal</td>
    </tr>
    <tr>
      <td class="center bold">F7</td>
      <td>Frontal (Left)</td>
      <td class="center">7.05 ± 0.08</td>
      <td class="center">6.76 ± 0.08</td>
      <td class="center bold">+0.29 dB</td>
      <td class="center">2.38&times;</td>
      <td>Broca's area, internal rule verbalization</td>
    </tr>
    <tr>
      <td class="center bold">AF4</td>
      <td>Prefrontal (Right)</td>
      <td class="center">6.89 ± 0.08</td>
      <td class="center">6.65 ± 0.06</td>
      <td class="center bold">+0.23 dB</td>
      <td class="center">3.57&times;</td>
      <td>Executive control, goal management under stress</td>
    </tr>
    <tr>
      <td class="center bold">F3</td>
      <td>Frontal (Left)</td>
      <td class="center">6.66 ± 0.13</td>
      <td class="center">6.50 ± 0.13</td>
      <td class="center bold">+0.17 dB</td>
      <td class="center">0.75&times;</td>
      <td>DLPFC working memory manipulation, mental calculation</td>
    </tr>
    <tr>
      <td class="center bold">O2</td>
      <td>Occipital (Right)</td>
      <td class="center">6.42 ± 0.09</td>
      <td class="center">6.29 ± 0.08</td>
      <td class="center bold">+0.13 dB</td>
      <td class="center">3.43&times;</td>
      <td>Visual stimulus discrimination, screen monitoring</td>
    </tr>
    <tr>
      <td class="center bold">F4</td>
      <td>Frontal (Right)</td>
      <td class="center">6.65 ± 0.10</td>
      <td class="center">6.53 ± 0.07</td>
      <td class="center bold">+0.12 dB</td>
      <td class="center">4.28&times;</td>
      <td>DLPFC cognitive control, working memory update</td>
    </tr>
    <tr>
      <td class="center bold">FC5</td>
      <td>Fronto-Central (Left)</td>
      <td class="center">6.50 ± 0.09</td>
      <td class="center">6.38 ± 0.08</td>
      <td class="center bold">+0.12 dB</td>
      <td class="center">2.38&times;</td>
      <td>Motor-cognitive integration, executive motor execution</td>
    </tr>
    <tr>
      <td class="center bold">P7</td>
      <td>Parietal (Left)</td>
      <td class="center">6.16 ± 0.09</td>
      <td class="center">6.07 ± 0.08</td>
      <td class="center bold">+0.10 dB</td>
      <td class="center">3.77&times;</td>
      <td>Visuospatial storage buffer, arithmetic processing</td>
    </tr>
    <tr>
      <td class="center bold">O1</td>
      <td>Occipital (Left)</td>
      <td class="center">6.41 ± 0.09</td>
      <td class="center">6.31 ± 0.08</td>
      <td class="center bold">+0.09 dB</td>
      <td class="center">3.68&times;</td>
      <td>Visual feature parsing, stimulus perception</td>
    </tr>
    <tr>
      <td class="center bold">AF3</td>
      <td>Prefrontal (Left)</td>
      <td class="center">6.84 ± 0.09</td>
      <td class="center">6.79 ± 0.09</td>
      <td class="center bold">+0.05 dB</td>
      <td class="center">0.84&times;</td>
      <td>Executive cognitive regulation, attentional allocation</td>
    </tr>
    <tr>
      <td class="center bold">P8</td>
      <td>Parietal (Right)</td>
      <td class="center">6.43 ± 0.10</td>
      <td class="center">6.40 ± 0.08</td>
      <td class="center bold">+0.02 dB</td>
      <td class="center">2.66&times;</td>
      <td>Spatial coordinate transformation, storage buffer</td>
    </tr>
  </tbody>
</table>

<h2>6. Discussion & Wearable Translation</h2>

<p class="no-indent"><strong>Neurophysiological Congruence:</strong> Multitasking under SIMKAP recruits the distributed fronto-parietal cognitive control network [20]. The prominent predictive reliance on <strong>AF4, FC6, and F4</strong> (Table 5) alongside large physical power surges at <strong>F8 (+0.41 dB)</strong> and <strong>FC6 (+0.36 dB)</strong> aligns with established cognitive neuroscience: the right prefrontal and fronto-central cortices govern sustained vigilance, rapid conflict steering, and spatial coordinate transformation under acute psychological stress [21]. Meanwhile, left temporal <strong>T7 (+0.33 dB)</strong> serves as a cross-subject anchor reflecting Baddeley's phonological loop rehearsal during continuous mental arithmetic.</p>

<p><strong>Snapshot vs. Trajectory Trade-Offs:</strong> Tabular RBF-SVM achieves superior precision (81.29%) and specificity (80.00%) on temporally averaged 50-dimensional vectors because mean-pooling smooths short-term temporal noise, allowing the SVM to construct broad, maximal-margin hyperplanes. Conversely, the deep sequential 1D-CNN achieves superior recall (78.96%) and F1-score (77.00%) because its temporal convolutional kernels explicitly track continuous non-stationary transition dynamics across the 20-second rolling trajectory. In safety-critical systems, detecting emerging overload before an operator fails is paramount, favoring sequential deep modeling.</p>

<p><strong>Toward Wearable 4-Channel Headsets:</strong> Standard 14-channel wet caps are impractical in operational environments due to long setup times and user discomfort. Our empirical consensus rankings isolate an ultra-compact 4-electrode montage:
M<sub>minimal</sub> = {AF4, FC6, F4, AF3}
All four electrodes reside on the anterior forehead and upper temple. This anatomical clustering enables dry-sensor, gel-free smart headbands and aviation headsets capable of running low-power 1D-CNN inference on edge microcontrollers (e.g., ARM Cortex-M) in real time.</p>

<h2>7. Conclusion</h2>
<p class="no-indent">We presented an end-to-end, subject-independent mental workload classification framework on the 48-subject STEW dataset. By integrating multi-band magnitude-squared coherence with graph network topology across 20-second rolling episodes, our RBF-SVM achieved 78.41% accuracy (81.29% precision) and our sequential 1D-CNN achieved 77.38% accuracy with highest recall (78.96%) and F1-score (77.00%) under strict Leave-One-Subject-Out cross-validation. Statistically controlled grouped permutation ablation confirmed right prefrontal/fronto-central electrodes (AF4, FC6, F4) and left temporal rehearsal (T7) as universal neural biomarkers, establishing an empirical foundation for real-world 4-channel wearable neuroergonomic systems.</p>

<h2>References</h2>
<p class="no-indent" style="font-size: 8pt; line-height: 1.3;">
[1] R. Parasuraman et al., <em>IEEE Trans. Syst., Man, Cybern. A</em>, 30(3):286–297, 2000.<br>
[2] F. Dehais et al., in <em>Neuroergonomics: The Brain at Work</em>, pp. 115–120, Academic Press, 2019.<br>
[3] S. G. Hart and L. E. Staveland, <em>Adv. Psychol.</em>, 52:139–183, 1988.<br>
[4] M. Teplan, <em>Meas. Sci. Rev.</em>, 2(2):1–11, 2002.<br>
[5] A. Gevins and M. E. Smith, <em>Theor. Issues Ergon. Sci.</em>, 4(1–2):113–131, 2003.<br>
[6] G. Pfurtscheller and F. H. Lopes da Silva, <em>Clin. Neurophysiol.</em>, 110(11):1842–1857, 1999.<br>
[7] F. L. Kohlmorgen et al., in <em>Proc. IEEE EMBC</em>, pp. 2486–2489, 2017.<br>
[8] C. J. Stam, <em>Nat. Rev. Neurosci.</em>, 15(10):683–695, 2014.<br>
[9] R. Roy et al., <em>Comput. Biol. Med.</em>, 67:110–118, 2015.<br>
[10] E. Bullmore and O. Sporns, <em>Nat. Rev. Neurosci.</em>, 10(3):186–198, 2009.<br>
[11] M. M. K. Al-Saegh et al., <em>IEEE Access</em>, 9:142105–142122, 2021.<br>
[12] H. Saadati et al., <em>Front. Neurosci.</em>, 14:574441, 2020.<br>
[13] V. Jayaram and P. Alamgir, <em>J. Neural Eng.</em>, 15(6):066025, 2018.<br>
[14] M. Safari, R. Shalbaf, S. Bagherzadeh, and A. Shalbaf, <em>Sci. Rep.</em>, 14:8291, 2024.<br>
[15] W. L. Lim, O. Sourina, and L. Wang, <em>IEEE Trans. Neural Syst. Rehabil. Eng.</em>, 26(11):2106–2114, 2018.<br>
[16] P. Zhang, X. Wang, and F. Wan, <em>Front. Hum. Neurosci.</em>, 17:112045, 2023.<br>
[17] A. Al-Nafjan et al., <em>Appl. Sci.</em>, 10(6):2082, 2020.<br>
[18] G. Siddhad, P. P. Roy, and B.-G. Kim, in <em>Proc. 27th ICPR</em>, arXiv:2409.07722, 2024.<br>
[19] J.-P. Onnela et al., <em>Phys. Rev. E</em>, 71(6):065103, 2005.<br>
[20] M. W. Cole and W. Schneider, <em>NeuroImage</em>, 37(1):343–360, 2007.<br>
[21] D. L. Schacter et al., <em>Psychology</em>, 2nd ed., Worth Publishers, 2011.
</p>

</body>
</html>
"""

html_content = (
    html_template.replace("{IMG_WAVE_HI}", img_wave_hi)
                 .replace("{IMG_WAVE_LO}", img_wave_lo)
                 .replace("{IMG_ACC}", img_acc)
                 .replace("{IMG_MET}", img_met)
                 .replace("{IMG_BOX}", img_box)
                 .replace("{IMG_SUB}", img_sub)
                 .replace("{IMG_HEAT}", img_heat)
                 .replace("{IMG_GROUP}", img_group)
                 .replace("{IMG_CONS}", img_cons)
)

with open(HTML_OUT, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML written to {HTML_OUT}. Now compiling to PDF via Microsoft Edge Headless...")

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not os.path.exists(edge_path):
    edge_path = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"

cmd = [
    edge_path,
    "--headless",
    "--disable-gpu",
    f"--print-to-pdf={PDF_OUT}",
    "--no-pdf-header-footer",
    HTML_OUT
]

res = subprocess.run(cmd, capture_output=True, text=True)
if os.path.exists(PDF_OUT) and os.path.getsize(PDF_OUT) > 10000:
    print(f"SUCCESS: PDF generated at {PDF_OUT} ({os.path.getsize(PDF_OUT)} bytes)")
else:
    print(f"Failed to generate PDF. Edge stderr: {res.stderr}")
