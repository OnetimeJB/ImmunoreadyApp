import streamlit as st
import pandas as pd
import requests
import base64
import mimetypes

st.set_page_config(
    page_title="Immunoready Peptide Classifier",
    layout="centered",
    page_icon="🧬")

def set_background(image_path, overlay_opacity=0.5):
    mime_type, _ = mimetypes.guess_type(image_path)
    if mime_type is None:
        mime_type = "image/jpeg"  # fallback default

    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

    css = f"""
    <style>
    .stApp {{
        background-image: url("data:{mime_type};base64,{encoded_string}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, {overlay_opacity});
        z-index: -1;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Path to your background image (change this to your actual image path)
background_image_path = 'virus.jpeg'

# Set background
set_background(background_image_path)


st.markdown("""
# 🧬 Immunoready: Peptide Safety Classifier

## Welcome to ImmunoReady
ImmunoReady is an AI-powered tool aiming to predict the safety of MHC-bound peptides in the context of vaccine development. By leveraging advanced machine learning algorithms, ImmunoReady helps identify peptides with minimal risk of triggering autoimmune responses, thereby streamlining and improving the vaccine design process.

### Key Features
- Autoimmunity Risk Assessment: ImmunoReady is specifically trained to distinguish peptides that could potentially trigger autoimmune or inflammatory responses from those that are safe, based solely on their amino acid sequences.
- MHC/HLA Agnostic: The tool operates independently of MHC class and HLA type, allowing for broad applicability across different populations and facilitating generalization.
- Curated Training Data: Peptides used for training include known epitopes implicated in autoimmune and inflammatory diseases, as well as peptides derived from healthy tissues, ensuring robust discrimination between risky and safe candidates.
- Vaccine Development Support: By flagging high-risk peptides early in the design pipeline, ImmunoReady helps researchers avoid sequences that could lead to adverse effects, accelerating safe vaccine development.

### How It Works
ImmunoReady analyzes peptide sequences submitted by the user and predicts their safety profile. The underlying model has been trained on a diverse dataset:

- Risky: Peptides associated with known autoimmune and inflammatory disorders.
- Safe: Peptides derived from healthy human tissues, considered safe for use in vaccines.

### Use Cases
- Epitope Screening: Quickly evaluate candidate peptides for their likelihood to induce autoimmunity.
- Rational Vaccine Design: Select sequences most likely to be safe, reducing downstream risk and development costs.
- Immunology Research: Explore sequence patterns and risk factors associated with autoimmunity at the peptide level.

### Technical Overview
- Input: Amino acid sequence of candidate peptide(s).
- Output: Classification of each peptide as "Safe" or "Potentially Autoimmunity Triggering," with associated confidence scores.

ImmunoReady empowers vaccine researchers to make informed, data-driven decisions, fostering innovation while prioritizing patient safety.
DISCLAIMER: This tool is under-development and results might not be accurate. Do not use the results for any clinical purposes.

### ⚙️ Prediction options:
A) Enter your peptide sequences manually (one per line)\n
B) Upload a CSV file with a column of peptide sequences

### 🧾 Instructions:
- Peptides must be between **8 and 25 amino acids** long.
- **⚠️ Do not use both input methods simultaneously.** If you do, only the **CSV input will be used**.
""")

st.divider()

with st.form(key='params_for_api'):
    input_text = st.text_area(
        "Enter peptide sequences (one per line):",
        height=200,
        placeholder="ACDEFGHIK\nLMNPQRSTV\nQTQAARSYTVASRSQSNSPR")

    uploaded_file = st.file_uploader("Upload a CSV file full of peptides", type="csv")

    st.form_submit_button('Make prediction')


params = dict()

if input_text:
    sequences = [seq.strip() for seq in input_text.splitlines() if seq.strip()]
    params['peptides'] = sequences
    st.write("You submitted the following sequences:")
    st.write(sequences)

if uploaded_file:
    data = pd.read_csv(uploaded_file,header=None)
    list = data.values.tolist()
    params['peptides'] = [items[0] for items in list]
    st.write("You submitted the following sequences:")
    st.write([items[0] for items in list])


immunoready_api_url = 'https://immunoready-157677064329.europe-west1.run.app/predict'

response = requests.post(
    immunoready_api_url,
    json = params)

prediction = response.json()

if 'predictions' in prediction:
    df = pd.DataFrame(prediction['predictions'])
    st.dataframe(df)
