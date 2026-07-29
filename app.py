import streamlit as st
from excel_reader import read_excel
from diagram import create_diagram

st.title("AI BOM Architecture Generator")

uploaded_file = st.file_uploader(
    "Upload BOM Excel",
    type=["xlsx"]
)

if uploaded_file:

    df = read_excel(uploaded_file)

    st.write(df)

    image = create_diagram(df)

    st.image(image)