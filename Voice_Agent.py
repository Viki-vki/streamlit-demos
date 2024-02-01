import streamlit as st
from streamlit.logger import get_logger
import os
from audio_recorder_streamlit import audio_recorder
from openai import OpenAI
from PIL import Image
from lyzr import VoiceBot
import re
from json import JSONDecodeError
import streamlit_analytics
import pandas as pd
from streamlit import session_state


# This is the path to the json file where you want to save the analytics
analytics_filepath = "analytics.json"

# start tracking analytics
try:
    print("Loading analytics from json file.")
    streamlit_analytics.start_tracking(load_from_json=analytics_filepath)
except (JSONDecodeError, FileNotFoundError):
    print("No analytics json file found. Starting new analytics.")
    streamlit_analytics.start_tracking()

st.set_page_config(
    page_title="VoiceAgent",
    page_icon="🎤",
)
st.sidebar.title("Voice Agent")
st.image("lyzr-logo-oneColor-rgb-600-cropped.png", width=180)
st.title("Welcome to the Voice Agent")
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

st.sidebar.markdown(
    """<style>
    p .external-link {
        font-weight: bold;
        text-decoration: none;
        color: rgb(49, 51, 63);
    }
    p .external-link:after {
        content: "";
        background-image: url('https://www.svgrepo.com/show/374989/new-window.svg') !important;
        background-repeat: no-repeat;
        background-size: 12px;
        display: inline-block;
        width: 1em;
        height: 1em;
        margin-left: 3px;
    }
    </style>""",
    unsafe_allow_html=True,
)
st.sidebar.markdown(
    """
    <div style="bottom: 10px; position: fixed;">
    <p style='margin-bottom: 5px;'>
    <a class='external-link' href='https://lyzr.ai' target='_blank' rel='noopener noreferrer'>Homepage</a>
    </p>
    <p style='margin-bottom: 5px;'>
    <a class='external-link' href='https://docs.lyzr.ai' target='_blank' rel='noopener noreferrer'>Documentation</a>
    </p>
    <p style='margin-bottom: 5px;'>
    <a class='external-link' href='https://discord.gg/P6HCMQ9TRX' target='_blank' rel='noopener noreferrer'>Discord</a>
    </p>
    <p style='margin-bottom: 5px;'>
    <a class='external-link' href='https://join.slack.com/t/genaiforenterprise/shared_invite/zt-2a7fr38f7-_QDOY1W1WSlSiYNAEncLGw' target='_blank' rel='noopener noreferrer'>Slack</a>
    </p>
    </div>
    """,
    unsafe_allow_html=True,
)

def text_to_notes(text):
    
    notes = vb.text_to_notes(text)
    return notes

def save_uploadedfile(uploaded_file):
    with open(os.path.join('tempDir', uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())
    return st.success(f"Saved File: {uploaded_file.name} to tempDir")
def tts(text, model="tts-1-hd", voice="echo"):
    
    response= vb.text_to_speech(text)
    return response

def is_valid_api_key(api_key):
    """Check if the API key is valid. A valid API key in our case is a non-empty string of a certain length
    that consists of alphanumeric characters, optionally including hyphens and underscores."""
    return bool(re.match(r'^[a-zA-Z0-9\-_]{32,64}$', api_key))

def recordaudio():
    audio_bytes = audio_recorder(pause_threshold=10.0, sample_rate=41_000)
    recorded = False

    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")
        # Save the recorded audio for transcription
        with open('tempDir/output.wav', 'wb') as f:
            f.write(audio_bytes)
            transcript = vb.transcribe('tempDir/output.wav')
        #st.write(transcript)
        if transcript:
            ainotes = text_to_notes(transcript)
            #st.write(ainotes)
            recorded= True
    
    #Select Voice Style and Model
    col1, col2 = st.columns(2)

    with col1:
        voice = st.radio('Voice Style', ['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer'])

    with col2:
        model = st.radio('Model', ["tts-1","tts-1-hd"])
    
    submit_button = st.button("Submit")
    if submit_button:
        st.subheader('Transcription')
        st.write(transcript)
        st.subheader('Notes')
        st.write(ainotes)
        tts(ainotes, model, voice)
        st.subheader("Notes to Speech") 
        st.audio("tts_output.mp3")
    
    

def uploadaudio():
    st.subheader('Upload any audio file (.wav format only) and get the transcript', divider=True)
    uploaded_file = st.file_uploader("Upload Files", type=['wav'])
    recorded = False

    if uploaded_file is not None:
        file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
        st.write(file_details)
        save_uploadedfile(uploaded_file)
        audio_file = open(os.path.join('tempDir', uploaded_file.name), "rb")
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/wav')
        transcript = vb.transcribe(os.path.join('tempDir', uploaded_file.name))
        #st.write(transcript)
        if transcript:
            ainotes = text_to_notes(transcript)
            #st.write(ainotes)
            recorded= True
    
    #Select Voice Style and Model
    col1, col2 = st.columns(2)

    with col1:
        voice = st.radio('Voice Style', ['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer'])

    with col2:
        model = st.radio('Model', ["tts-1","tts-1-hd"])

    
    submit_button = st.button("Submit")
    if submit_button:
        st.subheader('Transcription')
        st.write(transcript)
        st.subheader('Notes')
        st.write(ainotes)
        tts(ainotes, model, voice)
        st.subheader("Notes to Speech") 
        st.audio("tts_output.mp3")

def Textaudio():
    st.subheader('Enter Text or Try a sample script')
    # Define the sample text
    sample_text = "The VoiceBot open-source software (OSS) module is a versatile tool that utilizes OpenAI's powerful APIs to perform text-to-speech conversion, audio transcription, and text summarization into structured notes."
    
    # Check if the sample button has been clicked before creating the text_area widget
    try_sample_button = st.button("Try Sample")
    if try_sample_button:
        st.session_state['sample_text'] = sample_text

    # Create the text area with a key different from 'sample_text'
    user_input = st.text_area("Enter Text", height=150, key="user_input", value=st.session_state.get('sample_text', ''))
    
    #Select Voice Style and Model
    col1, col2 = st.columns(2)

    with col1:
        voice = st.radio('Voice Style', ['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer'])

    with col2:
        model = st.radio('Model', ["tts-1","tts-1-hd"])

    
    submit_button = st.button("Submit")
    if submit_button:
        if pd.isna(user_input) or user_input.strip() == "":
            st.warning("Please enter some text before submitting.")
            return
        else:
            ainotes = text_to_notes(user_input)
            st.subheader('Notes')
            st.write(ainotes)
            tts(user_input, model, voice)
            st.subheader("Text to Speech") 
            st.audio("tts_output.mp3")
            tts(ainotes, model, voice)
            st.subheader("Notes to Speech") 
            st.audio("tts_output.mp3")


      
#Check if OpenAI API key is valid
if openai_api_key:
    if is_valid_api_key(openai_api_key):
        vb = VoiceBot(api_key=openai_api_key)
    else:
        st.warning("Please enter the correct API key.")
        st.stop()
elif openai_api_key is None or openai_api_key == "":
    st.info("Please add your OpenAI API key to continue.")
    st.stop()
else:
    st.warning("Invalid API key format!")
    st.stop()

page_options = ['Record Audio', 'Upload Audio','Text']

# Sidebar
selected_page = st.selectbox('Select Input type', page_options)

# Based on the selected page, display the content accordingly
if selected_page == 'Record Audio':
    recordaudio()
elif selected_page == 'Upload Audio':
    uploadaudio()
else:
    Textaudio()

# stop tracking analytics and save to json file
# IMPORTANT: You must add an environment variable ANALYTICS_PASSWORD to ~/.streamlit/secrets.toml
streamlit_analytics.stop_tracking(
    save_to_json=analytics_filepath, unsafe_password=os.environ["ANALYTICS_PASSWORD"]
)




