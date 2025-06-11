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

Welcome to **Immunoready**, a web app to classify peptide sequences as **safe** or **unsafe**.

### ⚙️ Prediction options:
A) Enter your peptide sequences manually (one per line)\n
B) Upload a CSV file with a column of peptide sequences

### 🧾 Instructions:
- Peptides must be between **8 and 25 amino acids** long.
- **⚠️ Do not use both input methods simultaneously.** If you do, only the **CSV input will be used**.
""")


# st.markdown("""# Welcome to Immunoready peptides classification
# You have two options to use the model:
# 1. simple text input: write the peptides you want to predict one after the other
# 2. file uploader: upload a csv file with peptides you want to predict

# Peptides you want to predict must have a lenght between 8 and 25.
# Do not use both text input ans csv input at the same time.
# If so, only the csv peptides will get a prediction.
# """)

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
