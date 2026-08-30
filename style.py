import streamlit as st

def custom_style():
    css = '''
    <style>
        .st-key-styled button {
            color: white;
            background-color: #4975D6;
            border-style: none;
        }
        .st-key-styled button:hover {
            color: white;
            background-color: #6083D6;
            border-style: none;
        }
        .st-key-note_container {
            box-shadow: 3px 5px 15px 0px rgba(128, 128, 128, 0.245);
        }
        [class*="st-key-col"] {
            border-color: lightsteelblue;
        }
        .st-key-term_container {
            border-color: orange;
            background-color: floralwhite;
        }
        .st-key-term_container p{
            font-size: 14px;
        }
        .st-key-btn_-material-article--Records button {
            background-color: whitesmoke;
        }
        .st-key-mail button {
            text-decoration: underline;
        }
    </style>
    '''
    st.html(css)
