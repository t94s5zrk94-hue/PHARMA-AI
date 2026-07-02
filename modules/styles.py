import streamlit as st

def load_css():

    st.markdown("""
    <style>

    /* App Background */
    .main {
        background-color: #0E1117;
    }

    /* Medicine Card */
    div[data-testid="stMetric"]{
        background-color:#1E1E1E;
        border:1px solid #333333;
        border-radius:12px;
        padding:18px;
        box-shadow:0px 2px 8px rgba(0,0,0,0.25);
    }

    div[data-testid="stMetric"]:hover{
        border:1px solid #2196F3;
    }

    /* Metric Label */
    div[data-testid="stMetric"] label{
        color:#BBBBBB !important;
    }

    /* Metric Value */
    div[data-testid="stMetric"] div{
        color:white !important;
    }

    </style>
    """, unsafe_allow_html=True)