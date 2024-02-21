import streamlit as st


st.set_page_config(
    page_title="LYZR",
    page_icon="",
)

st.image("lyzr-logo-oneColor-rgb-600-cropped.png", width=180)
st.title("Welcome to Lyzr OSS Agents")
st.write("Lyzr is a low-code agent framework that provides locally deployable agent SDKs and a control center to build and run generative AI applications securely and privately.  ")
st.write("""Lyzr SDKs cover a wide range of use cases:

Chatbots: Build memory-enabled chatbots for various sources, including PDF documents, websites, and YouTube videos.
Question Answering: Ask questions about your data, whether it's in a PDF, website, or text document.
Data Analysis: Analyze structured data in databases, spreadsheets, and CSV files using natural language queries.
Voice Processing: Convert speech to text, summarize text, and convert text back to speech.
Formula Generation: Simplify regular expressions, text-to-SQL queries, and spreadsheet formula generation.""")
st.write("Feel free to explore the diverse agents available here.")
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

