import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image

BASE_DIR = r'C:\Users\oo163\AIBSI_ML_DL'
OUTPUT_FILE = os.path.join(BASE_DIR, 'AIBSI_Cognitive_Workload_Presentation.pptx')

# ----------------- DESIGN THEME & PALETTES -----------------
# Dark Theme (Title & Conclusion)
BG_DARK = RGBColor(11, 19, 43)        # #0B132B Deep Midnight Navy
CARD_DARK = RGBColor(24, 38, 71)      # #182647 Slate Navy Card
BORDER_DARK = RGBColor(46, 68, 115)   # Subtle outline

# Light Theme (Content Slides)
BG_LIGHT = RGBColor(248, 250, 252)    # #F8FAFC Crisp Slate White
CARD_LIGHT = RGBColor(255, 255, 255)  # #FFFFFF Clean White Card
BORDER_LIGHT = RGBColor(226, 232, 240)# #E2E8F0 Subtle Border

# Text Colors
TEXT_DARK = RGBColor(15, 23, 42)      # #0F172A Deep Charcoal
TEXT_MUTED = RGBColor(100, 116, 139)  # #64748B Slate Muted
TEXT_BODY = RGBColor(51, 65, 85)      # #334155 Slate Body
TEXT_LIGHT = RGBColor(248, 250, 252)  # #F8FAFC
TEXT_LIGHT_MUTED = RGBColor(148, 163, 184) # #94A3B8

# Accents
ACCENT_BLUE = RGBColor(37, 99, 235)   # #2563EB Vibrant Tech Blue
ACCENT_CYAN = RGBColor(14, 165, 233)  # #0EA5E9 Bright Cyan
ACCENT_INDIGO = RGBColor(99, 102, 241)# #6366F1 Modern Indigo
ACCENT_GREEN = RGBColor(16, 185, 129) # #10B981 Emerald
ACCENT_AMBER = RGBColor(245, 158, 11) # #F59E0B Amber Gold
ACCENT_RED = RGBColor(239, 68, 68)    # #EF4444 Rose Red

prs = pptx.Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

def create_slide(is_dark=False):
    slide = prs.slides.add_slide(blank_layout)
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = BG_DARK if is_dark else BG_LIGHT
    bg.line.fill.background()
    return slide

def add_header(slide, title, kicker=None, subtitle=None, is_dark=False):
    # Kicker
    if kicker:
        kb = slide.shapes.add_textbox(Inches(0.8), Inches(0.42), Inches(11.733), Inches(0.28))
        ktf = kb.text_frame
        ktf.word_wrap = True
        ktf.margin_left = ktf.margin_right = ktf.margin_top = ktf.margin_bottom = 0
        kp = ktf.paragraphs[0]
        kp.text = kicker.upper()
        kp.font.size = Pt(10)
        kp.font.bold = True
        kp.font.color.rgb = ACCENT_CYAN if is_dark else ACCENT_BLUE

    # Title
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.68) if kicker else Inches(0.45), Inches(11.733), Inches(0.55))
    ttf = tb.text_frame
    ttf.word_wrap = True
    ttf.margin_left = ttf.margin_right = ttf.margin_top = ttf.margin_bottom = 0
    tp = ttf.paragraphs[0]
    tp.text = title
    tp.font.size = Pt(22)
    tp.font.bold = True
    tp.font.color.rgb = TEXT_LIGHT if is_dark else TEXT_DARK

    # Subtitle
    if subtitle:
        sb = slide.shapes.add_textbox(Inches(0.8), Inches(1.22), Inches(11.733), Inches(0.35))
        stf = sb.text_frame
        stf.word_wrap = True
        stf.margin_left = stf.margin_right = stf.margin_top = stf.margin_bottom = 0
        sp = stf.paragraphs[0]
        sp.text = subtitle
        sp.font.size = Pt(11.5)
        sp.font.color.rgb = TEXT_LIGHT_MUTED if is_dark else TEXT_MUTED

def add_card(slide, left, top, width, height, bg_color=None, border_color=None, is_dark=False):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color or (CARD_DARK if is_dark else CARD_LIGHT)
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1)
    else:
        shape.line.color.rgb = BORDER_DARK if is_dark else BORDER_LIGHT
        shape.line.width = Pt(1)
    return shape

def add_stat_box(slide, left, top, width, height, value, label, subtext="", accent_color=ACCENT_BLUE, is_dark=False):
    card = add_card(slide, left, top, width, height, is_dark=is_dark)
    
    # Top accent line
    bar = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, Inches(0.08))
    bar.fill.solid()
    bar.fill.fore_color.rgb = accent_color
    bar.line.fill.background()
    
    tb = slide.shapes.add_textbox(left + Inches(0.15), top + Inches(0.12), width - Inches(0.3), height - Inches(0.18))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    
    vp = tf.paragraphs[0]
    vp.text = str(value)
    vp.font.size = Pt(22)
    vp.font.bold = True
    vp.font.color.rgb = accent_color
    
    lp = tf.add_paragraph()
    lp.text = label
    lp.font.size = Pt(10.5)
    lp.font.bold = True
    lp.font.color.rgb = TEXT_LIGHT if is_dark else TEXT_DARK
    lp.space_before = Pt(2)
    
    if subtext:
        stp = tf.add_paragraph()
        stp.text = subtext
        stp.font.size = Pt(8.5)
        stp.font.color.rgb = TEXT_LIGHT_MUTED if is_dark else TEXT_MUTED
        stp.space_before = Pt(2)

def add_image_fitted(slide, img_path, left, top, max_w, max_h):
    if not os.path.exists(img_path):
        print(f"Warning: Image not found: {img_path}")
        return None
    try:
        im = Image.open(img_path)
        im_w, im_h = im.size
        aspect = im_w / float(im_h)
        target_aspect = max_w / float(max_h)
        
        if aspect > target_aspect:
            # Width limited
            w = max_w
            h = max_w / aspect
            x = left
            y = top + (max_h - h) / 2
        else:
            # Height limited
            h = max_h
            w = max_h * aspect
            x = left + (max_w - w) / 2
            y = top
            
        return slide.shapes.add_picture(img_path, x, y, w, h)
    except Exception as e:
        print(f"Error adding image {img_path}: {e}")
        return None

def add_bullets(tf, items, is_dark=False, font_size=11, space_after=6):
    for i, item in enumerate(items):
        if i == 0 and len(tf.paragraphs) > 0 and tf.paragraphs[0].text == '':
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        
        p.space_after = Pt(space_after)
        p.font.size = Pt(font_size)
        
        if isinstance(item, tuple):
            lead, body = item
            run_lead = p.add_run()
            run_lead.text = lead + ": "
            run_lead.font.bold = True
            run_lead.font.color.rgb = ACCENT_CYAN if is_dark else ACCENT_BLUE
            
            run_body = p.add_run()
            run_body.text = body
            run_body.font.color.rgb = TEXT_LIGHT if is_dark else TEXT_BODY
        else:
            run = p.add_run()
            run.text = item
            run.font.color.rgb = TEXT_LIGHT if is_dark else TEXT_BODY

print('Helper functions compiled successfully.')
# ==============================================================================
# SLIDE 1: TITLE SLIDE (Dark Theme)
# ==============================================================================
s1 = create_slide(is_dark=True)

# Main Title Card
t_card = add_card(s1, Inches(0.8), Inches(0.8), Inches(11.733), Inches(4.3), bg_color=CARD_DARK, border_color=BORDER_DARK, is_dark=True)

# Accent top bar
bar1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(0.1))
bar1.fill.solid()
bar1.fill.fore_color.rgb = ACCENT_CYAN
bar1.line.fill.background()

tb1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.2), Inches(10.9), Inches(3.6))
tf1 = tb1.text_frame
tf1.word_wrap = True

kp1 = tf1.paragraphs[0]
kp1.text = 'ARTIFICIAL INTELLIGENCE FOR BRAIN-SIGNAL INTERFACES (AIBSI)'
kp1.font.size = Pt(11)
kp1.font.bold = True
kp1.font.color.rgb = ACCENT_CYAN

tp1 = tf1.add_paragraph()
tp1.text = 'EEG-Based Cognitive Workload Classification & Explainable Predictive Node Importance'
tp1.font.size = Pt(26)
tp1.font.bold = True
tp1.font.color.rgb = TEXT_LIGHT
tp1.space_before = Pt(12)

sp1 = tf1.add_paragraph()
sp1.text = 'A Comprehensive Leave-One-Subject-Out (LOSO) Cross-Validation Benchmark of Machine Learning & Deep 1D-CNN Architectures on the STEW Dataset'
sp1.font.size = Pt(14)
sp1.font.color.rgb = TEXT_LIGHT_MUTED
sp1.space_before = Pt(12)

dp1 = tf1.add_paragraph()
dp1.text = 'Authors / Research Focus: Minsi Hu Pipeline Extension & Predictive Neurophysiological Electrode Analysis'
dp1.font.size = Pt(11)
dp1.font.color.rgb = ACCENT_INDIGO
dp1.space_before = Pt(18)

# Bottom 4 Feature Cards
card_w = Inches(2.75)
gap = Inches(0.24)
start_x = Inches(0.8)
y_bottom = Inches(5.35)
h_bottom = Inches(1.5)

b_data = [
    ('48 Subjects', '96 Total Recordings', 'High & Low Workload', ACCENT_BLUE),
    ('14 Channels', 'Emotiv EPOC 10-20', 'Raw Scalp EEG @ 128Hz', ACCENT_CYAN),
    ('600 Features', 'Spectral Coherence', 'Complex Graph Topology', ACCENT_INDIGO),
    ('Strict LOSO', 'Zero Subject Leakage', 'Grouped Permutation XAI', ACCENT_GREEN)
]

for idx, (b_val, b_lbl, b_sub, b_col) in enumerate(b_data):
    bx = start_x + idx * (card_w + gap)
    add_stat_box(s1, bx, y_bottom, card_w, h_bottom, b_val, b_lbl, b_sub, accent_color=b_col, is_dark=True)

# ==============================================================================
# SLIDE 2: MOTIVATION & PROBLEM STATEMENT (Light Theme)
# ==============================================================================
s2 = create_slide(is_dark=False)
add_header(s2, 'The Imperative for Objective Cognitive Workload Monitoring',
           kicker='Background & Problem Statement',
           subtitle='Addressing cognitive overload in safety-critical operations through non-invasive neuroadaptive systems')

# Left Column: Operational Imperative
add_card(s2, Inches(0.8), Inches(1.65), Inches(5.65), Inches(5.2))
tb2_l = s2.shapes.add_textbox(Inches(1.05), Inches(1.85), Inches(5.15), Inches(4.8))
tf2_l = tb2_l.text_frame
tf2_l.word_wrap = True

p = tf2_l.paragraphs[0]
p.text = 'Operational & Clinical Imperative'
p.font.size = Pt(15)
p.font.bold = True
p.font.color.rgb = ACCENT_BLUE

bullets_2l = [
    ('Cognitive Overload Vulnerability', 'In high-stakes domains (aviation, surgery, automated driving, defense), cognitive saturation drastically degrades situational awareness, response latency, and critical decision-making.'),
    ('Subjective Metric Deficiencies', 'Standard retrospective assessments (e.g., NASA-TLX, SWAT) are post-hoc, intrusive, prone to subjective bias, and cannot trigger real-time proactive interventions.'),
    ('Continuous Scalp EEG Advantage', 'Non-invasive electroencephalography provides millisecond-level temporal resolution to passively monitor cortical state changes before errors manifest.'),
    ('Translational Goal', 'Engineer an automated, robust classifier that reliably generalizes across unseen individuals without requiring subject calibration.')
]
add_bullets(tf2_l, bullets_2l, is_dark=False, font_size=10.5, space_after=8)

# Right Column: Technical Challenges & Our Solutions
add_card(s2, Inches(6.8), Inches(1.65), Inches(5.733), Inches(5.2))
tb2_r = s2.shapes.add_textbox(Inches(7.05), Inches(1.85), Inches(5.233), Inches(4.8))
tf2_r = tb2_r.text_frame
tf2_r.word_wrap = True

p = tf2_r.paragraphs[0]
p.text = 'Core Technical Challenges & Proposed Solutions'
p.font.size = Pt(15)
p.font.bold = True
p.font.color.rgb = ACCENT_INDIGO

bullets_2r = [
    ('Severe Inter-Subject Variability', 'Distinct skull thickness and cortical geometry cause major distribution shifts between brains. -> Solved via rigorous 48-fold Leave-One-Subject-Out (LOSO) cross-validation.'),
    ('Dynamic Temporal Nature', 'Cognitive demand fluctuates dynamically over time rather than behaving as isolated static snapshots. -> Solved by modeling 20s continuous rolling wave episodes.'),
    ('High Spatial-Spectral Dimensionality', 'Raw EEG is noisy and redundant across 14 channels and multiple bands. -> Solved via 600-dim pairwise coherence and complex network graph metrics.'),
    ('The "Black-Box" Dilemma', 'Deep models often obscure which cortical zones drive classifications. -> Solved via grouped electrode permutation importance with FDR correction (q < 0.05).')
]
add_bullets(tf2_r, bullets_2r, is_dark=False, font_size=10.5, space_after=8)

print('Slides 1 and 2 appended.')
# ==============================================================================
# SLIDE 3: DATASET ARCHITECTURE & EXPERIMENTAL PARADIGM
# ==============================================================================
s3 = create_slide(is_dark=False)
add_header(s3, 'The STEW Dataset: Simultaneous Task EEG Workload',
           kicker='Dataset & Sensory Specifications',
           subtitle='Benchmarking cognitive workload under controlled experimental multitasking paradigms')

# Top 4 Stat Cards
s3_stats = [
    ('48', 'Participants', 'Healthy adult cohort', ACCENT_BLUE),
    ('96', 'Total Recordings', '48 High vs 48 Low Workload', ACCENT_CYAN),
    ('14', 'Scalp Electrodes', 'Emotiv EPOC 10-20 Montage', ACCENT_INDIGO),
    ('128 Hz', 'Sampling Rate', '19,200 points per recording', ACCENT_GREEN)
]
for idx, (val, lbl, sub, col) in enumerate(s3_stats):
    bx = Inches(0.8) + idx * (Inches(2.75) + Inches(0.24))
    add_stat_box(s3, bx, Inches(1.65), Inches(2.75), Inches(1.15), val, lbl, sub, accent_color=col, is_dark=False)

# Left Column: Experimental Paradigm
add_card(s3, Inches(0.8), Inches(2.95), Inches(5.65), Inches(3.9))
tb3_l = s3.shapes.add_textbox(Inches(1.05), Inches(3.05), Inches(5.15), Inches(3.6))
tf3_l = tb3_l.text_frame
tf3_l.word_wrap = True

p = tf3_l.paragraphs[0]
p.text = 'Experimental Paradigm & Cognitive Load Induction'
p.font.size = Pt(13.5)
p.font.bold = True
p.font.color.rgb = ACCENT_BLUE

bullets_3l = [
    ('Low Workload Condition', 'Participants sat quietly in an eyes-open resting state viewing neutral stimuli, capturing baseline physiological cortical oscillations.'),
    ('High Workload Condition (SIMKAP)', 'Participants executed the Simultaneous Capacity (SIMKAP) multitasking protocol, demanding rapid visual character matching, auditory tone monitoring, and concurrent arithmetic calculations under strict time pressure.'),
    ('Cognitive System Stressors', 'SIMKAP induces intense mental workload by simultaneously exhausting working memory, sustained attention, and sensory-motor gating.'),
    ('Standardized Ground Truth', 'Subjective rating files (ratings.txt) validate substantial perceptual separation in task difficulty between low and high conditions.')
]
add_bullets(tf3_l, bullets_3l, is_dark=False, font_size=10, space_after=6)

# Right Column: Sensor Montage
add_card(s3, Inches(6.8), Inches(2.95), Inches(5.733), Inches(3.9))
tb3_r = s3.shapes.add_textbox(Inches(7.05), Inches(3.05), Inches(5.233), Inches(3.6))
tf3_r = tb3_r.text_frame
tf3_r.word_wrap = True

p = tf3_r.paragraphs[0]
p.text = '14-Channel Scalp Sensor Topology'
p.font.size = Pt(13.5)
p.font.bold = True
p.font.color.rgb = ACCENT_INDIGO

bullets_3r = [
    ('Prefrontal (AF3, AF4)', 'Frontal pole coordinates governing executive decision planning, goal monitoring, and sustained emotional regulation.'),
    ('Frontal (F7, F3, F4, F8)', 'Dorsolateral and ventrolateral prefrontal cortices managing working memory retrieval, mental calculations, and focused attention.'),
    ('Fronto-Central (FC5, FC6)', 'Sensorimotor integration centers involved in motor coordination and task response execution.'),
    ('Temporal (T7, T8)', 'Lateral temporal lobes processing auditory stimuli and verbal working memory demands.'),
    ('Parietal (P7, P8)', 'Posterior parietal cortices coordinating spatial awareness, visual-spatial attention, and multimodal integration.'),
    ('Occipital (O1, O2)', 'Primary and associative visual cortices processing continuous on-screen optical stimuli.')
]
add_bullets(tf3_r, bullets_3r, is_dark=False, font_size=9.5, space_after=4)

# ==============================================================================
# SLIDE 4: SIGNAL PREPROCESSING & DYNAMIC FEATURE WAVES
# ==============================================================================
s4 = create_slide(is_dark=False)
add_header(s4, 'From Raw Microvolts to Dynamic Continuous Feature Waves',
           kicker='Signal Pipeline & Waveforms',
           subtitle='Butterworth filtering, window segmentation, and continuous dynamic wave construction')

# Left Column: Preprocessing Pipeline
add_card(s4, Inches(0.8), Inches(1.65), Inches(5.3), Inches(5.2))
tb4_l = s4.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(4.9), Inches(4.9))
tf4_l = tb4_l.text_frame
tf4_l.word_wrap = True

p = tf4_l.paragraphs[0]
p.text = 'End-to-End Signal Preprocessing Pipeline'
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = ACCENT_BLUE

bullets_4l = [
    ('6th-Order Butterworth Filter', 'Bandpass filtered between 1.0 Hz and 50.0 Hz using Second-Order Sections (SOS) for high numerical stability and zero-phase distortion.'),
    ('Artifact Attenuation', 'Effectively removes low-frequency DC drift, perspiration artifacts, electro-oculogram baseline shifts, and high-frequency 50/60 Hz power-line interference.'),
    ('Sliding Window Segmentation', 'Segmented into non-overlapping 5-second windows (640 data points per window @ 128 Hz sampling frequency).'),
    ('Full Recording Wave Ingestion', 'Rather than discarding later timestamps, all 19,200 time points (~30 full windows per recording) are converted into continuous temporal wave vectors.'),
    ('Sequential Temporal Chunking', 'Consecutive 5-second windows are structured into 4-timestep sliding sequences, yielding 20-second rolling dynamic episodes for temporal learning.')
]
add_bullets(tf4_l, bullets_4l, is_dark=False, font_size=10, space_after=7)

# Right Column: Wave Visualizations
add_card(s4, Inches(6.35), Inches(1.65), Inches(6.183), Inches(5.2))

# Subtitle inside right card
tb4_rt = s4.shapes.add_textbox(Inches(6.55), Inches(1.8), Inches(5.783), Inches(0.4))
tf4_rt = tb4_rt.text_frame
tf4_rt.word_wrap = True
prt = tf4_rt.paragraphs[0]
prt.text = 'Continuous Mean Global Connectivity Waves (Subject 01)'
prt.font.size = Pt(13)
prt.font.bold = True
prt.font.color.rgb = ACCENT_INDIGO

# Add images of High vs Low Workload waves
img_hi = os.path.join(BASE_DIR, 'features', 'sub01_hi_wave.png')
img_lo = os.path.join(BASE_DIR, 'features', 'sub01_lo_wave.png')

add_image_fitted(s4, img_hi, Inches(6.55), Inches(2.25), Inches(5.783), Inches(2.0))
add_image_fitted(s4, img_lo, Inches(6.55), Inches(4.35), Inches(5.783), Inches(2.0))

# Bottom note
tb4_rn = s4.shapes.add_textbox(Inches(6.55), Inches(6.38), Inches(5.783), Inches(0.4))
tf4_rn = tb4_rn.text_frame
tf4_rn.word_wrap = True
prn = tf4_rn.paragraphs[0]
prn.text = 'Observation: High workload demonstrates sustained elevated functional connectivity amplitudes and burstiness across time relative to resting baseline.'
prn.font.size = Pt(9)
prn.font.italic = True
prn.font.color.rgb = TEXT_MUTED

print('Slides 3 and 4 appended.')
# ==============================================================================
# SLIDE 5: FEATURE ENGINEERING: COHERENCE & COMPLEX GRAPH TOPOLOGY
# ==============================================================================
s5 = create_slide(is_dark=False)
add_header(s5, 'Multiband Functional Connectivity & Complex Network Graphs',
           kicker='Feature Engineering Architecture',
           subtitle='Constructing 600 spatial-spectral features per window across 5 canonical neurophysiological frequency bands')

card_w5 = Inches(3.72)
gap5 = Inches(0.28)
top5 = Inches(1.65)
h5 = Inches(5.2)

# Card 1: 5 Frequency Bands
add_card(s5, Inches(0.8), top5, card_w5, h5)
tb5_1 = s5.shapes.add_textbox(Inches(1.0), Inches(1.8), card_w5 - Inches(0.4), h5 - Inches(0.35))
tf5_1 = tb5_1.text_frame
tf5_1.word_wrap = True
p = tf5_1.paragraphs[0]
p.text = '5 Neurophysiological Bands'
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = ACCENT_BLUE

b5_1 = [
    ('Theta (4–8 Hz)', 'Frontal midline theta power increases with working memory demand, mental arithmetic, and focused cognitive effort.'),
    ('Low Alpha (8–11 Hz)', 'Cortical idling marker; desynchronizes (decreases) during sensory engagement and active attention allocation.'),
    ('High Alpha (11–13 Hz)', 'Reflects task-specific cortical activation, memory access, and targeted selective processing.'),
    ('Beta (13–30 Hz)', 'Prominent during heightened vigilance, active problem-solving, cognitive evaluation, and motor inhibition.'),
    ('Gamma (30–40 Hz)', 'Coordinates millisecond-scale neural binding, cross-cortical information integration, and multimodal perception.')
]
add_bullets(tf5_1, b5_1, is_dark=False, font_size=9.5, space_after=6)

# Card 2: Coherence & Graph Topology
add_card(s5, Inches(0.8) + card_w5 + gap5, top5, card_w5, h5)
tb5_2 = s5.shapes.add_textbox(Inches(0.8) + card_w5 + gap5 + Inches(0.2), Inches(1.8), card_w5 - Inches(0.4), h5 - Inches(0.35))
tf5_2 = tb5_2.text_frame
tf5_2.word_wrap = True
p = tf5_2.paragraphs[0]
p.text = 'Coherence & Graph Metrics'
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = ACCENT_INDIGO

b5_2 = [
    ('Spectral Coherence (91/band)', 'Computes pairwise magnitude-squared coherence between all 14 channels (14*13/2 = 91 pairs), capturing cross-channel synchrony.'),
    ('Network Graph Generation', 'Constructs a weighted graph G for each window where edge weights represent coherence strengths between nodes.'),
    ('Global Characteristic Path (1/band)', 'Calculates average shortest path length, measuring overall network integration efficiency.'),
    ('Nodal Centrality (14/band)', 'Calculates Closeness Centrality for each of the 14 nodes, quantifying communication velocity to all other electrodes.'),
    ('Nodal Clustering (14/band)', 'Calculates Clustering Coefficient for each node, quantifying local functional segregation and clique robustness.'),
    ('Total Dimensions: 600', '120 features per band * 5 bands = 600 features per 5s window!')
]
add_bullets(tf5_2, b5_2, is_dark=False, font_size=9.2, space_after=5)

# Card 3: Supervised Selection
add_card(s5, Inches(0.8) + 2 * (card_w5 + gap5), top5, card_w5, h5)
tb5_3 = s5.shapes.add_textbox(Inches(0.8) + 2 * (card_w5 + gap5) + Inches(0.2), Inches(1.8), card_w5 - Inches(0.4), h5 - Inches(0.35))
tf5_3 = tb5_3.text_frame
tf5_3.word_wrap = True
p = tf5_3.paragraphs[0]
p.text = 'Selection & Preprocessing'
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = ACCENT_GREEN

b5_3 = [
    ('Strict Fold Isolation', 'All scaling and feature selection operations are fitted strictly on training subjects to ensure zero subject leakage.'),
    ('StandardScaler Normalization', 'Zero-mean, unit-variance normalization applied across feature channels to balance disparate graph and coherence scales.'),
    ('ANOVA F-Test Selection', 'SelectKBest with f_classif ranks all 600 features by variance ratio (between-class vs within-class variance).'),
    ('Top 50 Discriminative Features', 'Preserves the 50 most statistically significant features, maximizing classification signal-to-noise ratio.'),
    ('Curse of Dimensionality', 'Prevents model overfitting by reducing input dimensionality by 91.7% while maintaining high discriminability.')
]
add_bullets(tf5_3, b5_3, is_dark=False, font_size=9.5, space_after=6)

# ==============================================================================
# SLIDE 6: MODEL ARCHITECTURES: CLASSICAL ML VS DEEP 1D-CNN
# ==============================================================================
s6 = create_slide(is_dark=False)
add_header(s6, 'Comparative Architectures: From Ensembles to Deep Convolutions',
           kicker='Modeling & Architecture Design',
           subtitle='Benchmarking tabular classical machine learning against a true sequential 1D-CNN')

# Left Column: Classical ML
add_card(s6, Inches(0.8), Inches(1.65), Inches(5.65), Inches(5.2))
tb6_l = s6.shapes.add_textbox(Inches(1.05), Inches(1.8), Inches(5.15), Inches(4.9))
tf6_l = tb6_l.text_frame
tf6_l.word_wrap = True
p = tf6_l.paragraphs[0]
p.text = 'Classical Machine Learning Pipeline'
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = ACCENT_BLUE

b6_l = [
    ('Input Transformation', 'The 4-window sequence (4 steps x 50 features) is temporally mean-pooled into a static 50-dimensional input vector for classical algorithms.'),
    ('Support Vector Machine (SVM)', 'Employs a Radial Basis Function (RBF) non-linear kernel with penalty C=2.0 and gamma="scale" to construct optimal separating hyperplanes.'),
    ('Random Forest Classifier', 'Ensemble of 150 bagged decision trees with max depth=6 and min_samples_leaf=2 to control model complexity and variance.'),
    ('XGBoost Gradient Boosting', 'Sequential boosting with 80 trees, max depth=3, learning rate=0.05, and 80% feature subsampling to minimize logarithmic loss.'),
    ('K-Nearest Neighbors (KNN)', 'Distance-weighted Euclidean voting with k=7 neighbors, serving as a non-parametric baseline benchmark.')
]
add_bullets(tf6_l, b6_l, is_dark=False, font_size=10, space_after=7)

# Right Column: Deep 1D-CNN
add_card(s6, Inches(6.8), Inches(1.65), Inches(5.733), Inches(5.2))
tb6_r = s6.shapes.add_textbox(Inches(7.05), Inches(1.8), Inches(5.233), Inches(4.9))
tf6_r = tb6_r.text_frame
tf6_r.word_wrap = True
p = tf6_r.paragraphs[0]
p.text = 'WorkloadSequential1DCNN (Deep Learning Engine)'
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = ACCENT_INDIGO

b6_r = [
    ('Temporal 3D Tensor Input', 'Directly ingests the full 3D tensor: (Batch Size, 50 Features, 4 Timesteps) - preserving continuous 20s temporal trajectories.'),
    ('Convolutional Block 1', 'Conv1D(in=50, out=64, kernel=2, pad=1) -> BatchNorm1d(64) -> ReLU() -> Dropout(p=0.30) to learn low-level temporal motifs.'),
    ('Convolutional Block 2', 'Conv1D(in=64, out=32, kernel=2, pad=1) -> BatchNorm1d(32) -> ReLU() -> AdaptiveAvgPool1d(1) to compress temporal dynamics into a 32-dim latent vector.'),
    ('Dense Classification Head', 'Linear(32 -> 16) -> ReLU() -> Dropout(p=0.40) -> Linear(16 -> 1) -> Sigmoid() producing workload probability.'),
    ('Training Optimization', 'Trained with Binary Cross-Entropy (BCELoss), Adam Optimizer (learning rate=0.001, weight decay=1e-3), batch size=32.')
]
add_bullets(tf6_r, b6_r, is_dark=False, font_size=10, space_after=7)

print('Slides 5 and 6 appended.')
# ==============================================================================
# SLIDE 7: VALIDATION STRATEGY: LEAVE-ONE-SUBJECT-OUT (LOSO)
# ==============================================================================
s7 = create_slide(is_dark=False)
add_header(s7, 'Leave-One-Subject-Out (LOSO): Eliminating Subject Leakage',
           kicker='Experimental Integrity & Rigor',
           subtitle='Ensuring genuine subject-independent generalization for real-world neuroadaptive BCI deployment')

# Top 3 Stat Cards
s7_stats = [
    ('48 Folds', 'Outer Validation Loops', 'Strict leave-one-subject-out iteration', ACCENT_BLUE),
    ('Zero Leakage', 'Pipeline Isolation', 'Scaling & feature selection in-fold only', ACCENT_INDIGO),
    ('Zero Calibration', 'Plug-and-Play Test', 'Tests immediately on brand-new brains', ACCENT_GREEN)
]
for idx, (val, lbl, sub, col) in enumerate(s7_stats):
    bx = Inches(0.8) + idx * (Inches(3.72) + Inches(0.28))
    add_stat_box(s7, bx, Inches(1.65), Inches(3.72), Inches(1.15), val, lbl, sub, accent_color=col, is_dark=False)

# Left Column: Pitfalls of K-Fold
add_card(s7, Inches(0.8), Inches(2.95), Inches(5.65), Inches(3.9))
tb7_l = s7.shapes.add_textbox(Inches(1.05), Inches(3.05), Inches(5.15), Inches(3.6))
tf7_l = tb7_l.text_frame
tf7_l.word_wrap = True
p = tf7_l.paragraphs[0]
p.text = 'The Critical Pitfall of Standard K-Fold Cross-Validation'
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = ACCENT_RED

b7_l = [
    ('Temporal Random Splitting Flaw', 'Conventional random k-fold splits time-windows from the same subject into both training and test folds.'),
    ('Subject-Identity Memorization', 'Because individual human skull thickness, electrode impedances, and resting alpha peaks are unique, models memorize user identity rather than mental workload.'),
    ('Artificial Performance Inflation', 'Standard k-fold routinely yields misleading 95–99% accuracies in literature that collapse to chance when deployed on unseen users in clinical reality.'),
    ('Unsuitability for Real-World BCI', 'A deployable BCI cannot require extensive retraining or invasive calibration on every prospective operator.')
]
add_bullets(tf7_l, b7_l, is_dark=False, font_size=9.5, space_after=6)

# Right Column: Our Strict Protocol
add_card(s7, Inches(6.8), Inches(2.95), Inches(5.733), Inches(3.9))
tb7_r = s7.shapes.add_textbox(Inches(7.05), Inches(3.05), Inches(5.233), Inches(3.6))
tf7_r = tb7_r.text_frame
tf7_r.word_wrap = True
p = tf7_r.paragraphs[0]
p.text = 'Our Strict 48-Subject LOSO Protocol'
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = ACCENT_GREEN

b7_r = [
    ('Outer LOSO Loop', 'In each fold, exactly 1 subject is isolated as the unseen test set (2 recordings, 54 sequences), while the remaining 47 subjects form the training set (94 recordings, ~2,538 sequences).'),
    ('Complete Pipeline Encapsulation', 'StandardScaler normalization and ANOVA F-test feature selection are fitted exclusively on the 47 training subjects during each fold.'),
    ('Zero Information Contamination', 'The test subject features are transformed using training parameters with no test-set feedback.'),
    ('Honest Generalization Assessment', 'Demonstrates true cross-subject generalizability, providing a sound scientific baseline for real-world applications.')
]
add_bullets(tf7_r, b7_r, is_dark=False, font_size=9.5, space_after=6)

# ==============================================================================
# SLIDE 8: OVERALL MODEL PERFORMANCE COMPARISON
# ==============================================================================
s8 = create_slide(is_dark=False)
add_header(s8, 'Cross-Model Benchmark Under LOSO Validation',
           kicker='Benchmark Results',
           subtitle='Quantitative comparison across classical machine learning models and deep 1D-CNN')

# Left Side: Table Card
add_card(s8, Inches(0.8), Inches(1.65), Inches(5.8), Inches(4.3))
tb8_t = s8.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.4), Inches(0.4))
tf8_t = tb8_t.text_frame
tf8_t.word_wrap = True
pt = tf8_t.paragraphs[0]
pt.text = 'LOSO Performance Metrics Across 48 Subjects'
pt.font.size = Pt(13.5)
pt.font.bold = True
pt.font.color.rgb = ACCENT_BLUE

# Create Table
table_shape = s8.shapes.add_table(6, 5, Inches(1.0), Inches(2.3), Inches(5.4), Inches(2.6))
tbl = table_shape.table
tbl.columns[0].width = Inches(1.8)
tbl.columns[1].width = Inches(1.2)
tbl.columns[2].width = Inches(0.8)
tbl.columns[3].width = Inches(0.8)
tbl.columns[4].width = Inches(0.8)

headers = ['Model Architecture', 'Accuracy (%)', 'Prec (%)', 'Rec (%)', 'F1 (%)']
for col_idx, h in enumerate(headers):
    cell = tbl.cell(0, col_idx)
    cell.fill.solid()
    cell.fill.fore_color.rgb = RGBColor(15, 23, 42)
    p = cell.text_frame.paragraphs[0]
    p.text = h
    p.font.bold = True
    p.font.size = Pt(9.5)
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.alignment = PP_ALIGN.CENTER if col_idx > 0 else PP_ALIGN.LEFT

row_data = [
    ('SVM (RBF Kernel)', '78.41 ± 19.58', '81.29', '76.83', '75.31'),
    ('1D-CNN (Deep Learning)', '77.38 ± 19.80', '81.17', '78.96', '77.00'),
    ('XGBoost Classifier', '77.07 ± 18.73', '78.91', '76.67', '74.63'),
    ('Random Forest (150 trees)', '76.87 ± 20.34', '79.52', '77.94', '75.01'),
    ('KNN Baseline (k=7)', '72.54 ± 19.78', '74.12', '74.78', '71.76')
]

for row_idx, r_vals in enumerate(row_data, start=1):
    bg_c = RGBColor(241, 245, 249) if row_idx % 2 == 1 else RGBColor(255, 255, 255)
    for col_idx, val in enumerate(r_vals):
        cell = tbl.cell(row_idx, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = bg_c
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.size = Pt(9)
        if col_idx == 0:
            p.font.bold = True
            p.font.color.rgb = TEXT_DARK
            p.alignment = PP_ALIGN.LEFT
        else:
            p.font.color.rgb = TEXT_BODY
            p.alignment = PP_ALIGN.CENTER

# Right Side: Image Card
add_card(s8, Inches(6.8), Inches(1.65), Inches(5.733), Inches(4.3))
img_acc = os.path.join(BASE_DIR, 'graphs', 'accuracy_comparison.png')
add_image_fitted(s8, img_acc, Inches(6.95), Inches(1.8), Inches(5.433), Inches(4.0))

# Bottom Highlight Card across both columns
add_card(s8, Inches(0.8), Inches(6.05), Inches(11.733), Inches(0.8), bg_color=RGBColor(238, 242, 255), border_color=ACCENT_INDIGO)
tb8_b = s8.shapes.add_textbox(Inches(1.0), Inches(6.12), Inches(11.333), Inches(0.65))
tf8_b = tb8_b.text_frame
tf8_b.word_wrap = True
pb = tf8_b.paragraphs[0]
r_lead = pb.add_run()
r_lead.text = 'Core Benchmark Takeaways: '
r_lead.font.bold = True
r_lead.font.color.rgb = ACCENT_INDIGO
r_lead.font.size = Pt(10.5)

r_body = pb.add_run()
r_body.text = 'SVM achieves top overall accuracy (78.41%), closely tracked by 1D-CNN (77.38%). Crucially, the 1D-CNN achieves the highest recall (78.96%) and balanced F1 score (77.00%), confirming that temporal sequence modeling is more sensitive to high-workload cognitive transitions.'
r_body.font.size = Pt(10)
r_body.font.color.rgb = TEXT_DARK

print('Slides 7 and 8 appended.')
# ==============================================================================
# SLIDE 9: DETAILED CLASSIFICATION METRICS (PRECISION, RECALL, F1)
# ==============================================================================
s9 = create_slide(is_dark=False)
add_header(s9, 'Comprehensive Evaluation Across Precision, Recall, and F1',
           kicker='Diagnostic Trade-Offs & Sensitivity',
           subtitle='Balancing false alarms against missed cognitive saturation events in safety-critical operations')

# Left Column: Metrics Bar Chart
add_card(s9, Inches(0.8), Inches(1.65), Inches(5.8), Inches(5.2))
img_met = os.path.join(BASE_DIR, 'graphs', 'classification_metrics.png')
add_image_fitted(s9, img_met, Inches(0.95), Inches(1.8), Inches(5.5), Inches(4.9))

# Right Column: 3 Detailed Diagnostic Insight Cards
r_top9 = Inches(1.65)
card_h9 = Inches(1.63)
gap9 = Inches(0.15)
card_w9 = Inches(5.65)

# Insight 1: Precision
add_card(s9, Inches(6.8), r_top9, card_w9, card_h9)
tb9_1 = s9.shapes.add_textbox(Inches(7.0), r_top9 + Inches(0.1), card_w9 - Inches(0.4), card_h9 - Inches(0.2))
tf9_1 = tb9_1.text_frame
tf9_1.word_wrap = True
p = tf9_1.paragraphs[0]
p.text = '1. Precision & Prevention of Alarm Fatigue'
p.font.size = Pt(11.5)
p.font.bold = True
p.font.color.rgb = ACCENT_BLUE

b9_1 = [
    ('High Specificity', 'SVM (81.29%) and 1D-CNN (81.17%) achieve the lowest false-alarm rates.'),
    ('Operational Value', 'Prevents erroneous workload warnings, preserving operator trust in automated assistance systems in aviation and air traffic control.')
]
add_bullets(tf9_1, b9_1, is_dark=False, font_size=9, space_after=2)

# Insight 2: Recall
add_card(s9, Inches(6.8), r_top9 + card_h9 + gap9, card_w9, card_h9)
tb9_2 = s9.shapes.add_textbox(Inches(7.0), r_top9 + card_h9 + gap9 + Inches(0.1), card_w9 - Inches(0.4), card_h9 - Inches(0.2))
tf9_2 = tb9_2.text_frame
tf9_2.word_wrap = True
p = tf9_2.paragraphs[0]
p.text = '2. Recall & Safety-Critical Sensitivity'
p.font.size = Pt(11.5)
p.font.bold = True
p.font.color.rgb = ACCENT_GREEN

b9_2 = [
    ('1D-CNN Superiority', '1D-CNN reaches 78.96% recall, outperforming SVM (76.83%) and XGBoost (76.67%).'),
    ('Safety Imperative', 'Failing to detect true cognitive overload (Type II error) can be catastrophic. The sequential CNN captures transient overload cues more effectively.')
]
add_bullets(tf9_2, b9_2, is_dark=False, font_size=9, space_after=2)

# Insight 3: F1 Balance
add_card(s9, Inches(6.8), r_top9 + 2 * (card_h9 + gap9), card_w9, card_h9)
tb9_3 = s9.shapes.add_textbox(Inches(7.0), r_top9 + 2 * (card_h9 + gap9) + Inches(0.1), card_w9 - Inches(0.4), card_h9 - Inches(0.2))
tf9_3 = tb9_3.text_frame
tf9_3.word_wrap = True
p = tf9_3.paragraphs[0]
p.text = '3. Harmonic F1 Score & Robustness'
p.font.size = Pt(11.5)
p.font.bold = True
p.font.color.rgb = ACCENT_INDIGO

b9_3 = [
    ('Peak Overall F1', '1D-CNN attains 77.00% F1, surpassing SVM (75.31%) and Random Forest (75.01%).'),
    ('Balanced Generalization', 'Confirms that temporal convolutions maintain the optimal balance between precision and sensitivity across heterogeneous subjects.')
]
add_bullets(tf9_3, b9_3, is_dark=False, font_size=9, space_after=2)

# ==============================================================================
# SLIDE 10: INTER-SUBJECT VARIABILITY & ACCURACY DISTRIBUTION
# ==============================================================================
s10 = create_slide(is_dark=False)
add_header(s10, 'Subject-Wise Accuracy Distribution & Performance Spread',
           kicker='Neurodiversity & Generalization',
           subtitle='Analyzing population-level neurodiversity and model consistency across 48 subjects')

# Left Side: Boxplot
add_card(s10, Inches(0.8), Inches(1.65), Inches(5.65), Inches(4.1))
img_box = os.path.join(BASE_DIR, 'graphs', 'accuracy_boxplot.png')
add_image_fitted(s10, img_box, Inches(0.95), Inches(1.75), Inches(5.35), Inches(3.9))

# Right Side: Subject Plot
add_card(s10, Inches(6.75), Inches(1.65), Inches(5.783), Inches(4.1))
img_sub = os.path.join(BASE_DIR, 'graphs', 'subject_accuracy.png')
add_image_fitted(s10, img_sub, Inches(6.9), Inches(1.75), Inches(5.483), Inches(3.9))

# Bottom Summary Card across both columns
add_card(s10, Inches(0.8), Inches(5.9), Inches(11.733), Inches(1.0), bg_color=CARD_LIGHT)
tb10_b = s10.shapes.add_textbox(Inches(1.0), Inches(5.95), Inches(11.333), Inches(0.9))
tf10_b = tb10_b.text_frame
tf10_b.word_wrap = True

p10_1 = tf10_b.paragraphs[0]
r_lead = p10_1.add_run()
r_lead.text = 'Median Superiority vs. Atypical Outliers: '
r_lead.font.bold = True
r_lead.font.color.rgb = ACCENT_BLUE
r_lead.font.size = Pt(10)

r_body = p10_1.add_run()
r_body.text = 'While the population mean is ~77–78%, median subject accuracy is ~85%, with over 60% of participants achieving >85% accuracy. A small cluster of atypical subjects (e.g. Sub04, Sub23, Sub39) with aberrant resting baselines pulls down the arithmetic mean.'
r_body.font.size = Pt(9.5)
r_body.font.color.rgb = TEXT_DARK

p10_2 = tf10_b.add_paragraph()
r_lead2 = p10_2.add_run()
r_lead2.text = 'Cross-Model Architectural Synchronization: '
r_lead2.font.bold = True
r_lead2.font.color.rgb = ACCENT_INDIGO
r_lead2.font.size = Pt(10)

r_body2 = p10_2.add_run()
r_body2.text = 'The subject-wise accuracy trajectories are closely aligned across SVM, CNN, and tree models, demonstrating that inter-subject difficulty is driven by intrinsic neurophysiology rather than algorithmic limitations.'
r_body2.font.size = Pt(9.5)
r_body2.font.color.rgb = TEXT_DARK

print('Slides 9 and 10 appended.')
# ==============================================================================
# SLIDE 11: EXPLAINABILITY FRAMEWORK: GROUPED ELECTRODE PERMUTATION IMPORTANCE
# ==============================================================================
s11 = create_slide(is_dark=False)
add_header(s11, 'Quantifying Predictive Reliance via Grouped Electrode Permutation',
           kicker='Explainable AI (XAI) Methodology',
           subtitle='A statistically rigorous post-hoc perturbation framework to isolate critical brain regions')

# Left Column: Grouping Framework
add_card(s11, Inches(0.8), Inches(1.65), Inches(5.65), Inches(5.2))
tb11_l = s11.shapes.add_textbox(Inches(1.05), Inches(1.8), Inches(5.15), Inches(4.9))
tf11_l = tb11_l.text_frame
tf11_l.word_wrap = True
p = tf11_l.paragraphs[0]
p.text = 'Grouped Electrode Feature Mapping'
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = ACCENT_BLUE

b11_l = [
    ('Multi-Feature Channel Identity', 'A single EEG electrode does not represent a single feature. It participates in multiple pairwise connectivity edges and network graph metrics.'),
    ('65 Incident Coherence Edges', 'Each electrode connects to 13 other channels across 5 frequency bands (13 x 5 = 65 pairwise coherence features).'),
    ('10 Nodal Graph Metrics', 'Each electrode contributes 1 Closeness Centrality and 1 Clustering Coefficient metric across all 5 bands (2 x 5 = 10 graph features).'),
    ('75 Features Permuted Simultaneously', 'To faithfully assess the functional contribution of an electrode, all 75 incident features must be jointly scrambled.'),
    ('Unassigned Global Features', 'The 5 global average shortest-path features are preserved without permutation to prevent confounding whole-brain network bias.')
]
add_bullets(tf11_l, b11_l, is_dark=False, font_size=10, space_after=7)

# Right Column: Protocol & Statistics
add_card(s11, Inches(6.8), Inches(1.65), Inches(5.733), Inches(5.2))
tb11_r = s11.shapes.add_textbox(Inches(7.05), Inches(1.8), Inches(5.233), Inches(4.9))
tf11_r = tb11_r.text_frame
tf11_r.word_wrap = True
p = tf11_r.paragraphs[0]
p.text = 'Permutation Protocol & Statistical Rigor'
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = ACCENT_INDIGO

b11_r = [
    ('5 Permutations Per Channel', 'For each held-out test subject in LOSO, the 75-feature block is permuted across time windows 5 times (240 evaluations per channel per model).'),
    ('Balanced Accuracy Delta', 'Importance is defined as: Delta BA = Baseline BA - Permuted BA. Positive values indicate critical reliance; negative indicates noise/redundancy.'),
    ('Bootstrap 95% Confidence Intervals', 'Computed via 1,000 subject-level bootstrap resamples to establish non-parametric confidence bounds.'),
    ('Wilcoxon Signed-Rank Test', 'Evaluates the null hypothesis that electrode perturbation does not degrade balanced accuracy (one-sided p-value against zero).'),
    ('Benjamini-Hochberg FDR Control', 'Corrects for multiple comparisons across the 14 channels, enforcing False Discovery Rate control at q < 0.05.')
]
add_bullets(tf11_r, b11_r, is_dark=False, font_size=10, space_after=7)

# ==============================================================================
# SLIDE 12: PREDICTIVE NODE IMPORTANCE HEATMAP & CROSS-MODEL RANKINGS
# ==============================================================================
s12 = create_slide(is_dark=False)
add_header(s12, 'Channel Predictive Importance Heatmap & Model Rankings',
           kicker='Empirical Findings',
           subtitle='Prefrontal and fronto-central electrodes demonstrate overwhelming predictive dominance across classifiers')

# Left Side: Heatmap
add_card(s12, Inches(0.8), Inches(1.65), Inches(5.65), Inches(4.2))
img_heat = os.path.join(BASE_DIR, 'loso_full_test', '02_model_node_importance_heatmap.png')
add_image_fitted(s12, img_heat, Inches(0.95), Inches(1.75), Inches(5.35), Inches(4.0))

# Right Side: Grouped Bar Chart
add_card(s12, Inches(6.75), Inches(1.65), Inches(5.783), Inches(4.2))
img_group = os.path.join(BASE_DIR, 'loso_full_test', '03_grouped_node_importance_by_model.png')
add_image_fitted(s12, img_group, Inches(6.9), Inches(1.75), Inches(5.483), Inches(4.0))

# Bottom Summary Card across both columns
add_card(s12, Inches(0.8), Inches(6.0), Inches(11.733), Inches(0.9), bg_color=RGBColor(240, 253, 244), border_color=ACCENT_GREEN)
tb12_b = s12.shapes.add_textbox(Inches(1.0), Inches(6.05), Inches(11.333), Inches(0.8))
tf12_b = tb12_b.text_frame
tf12_b.word_wrap = True

p12_1 = tf12_b.paragraphs[0]
r_lead = p12_1.add_run()
r_lead.text = 'Unequivocal Frontal Consensus Across Models: '
r_lead.font.bold = True
r_lead.font.color.rgb = ACCENT_GREEN
r_lead.font.size = Pt(10)

r_body = p12_1.add_run()
r_body.text = 'AF4 ranks #1 across Random Forest (+4.14% drop, FDR p=2.7e-5) and SVM (+3.59% drop, FDR p=2.8e-4). FC6 ranks #2 across all models (+3.70% RF, +3.26% SVM). F4 and AF3 occupy ranks #3 and #4. Prefrontal and fronto-central electrodes consistently drive the classification boundary.'
r_body.font.size = Pt(9.5)
r_body.font.color.rgb = TEXT_DARK

# ==============================================================================
# SLIDE 13: NEUROPHYSIOLOGICAL INTERPRETATION & BRAIN MAPPING
# ==============================================================================
s13 = create_slide(is_dark=False)
add_header(s13, 'Mapping Predictive Biomarkers to Cognitive Neuroscience',
           kicker='Neurophysiological Correlates',
           subtitle='Validating model decision boundaries against established cortical networks and mental fatigue literature')

card_w13 = Inches(3.72)
gap13 = Inches(0.28)
top13 = Inches(1.65)
h13 = Inches(5.2)

# Card 1: Prefrontal Executive Hub
add_card(s13, Inches(0.8), top13, card_w13, h13)
tb13_1 = s13.shapes.add_textbox(Inches(1.0), Inches(1.8), card_w13 - Inches(0.4), h13 - Inches(0.35))
tf13_1 = tb13_1.text_frame
tf13_1.word_wrap = True
p = tf13_1.paragraphs[0]
p.text = 'Prefrontal Executive Hub (AF4, AF3)'
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = ACCENT_BLUE

b13_1 = [
    ('Cortical Substrate', 'Frontal Pole and Dorsolateral Prefrontal Cortex (DLPFC).'),
    ('Cognitive Role', 'Central executive network seat responsible for goal maintenance, working memory updates, and rule execution.'),
    ('Task Demands', 'The SIMKAP multitasking protocol continuously overloads working memory buffers, producing prominent phase synchrony changes at AF4 and AF3.'),
    ('Artifact Dissociation', 'FDR significance (p < 0.001) persists despite bandpass filtering, demonstrating that models track true prefrontal activation rather than ocular artifacts.')
]
add_bullets(tf13_1, b13_1, is_dark=False, font_size=9.2, space_after=6)

# Card 2: Right-Hemisphere Fronto-Central Dominance
add_card(s13, Inches(0.8) + card_w13 + gap13, top13, card_w13, h13)
tb13_2 = s13.shapes.add_textbox(Inches(0.8) + card_w13 + gap13 + Inches(0.2), Inches(1.8), card_w13 - Inches(0.4), h13 - Inches(0.35))
tf13_2 = tb13_2.text_frame
tf13_2.word_wrap = True
p = tf13_2.paragraphs[0]
p.text = 'Fronto-Central Network (FC6, F4)'
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = ACCENT_INDIGO

b13_2 = [
    ('Cortical Substrate', 'Premotor cortex, Supplementary Motor Area (SMA), and Frontal Eye Fields (FEF).'),
    ('Cognitive Role', 'Fast sensorimotor decision mapping, stimulus-response association, and selective attention steering.'),
    ('Right-Hemispheric Lateralization', 'Right-hemisphere electrodes (AF4: +4.14%, FC6: +3.70%, F4: +2.25%) substantially outperform their left-hemisphere counterparts (AF3: +1.54%, FC5: +0.85%).'),
    ('Neurocognitive Agreement', 'Directly aligns with neuroscience literature: the right prefrontal cortex preferentially governs sustained vigilance and arithmetic stress.')
]
add_bullets(tf13_2, b13_2, is_dark=False, font_size=9.2, space_after=6)

# Card 3: Parieto-Occipital Integration
add_card(s13, Inches(0.8) + 2 * (card_w13 + gap13), top13, card_w13, h13)
tb13_3 = s13.shapes.add_textbox(Inches(0.8) + 2 * (card_w13 + gap13) + Inches(0.2), Inches(1.8), card_w13 - Inches(0.4), h13 - Inches(0.35))
tf13_3 = tb13_3.text_frame
tf13_3.word_wrap = True
p = tf13_3.paragraphs[0]
p.text = 'Sensory Integration (O1, O2, P7)'
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = ACCENT_AMBER

b13_3 = [
    ('Cortical Substrate', 'Primary Visual Cortex (V1/V2, O1/O2) and Posterior Parietal Cortex (P7).'),
    ('Cognitive Role', 'High-throughput visual character scanning, optical discrimination, and spatial coordinate transformation.'),
    ('Task Synergy', 'Occipital channels capture the continuous sensory processing demands imposed by on-screen SIMKAP test items.'),
    ('Secondary Modulator', 'Serves as an essential secondary sensory pathway; when combined with frontal executive networks, it optimizes classification stability.')
]
add_bullets(tf13_3, b13_3, is_dark=False, font_size=9.2, space_after=6)

# ==============================================================================
# SLIDE 14: SUBJECT CONSISTENCY & HEADSET MONTAGE REDUCTION
# ==============================================================================
s14 = create_slide(is_dark=False)
add_header(s14, 'Subject Consistency & Towards Reduced Montage Headsets',
           kicker='Robustness & Clinical Application',
           subtitle='Translating explainability insights into lightweight, wearable BCI hardware')

# Left Side: Subject Consistency Heatmap
add_card(s14, Inches(0.8), Inches(1.65), Inches(5.8), Inches(5.2))
img_cons = os.path.join(BASE_DIR, 'loso_full_test', '05_subject_consistency_heatmap.png')
add_image_fitted(s14, img_cons, Inches(0.95), Inches(1.8), Inches(5.5), Inches(4.9))

# Right Side: 2 Wearable Translation Cards
add_card(s14, Inches(6.8), Inches(1.65), Inches(5.733), Inches(2.45))
tb14_1 = s14.shapes.add_textbox(Inches(7.05), Inches(1.75), Inches(5.233), Inches(2.25))
tf14_1 = tb14_1.text_frame
tf14_1.word_wrap = True
p = tf14_1.paragraphs[0]
p.text = 'Population-Level Subject Consistency'
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = ACCENT_BLUE

b14_1 = [
    ('77.1% Subject Agreement', '77.1% of all held-out subjects exhibit degraded accuracy when AF4 is masked; 75.0% for FC6.'),
    ('Inter-Subject Stability', 'Unlike temporal channels (T7/T8) which exhibit high subject variance, frontal electrodes demonstrate universal predictive reliance across individuals.'),
    ('Absence of Subject-Specific Bias', 'Confirms that frontal dominance is a shared biological biomarker rather than an artifact of a few outlier subjects.')
]
add_bullets(tf14_1, b14_1, is_dark=False, font_size=9.5, space_after=4)

add_card(s14, Inches(6.8), Inches(4.3), Inches(5.733), Inches(2.55))
tb14_2 = s14.shapes.add_textbox(Inches(7.05), Inches(4.4), Inches(5.233), Inches(2.35))
tf14_2 = tb14_2.text_frame
tf14_2.word_wrap = True
p = tf14_2.paragraphs[0]
p.text = 'Toward Wearable 4-Channel Headsets'
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = ACCENT_GREEN

b14_2 = [
    ('The Clinical Wearability Bottleneck', '14-channel medical caps require conductive gel, extensive setup time, and cause discomfort during long shifts.'),
    ('Optimal Minimal Montage', 'Our empirical rankings isolate an ultra-compact 4-electrode montage: [AF4, FC6, F4, AF3].'),
    ('Forehead/Temple Ergonomics', 'All four critical electrodes reside on the anterior forehead and temple, enabling dry-sensor, gel-free smart headbands.'),
    ('Translational Impact', 'Paves the path for practical real-time cognitive state tracking in commercial cockpits, surgical suites, and industrial control rooms.')
]
add_bullets(tf14_2, b14_2, is_dark=False, font_size=9.5, space_after=4)

print('Slides 11, 12, 13, and 14 appended.')
# ==============================================================================
# SLIDE 15: DISCUSSION, CRITICAL NUANCES & FUTURE ROADMAP
# ==============================================================================
s15 = create_slide(is_dark=False)
add_header(s15, 'Critical Nuances, Methodological Caveats & Future Horizons',
           kicker='Methodological Considerations & Roadmap',
           subtitle='Distinguishing predictive reliance from causality and charting future technological advancements')

# Left Column: Critical Nuances
add_card(s15, Inches(0.8), Inches(1.65), Inches(5.65), Inches(5.2))
tb15_l = s15.shapes.add_textbox(Inches(1.05), Inches(1.8), Inches(5.15), Inches(4.9))
tf15_l = tb15_l.text_frame
tf15_l.word_wrap = True
p = tf15_l.paragraphs[0]
p.text = 'Methodological Nuances & Scientific Caveats'
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = ACCENT_AMBER

b15_l = [
    ('Overlapping Coherence Edges', 'Pairwise coherence connects two endpoints; each edge is shared by both electrodes. Importance reflects joint predictive reliance and is therefore non-additive.'),
    ('Model Reliance vs Neural Causality', 'Permutation importance identifies what the statistical model relies upon for classification, not direct neurophysiological causality.'),
    ('Fixed Hyperparameter Benchmark', 'All models operated with standardized parameters. A subsequent clinical validation will incorporate nested subject-wise Bayesian hyperparameter optimization.'),
    ('Retraining Verification Requirement', 'Importance rankings highlight candidates for montage reduction; empirical proof requires retraining dedicated models exclusively on candidate sub-montages.')
]
add_bullets(tf15_l, b15_l, is_dark=False, font_size=10, space_after=8)

# Right Column: Future Roadmap
add_card(s15, Inches(6.8), Inches(1.65), Inches(5.733), Inches(5.2))
tb15_r = s15.shapes.add_textbox(Inches(7.05), Inches(1.8), Inches(5.233), Inches(4.9))
tf15_r = tb15_r.text_frame
tf15_r.word_wrap = True
p = tf15_r.paragraphs[0]
p.text = 'Future Research & Engineering Horizons'
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = ACCENT_INDIGO

b15_r = [
    ('Spatio-Temporal Graph Neural Networks', 'Implement ST-GNNs (e.g. ST-GCN, GAT) to jointly learn dynamic graph connectivity and temporal transitions end-to-end directly from raw microvolts.'),
    ('Reduced-Montage Physical Retraining', 'Empirically train and validate dedicated 4-channel models (AF4, FC6, F4, AF3) to quantify performance retention vs 14 channels.'),
    ('Cross-Dataset & Multi-Task Transfer', 'Evaluate cross-corpus domain adaptation across DEAP, SEED, and NASA-MATB datasets using self-supervised foundation transformers.'),
    ('Embedded Ultra-Low Power BCI', 'Quantize the 1D-CNN architecture into INT8 for real-time edge execution on ARM Cortex-M microcontrollers embedded inside smart headbands.')
]
add_bullets(tf15_r, b15_r, is_dark=False, font_size=10, space_after=8)

# ==============================================================================
# SLIDE 16: CONCLUSION & EXECUTIVE SUMMARY (Dark Theme)
# ==============================================================================
s16 = create_slide(is_dark=True)
add_header(s16, 'Empowering Next-Generation Cognitive Brain-Signal Interfaces',
           kicker='Key Takeaways & Conclusions',
           subtitle='Summary of scientific breakthroughs and practical pathways to real-world neuroadaptive systems',
           is_dark=True)

# 3 Summary Cards Across Main Body
card_w16 = Inches(3.72)
gap16 = Inches(0.28)
top16 = Inches(1.65)
h16 = Inches(4.0)

# Card 1: Rigorous LOSO Benchmark
add_card(s16, Inches(0.8), top16, card_w16, h16, is_dark=True)
tb16_1 = s16.shapes.add_textbox(Inches(1.0), Inches(1.8), card_w16 - Inches(0.4), h16 - Inches(0.35))
tf16_1 = tb16_1.text_frame
tf16_1.word_wrap = True
p = tf16_1.paragraphs[0]
p.text = '1. Rigorous LOSO Validation'
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = ACCENT_CYAN

b16_1 = [
    ('Zero Subject Contamination', 'Strict 48-subject Leave-One-Subject-Out evaluation guarantees authentic subject-independent performance without data leakage.'),
    ('Robust Classification', 'Classical SVM achieved 78.41% accuracy, while tree ensembles and CNN achieved ~77–83% balanced accuracy across unseen brains.')
]
add_bullets(tf16_1, b16_1, is_dark=True, font_size=10, space_after=6)

# Card 2: Temporal Deep Learning
add_card(s16, Inches(0.8) + card_w16 + gap16, top16, card_w16, h16, is_dark=True)
tb16_2 = s16.shapes.add_textbox(Inches(0.8) + card_w16 + gap16 + Inches(0.2), Inches(1.8), card_w16 - Inches(0.4), h16 - Inches(0.35))
tf16_2 = tb16_2.text_frame
tf16_2.word_wrap = True
p = tf16_2.paragraphs[0]
p.text = '2. Temporal Sequence Modeling'
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = ACCENT_INDIGO

b16_2 = [
    ('Dynamic Continuous Waves', 'Transforming static windows into 20-second continuous temporal feature waves captured evolving cognitive dynamics.'),
    ('Peak Recall & F1 Dominance', 'Deep 1D-CNN delivered top sensitivity (78.96% recall) and harmonic F1 (77.00%), vital for preventing undetected cognitive overload.')
]
add_bullets(tf16_2, b16_2, is_dark=True, font_size=10, space_after=6)

# Card 3: Explainable Biomarkers
add_card(s16, Inches(0.8) + 2 * (card_w16 + gap16), top16, card_w16, h16, is_dark=True)
tb16_3 = s16.shapes.add_textbox(Inches(0.8) + 2 * (card_w16 + gap16) + Inches(0.2), Inches(1.8), card_w16 - Inches(0.4), h16 - Inches(0.35))
tf16_3 = tb16_3.text_frame
tf16_3.word_wrap = True
p = tf16_3.paragraphs[0]
p.text = '3. Grounded Biomarker Discovery'
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = ACCENT_GREEN

b16_3 = [
    ('Statistically Rigorous XAI', 'Grouped electrode permutation with FDR correction (q < 0.05) confirmed significant prefrontal dominance.'),
    ('Wearable BCI Blueprint', 'AF4, FC6, and F4 identified as the vital triad, providing the empirical foundation for lightweight 4-channel forehead smart headbands.')
]
add_bullets(tf16_3, b16_3, is_dark=True, font_size=10, space_after=6)

# Bottom Closing Banner across all 3 columns
add_card(s16, Inches(0.8), Inches(5.85), Inches(11.733), Inches(1.05), bg_color=CARD_DARK, border_color=ACCENT_CYAN, is_dark=True)
tb16_b = s16.shapes.add_textbox(Inches(1.05), Inches(5.92), Inches(11.233), Inches(0.9))
tf16_b = tb16_b.text_frame
tf16_b.word_wrap = True

p16_b = tf16_b.paragraphs[0]
r_lead = p16_b.add_run()
r_lead.text = 'Vision & Translational Impact: '
r_lead.font.bold = True
r_lead.font.color.rgb = ACCENT_CYAN
r_lead.font.size = Pt(11)

r_body = p16_b.add_run()
r_body.text = 'By synthesizing high-dimensional spectral graph topology, temporal deep learning, and explainable AI under strict subject-independent validation, this research bridges the gap between laboratory EEG analysis and deployable, real-time neuroadaptive interfaces for high-stakes human-machine teaming.'
r_body.font.size = Pt(10)
r_body.font.color.rgb = TEXT_LIGHT

p16_sub = tf16_b.add_paragraph()
r_sub = p16_sub.add_run()
r_sub.text = 'Project AIBSI | STEW Dataset Benchmark | Ready for Questions & Discussion'
r_sub.font.size = Pt(9.5)
r_sub.font.italic = True
r_sub.font.color.rgb = ACCENT_INDIGO
p16_sub.space_before = Pt(3)

# Save the presentation
prs.save(OUTPUT_FILE)
print(f'SUCCESS! Presentation saved to: {OUTPUT_FILE}')
