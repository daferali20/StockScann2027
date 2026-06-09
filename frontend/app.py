import streamlit as st
import pandas as pd
import requests
import time

st.set_page_config(
    page_title="Hot Money Flow",
    layout="wide"
)

st.title("🔥 Hot Money Flow Scanner")

placeholder = st.empty()

while True:

    trades = requests.get(
        "http://localhost:8000/big-trades"
    ).json()

    df = pd.DataFrame(trades)

    with placeholder.container():

        col1, col2 = st.columns([2,1])

        with col1:
            st.subheader("Large Trades")
            st.dataframe(
                df,
                use_container_width=True
            )

        with col2:
            st.metric(
                "Trades",
                len(df)
            )

    time.sleep(1)
