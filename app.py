import streamlit as st
import pandas as pd
import os

from excel_reader import read_excel
from diagram import create_diagram

# --------------------------
# Page Configuration
# --------------------------

st.set_page_config(
    page_title="BOMVision",
    page_icon="🏗️",
    layout="wide"
)

# --------------------------
# Sidebar
# --------------------------

st.sidebar.title("🏗️ BOMVision")

st.sidebar.markdown("""
### AI Architecture Generator

Upload a hierarchical Excel file to automatically generate a professional architecture diagram.

---
""")

st.sidebar.info(
    "Supported Formats\n\n"
    "• Parent → Component\n"
    "• Unlimited hierarchy columns"
)

# --------------------------
# Main Title
# --------------------------

st.title("🏗️ BOMVision")
st.subheader("AI Powered Architecture Diagram Generator")

st.markdown("---")

# --------------------------
# Upload
# --------------------------

uploaded_file = st.file_uploader(
    "📂 Upload Excel File",
    type=["xlsx"]
)

if uploaded_file:

    df = read_excel(uploaded_file)

    image = create_diagram(df)

    col1, col2 = st.columns([1,1])

    with col1:

        st.markdown("## 📋 Excel Preview")

        st.dataframe(
            df,
            use_container_width=True
        )

        st.markdown("## 📊 Statistics")

        st.metric(
            "Rows",
            len(df)
        )

        st.metric(
            "Columns",
            len(df.columns)
        )

        nodes = set()

        for _, row in df.iterrows():

            for value in row:

                if pd.notna(value):

                    nodes.add(str(value))

        st.metric(
            "Unique Components",
            len(nodes)
        )

    with col2:

        st.markdown("## 🏗️ Generated Architecture")

        st.image(
            image,
            use_container_width=True
        )

        with open(image, "rb") as file:

            st.download_button(
                "⬇️ Download PNG",
                file,
                file_name="architecture.png",
                mime="image/png"
            )

st.markdown("---")

st.caption("Developed using Streamlit • Pandas • Graphviz")