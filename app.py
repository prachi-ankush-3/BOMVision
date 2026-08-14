import streamlit as st
import pandas as pd
import os

from bom_parser import parse_bom
from diagram import create_part16_drawing


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="BOM Analysis using AI",
    page_icon="📐",
    layout="wide"
)


# ==========================================================
# TITLE
# ==========================================================

st.title("BOM Analysis using AI")
st.subheader("BOM Excel → Part 16 Engineering Drawing")


st.write(
    "Upload the BOM Excel file. The application will read "
    "Part No. 16 and generate its engineering drawing."
)


# ==========================================================
# FILE UPLOAD
# ==========================================================

uploaded_file = st.file_uploader(
    "Upload BOM Excel File",
    type=["xlsx", "xls"]
)


# ==========================================================
# PROCESS FILE
# ==========================================================

if uploaded_file is not None:

    try:

        # --------------------------------------------------
        # Read Excel
        # --------------------------------------------------

        df = pd.read_excel(uploaded_file)

        st.success("Excel file uploaded successfully.")

        # --------------------------------------------------
        # Show BOM
        # --------------------------------------------------

        st.subheader("📋 BOM Data")

        st.dataframe(
            df,
            use_container_width=True
        )

        # --------------------------------------------------
        # Parse Part 16
        # --------------------------------------------------

        st.subheader("🔍 Part No. 16 Analysis")

        part = parse_bom(
            df,
            part_no=16
        )

        # --------------------------------------------------
        # Display extracted information
        # --------------------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            st.write("### Basic Information")

            st.write(
                f"**Part Number:** {part['part_no']}"
            )

            st.write(
                f"**Component:** {part['component_type']}"
            )

            st.write(
                f"**Material:** {part['material']}"
            )

            st.write(
                f"**Quantity:** {part['quantity']}"
            )

        with col2:

            st.write("### Dimensions")

            st.write(
                f"**Width:** {part['width']} mm"
            )

            st.write(
                f"**Height:** {part['height']} mm"
            )

            st.write(
                f"**Thickness:** {part['thickness']} mm"
            )

            st.write(
                f"**Source Size:** {part['source_size']}"
            )

        # --------------------------------------------------
        # Hole information
        # --------------------------------------------------

        st.write("### Hole Information")

        st.write(
            f"**Number of Holes:** {part['hole_count']}"
        )

        st.write(
            f"**Hole Diameter:** Ø{part['hole_diameter']} mm"
        )

        st.write(
            f"**Bolt:** {part['bolt']}"
        )

        # --------------------------------------------------
        # Drawing dimensions
        # --------------------------------------------------

        st.write("### Drawing Dimensions")

        st.write(
            f"**35 mm:** {part['dimension_35']} mm"
        )

        st.write(
            f"**11 mm:** {part['dimension_11']} mm"
        )

        st.write(
            f"**310 mm:** {part['dimension_310']} mm"
        )

        # --------------------------------------------------
        # Generate Drawing Button
        # --------------------------------------------------

        st.divider()

        generate = st.button(
            "📐 Generate Part 16 Drawing",
            type="primary"
        )

        if generate:

            output_file = "Part_16_Drawing.png"

            # ----------------------------------------------
            # Generate drawing
            # ----------------------------------------------

            create_part16_drawing(
                part,
                output_file
            )

            # ----------------------------------------------
            # Display drawing
            # ----------------------------------------------

            st.success(
                "Part No. 16 drawing generated successfully!"
            )

            st.subheader(
                "📐 Generated Architecture / Engineering Drawing"
            )

            st.image(
                output_file,
                caption="Part No. 16",
                use_container_width=True
            )

            # ----------------------------------------------
            # Download button
            # ----------------------------------------------

            if os.path.exists(output_file):

                with open(
                    output_file,
                    "rb"
                ) as file:

                    st.download_button(
                        label="⬇️ Download Drawing",
                        data=file,
                        file_name="Part_16_Drawing.png",
                        mime="image/png"
                    )


    # ======================================================
    # ERROR HANDLING
    # ======================================================

    except Exception as e:

        st.error(
            f"An error occurred: {e}"
        )

        st.exception(e)