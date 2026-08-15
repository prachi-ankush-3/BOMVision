import streamlit as st
import pandas as pd
import os

from bom_parser import parse_bom
from diagram import create_engineering_drawing


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

st.subheader("BOM Excel → Engineering Drawing")

st.write(
    "Upload a BOM Excel file. The application will detect "
    "the Part Number and extract the required engineering data."
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
        # Detect Part Number automatically
        # --------------------------------------------------

        part_columns = [
            "Part No.",
            "Part No",
            "Item No.",
            "Item No",
            "Item Number",
            "Part Number"
        ]

        detected_column = None

        # First try exact column names
        for column in part_columns:

            if column in df.columns:
                detected_column = column
                break

        # If not found, try case-insensitive matching
        if detected_column is None:

            normalized = {
                str(c).strip().lower(): c
                for c in df.columns
            }

            for column in [
                "part no.",
                "part no",
                "item no.",
                "item no",
                "item number",
                "part number"
            ]:

                if column in normalized:
                    detected_column = normalized[column]
                    break

        if detected_column is None:

            raise ValueError(
                "Could not find the Part No. column in the Excel file."
            )

        # --------------------------------------------------
        # Get first valid Part Number
        # --------------------------------------------------

        part_values = (
            df[detected_column]
            .dropna()
            .astype(str)
            .str.strip()
        )

        if part_values.empty:

            raise ValueError(
                "No Part Number was found in the Excel file."
            )

        # Convert first part number to integer
        try:

            part_no = int(
                float(
                    part_values.iloc[0]
                )
            )

        except (ValueError, TypeError):

            raise ValueError(
                f"Invalid Part Number found: "
                f"{part_values.iloc[0]}"
            )

        # --------------------------------------------------
        # Show detected Part
        # --------------------------------------------------

        st.subheader(
            f"🔍 Part No. {part_no} Analysis"
        )

        st.info(
            f"Detected Part Number: {part_no}"
        )

        # --------------------------------------------------
        # Parse detected part
        # --------------------------------------------------

        part = parse_bom(
            df,
            part_no=part_no
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
            f"**Number of Holes:** "
            f"{part['hole_count']}"
        )

        st.write(
            f"**Hole Diameter:** "
            f"Ø{part['hole_diameter']} mm"
        )

        st.write(
            f"**Bolt:** "
            f"{part['bolt']}"
        )

        # --------------------------------------------------
        # Drawing dimensions
        # --------------------------------------------------

        st.write("### Drawing Dimensions")

        if part.get("dimension_35") is not None:

            st.write(
                f"**Horizontal Offset:** "
                f"{part['dimension_35']} mm"
            )

        if part.get("dimension_11") is not None:

            st.write(
                f"**Vertical Offset:** "
                f"{part['dimension_11']} mm"
            )

        if part.get("dimension_310") is not None:

            st.write(
                f"**Hole Spacing:** "
                f"{part['dimension_310']} mm"
            )

        if part.get("horizontal_spacing") is not None:

            st.write(
                f"**Horizontal Hole Spacing:** "
                f"{part['horizontal_spacing']} mm"
            )

        if part.get("vertical_spacing") is not None:

            st.write(
                f"**Vertical Hole Spacing:** "
                f"{part['vertical_spacing']} mm"
            )

        # --------------------------------------------------
        # Generate Drawing
        # --------------------------------------------------

        st.divider()

        generate = st.button(
            f"📐 Generate Part {part_no} Drawing",
            type="primary"
        )

        if generate:

            output_file = (
                f"Part_{part_no}_Drawing.png"
            )

            # ----------------------------------------------
            # Automatically select drawing based on
            # detected Part Number
            # ----------------------------------------------

            create_engineering_drawing(
                part,
                output_file
            )

            # ----------------------------------------------
            # Display drawing
            # ----------------------------------------------

            st.success(
                f"Part No. {part_no} drawing "
                f"generated successfully!"
            )

            st.subheader(
                "📐 Generated Engineering Drawing"
            )

            st.image(
                output_file,
                caption=f"Part No. {part_no}",
                use_container_width=True
            )

            # ----------------------------------------------
            # Download
            # ----------------------------------------------

            if os.path.exists(output_file):

                with open(
                    output_file,
                    "rb"
                ) as file:

                    st.download_button(
                        label="⬇️ Download Drawing",
                        data=file,
                        file_name=output_file,
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