PREDICTIVE EEG ELECTRODE IMPORTANCE — INTERPRETATION
=====================================================

Subjects evaluated: 48
Recordings loaded: 96
Sequence length: 4 windows = 20 seconds
Permutations per electrode per subject: 30
Validation: outer Leave-One-Subject-Out (LOSO)

Feature ordering reconstructed from feature_extraction.py:
Each band contains 91 coherence features, 1 global average shortest-path feature, and 28 node-specific graph features.
Five bands produce 600 features per window.
Each electrode group contains 65 incident coherence features and 10 node-specific graph features, for 75 total.
The global average-shortest-path features are not assigned to individual electrodes.

Importance definition:
Importance = baseline held-out-subject balanced accuracy minus balanced accuracy after grouped electrode-feature permutation.

Interpretation and limitations:
- Positive importance means shuffling the electrode group reduced balanced accuracy.
- Negative importance means shuffling improved balanced accuracy for that held-out subject.
- Electrode groups overlap because each coherence edge belongs to both endpoint electrodes; importance values are not additive.
- Importance measures model predictive reliance, not causality or neural activation.
- The four-window sequences overlap in time. Statistical summaries are computed across held-out subjects, not treating sequences as independent subjects.
- Models use fixed hyperparameters. A final publication study should use nested subject-wise validation for model selection.
- CNN training uses a fixed epoch count and no validation-based early stopping in this implementation.
- This script does not perform reduced-electrode montage retraining. Importance rankings alone do not prove that fewer electrodes preserve classification performance.
- The source feature extractor uses its own filtering and graph-distance choices. Report those preprocessing choices accurately and assess alternative graph-distance definitions as a separate analysis.
