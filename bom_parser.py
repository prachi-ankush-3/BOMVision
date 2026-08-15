import pandas as pd
import re


# ==========================================================
# NUMBER EXTRACTION
# ==========================================================

def extract_number(value):
    """
    Extract the first numeric value from a cell.

    Examples:
        '82 x 332 x 8THK' -> 82
        '8THK'            -> 8
        '65 mm'           -> 65
        310               -> 310
    """

    if pd.isna(value):
        return None

    match = re.search(
        r"[-+]?\d*\.?\d+",
        str(value)
    )

    if match:
        return float(match.group())

    return None


# ==========================================================
# DIMENSION PARSER
# ==========================================================

def parse_dimensions(value):
    """
    Extract three dimensions from a BOM size string.

    Examples:

        82 x 332 x 8THK
        300 x 380 x 16THK

    Returns:

        first_dimension,
        second_dimension,
        thickness
    """

    if pd.isna(value):
        return None, None, None

    text = str(value).upper()

    numbers = re.findall(
        r"[-+]?\d*\.?\d+",
        text
    )

    if len(numbers) >= 3:

        return (
            float(numbers[0]),
            float(numbers[1]),
            float(numbers[2])
        )

    return None, None, None


# ==========================================================
# HOLE INFORMATION PARSER
# ==========================================================

def parse_hole_information(value):
    """
    Extract hole information from text.

    Examples:

        2-Ø14 HOLE
        2-Ø14 HOLE FOR M12 BOLT
        4-Ø18 HOLE FOR M16 BOLT
    """

    result = {
        "hole_count": None,
        "hole_diameter": None,
        "bolt": None
    }

    if pd.isna(value):
        return result

    text = str(value).upper()

    # ------------------------------------------------------
    # Hole count
    # ------------------------------------------------------

    count_match = re.search(
        r"(\d+)\s*[-X]?\s*[ØO]",
        text
    )

    if count_match:

        result["hole_count"] = int(
            count_match.group(1)
        )

    # ------------------------------------------------------
    # Hole diameter
    # ------------------------------------------------------

    diameter_match = re.search(
        r"[ØO]\s*(\d+(?:\.\d+)?)",
        text
    )

    if diameter_match:

        result["hole_diameter"] = float(
            diameter_match.group(1)
        )

    # ------------------------------------------------------
    # Bolt
    # ------------------------------------------------------

    bolt_match = re.search(
        r"\bM\d+(?:\.\d+)?\b",
        text
    )

    if bolt_match:

        result["bolt"] = bolt_match.group(0)

    return result


# ==========================================================
# SAFE VALUE CONVERSION
# ==========================================================

def safe_float(value):
    """
    Safely convert a value to float.

    None / empty / invalid values return None.
    """

    if value is None:
        return None

    if pd.isna(value):
        return None

    try:
        return float(value)

    except (ValueError, TypeError):
        return None


# ==========================================================
# COLUMN NORMALIZATION
# ==========================================================

def normalize_columns(df):
    """
    Normalize Excel column names.

    Example:

        'Part No.' -> 'part no.'
        'Hole Diameter (mm)' -> 'hole diameter (mm)'
    """

    df = df.copy()

    df.columns = [
        str(column)
        .strip()
        .lower()
        for column in df.columns
    ]

    return df


# ==========================================================
# FIND COLUMN
# ==========================================================

def find_column(df, possible_names):
    """
    Find the first matching column from a list of possible names.
    """

    for name in possible_names:

        normalized_name = (
            str(name)
            .strip()
            .lower()
        )

        if normalized_name in df.columns:

            return normalized_name

    return None


# ==========================================================
# GET VALUE FROM ROW
# ==========================================================

def get_row_value(row, df, possible_names):
    """
    Get a value from a row using multiple possible column names.
    """

    column = find_column(
        df,
        possible_names
    )

    if column is not None:

        return row[column]

    return None


# ==========================================================
# MAIN BOM PARSER
# ==========================================================

def parse_bom(df, part_no=None):
    """
    Parse one part from the BOM.

    The part number can be supplied:

        parse_bom(df, part_no=13)

    or:

        parse_bom(df, part_no=16)

    The function does NOT contain Part-16-specific
    hardcoded drawing values.
    """

    # ------------------------------------------------------
    # Validate dataframe
    # ------------------------------------------------------

    if df is None:

        raise ValueError(
            "BOM DataFrame is empty."
        )

    if df.empty:

        raise ValueError(
            "The uploaded Excel file contains no data."
        )

    # ------------------------------------------------------
    # Remove empty rows
    # ------------------------------------------------------

    df = df.dropna(
        how="all"
    ).copy()

    # ------------------------------------------------------
    # Normalize column names
    # ------------------------------------------------------

    df = normalize_columns(df)

    # ------------------------------------------------------
    # Find Part Number column
    # ------------------------------------------------------

    part_column = find_column(
        df,
        [
            "part no.",
            "part no",
            "part number",
            "item no.",
            "item no",
            "item number"
        ]
    )

    if part_column is None:

        raise ValueError(
            "Could not find the Part No. column in the Excel file."
        )

    # ------------------------------------------------------
    # Normalize Part Numbers
    # ------------------------------------------------------

    def normalize_part_number(value):

        if pd.isna(value):
            return None

        text = str(value).strip()

        # Handle Excel numeric values such as 13.0
        try:

            number = float(text)

            if number.is_integer():

                return str(
                    int(number)
                )

        except (ValueError, TypeError):
            pass

        return text

    df["_normalized_part_no"] = (
        df[part_column]
        .apply(normalize_part_number)
    )

    # ------------------------------------------------------
    # Automatically detect part number if not supplied
    # ------------------------------------------------------

    if part_no is None:

        valid_parts = (
            df["_normalized_part_no"]
            .dropna()
        )

        if valid_parts.empty:

            raise ValueError(
                "No valid Part Number was found in the BOM."
            )

        part_no = valid_parts.iloc[0]

    else:

        part_no = normalize_part_number(
            part_no
        )

    # ------------------------------------------------------
    # Find requested part
    # ------------------------------------------------------

    target = df[
        df["_normalized_part_no"] == str(part_no)
    ]

    if target.empty:

        available_parts = (
            df["_normalized_part_no"]
            .dropna()
            .unique()
            .tolist()
        )

        raise ValueError(
            f"Part No. {part_no} was not found in the BOM. "
            f"Available Part Nos: {available_parts}"
        )

    # ------------------------------------------------------
    # Get first matching row
    # ------------------------------------------------------

    row = target.iloc[0]

    # ======================================================
    # BASIC INFORMATION
    # ======================================================

    description = get_row_value(
        row,
        df,
        [
            "item description",
            "description",
            "item"
        ]
    )

    material = get_row_value(
        row,
        df,
        [
            "material / standard",
            "material",
            "standard"
        ]
    )

    size = get_row_value(
        row,
        df,
        [
            "size / length / thickness",
            "size",
            "dimensions",
            "dimension"
        ]
    )

    quantity = get_row_value(
        row,
        df,
        [
            "qty",
            "quantity"
        ]
    )

    # ======================================================
    # PARSE PLATE DIMENSIONS
    # ======================================================

    first_dimension, second_dimension, thickness = (
        parse_dimensions(size)
    )

    # Your BOM format stores:
    #
    # Part 16:
    # 82 x 332 x 8THK
    #
    # Part 13:
    # 380 x 300 x 16THK
    #
    # We use first dimension as width
    # and second dimension as height.

    plate_width = first_dimension
    plate_height = second_dimension

    # ======================================================
    # HOLE INFORMATION
    # ======================================================

    hole_count = get_row_value(
        row,
        df,
        [
            "hole count",
            "number of holes",
            "no. of holes"
        ]
    )

    hole_diameter = get_row_value(
        row,
        df,
        [
            "hole diameter (mm)",
            "hole diameter",
            "diameter"
        ]
    )

    bolt = get_row_value(
        row,
        df,
        [
            "bolt",
            "bolt / thread",
            "thread"
        ]
    )

    # ------------------------------------------------------
    # Try to get hole information from a callout column
    # ------------------------------------------------------

    callout = get_row_value(
        row,
        df,
        [
            "callout",
            "hole callout",
            "hole information"
        ]
    )

    # If the explicit Excel columns are empty,
    # try extracting the information from the callout.

    parsed_hole = parse_hole_information(
        callout
    )

    if hole_count is None:

        hole_count = parsed_hole[
            "hole_count"
        ]

    if hole_diameter is None:

        hole_diameter = parsed_hole[
            "hole_diameter"
        ]

    if bolt is None:

        bolt = parsed_hole[
            "bolt"
        ]

    # Convert numeric hole values

    hole_count = safe_float(
        hole_count
    )

    if hole_count is not None:

        hole_count = int(
            hole_count
        )

    hole_diameter = safe_float(
        hole_diameter
    )

    if bolt is not None:

        bolt = str(
            bolt
        ).strip()

    # ======================================================
    # PART 13 DIMENSIONS
    # ======================================================

    horizontal_left = get_row_value(
        row,
        df,
        [
            "horizontal offset left (mm)",
            "horizontal left offset",
            "left offset"
        ]
    )

    horizontal_spacing = get_row_value(
        row,
        df,
        [
            "horizontal hole spacing (mm)",
            "horizontal spacing",
            "hole spacing"
        ]
    )

    horizontal_right = get_row_value(
        row,
        df,
        [
            "horizontal offset right (mm)",
            "horizontal right offset",
            "right offset"
        ]
    )

    vertical_top = get_row_value(
        row,
        df,
        [
            "vertical offset top (mm)",
            "vertical top offset",
            "top offset"
        ]
    )

    vertical_spacing = get_row_value(
        row,
        df,
        [
            "vertical hole spacing (mm)",
            "vertical spacing"
        ]
    )

    vertical_bottom = get_row_value(
        row,
        df,
        [
            "vertical offset bottom (mm)",
            "vertical bottom offset",
            "bottom offset"
        ]
    )

    # ======================================================
    # PART 16 DIMENSION COMPATIBILITY
    # ======================================================

    dimension_35 = get_row_value(
        row,
        df,
        [
            "dimension 35 (mm)",
            "dimension 35",
            "35 mm"
        ]
    )

    dimension_11 = get_row_value(
        row,
        df,
        [
            "dimension 11 (mm)",
            "dimension 11",
            "11 mm"
        ]
    )

    dimension_310 = get_row_value(
        row,
        df,
        [
            "dimension 310 (mm)",
            "dimension 310",
            "310 mm"
        ]
    )

    # ======================================================
    # FALLBACK MAPPING
    # ======================================================
    #
    # This makes the parser compatible with the Part 13
    # and Part 16 Excel structures we created.
    #
    # Part 13:
    #
    # horizontal_left  = 65
    # horizontal_space = 250
    # horizontal_right = 65
    #
    # vertical_top     = 75
    # vertical_space   = 150
    # vertical_bottom  = 75
    #
    # Part 16:
    #
    # dimension_35 = 35
    # dimension_11 = 11
    # dimension_310 = 310
    #
    # ======================================================

    horizontal_left = safe_float(
        horizontal_left
    )

    horizontal_spacing = safe_float(
        horizontal_spacing
    )

    horizontal_right = safe_float(
        horizontal_right
    )

    vertical_top = safe_float(
        vertical_top
    )

    vertical_spacing = safe_float(
        vertical_spacing
    )

    vertical_bottom = safe_float(
        vertical_bottom
    )

    dimension_35 = safe_float(
        dimension_35
    )

    dimension_11 = safe_float(
        dimension_11
    )

    dimension_310 = safe_float(
        dimension_310
    )

    # ------------------------------------------------------
    # If Part 16 uses the 35 / 11 / 310 fields,
    # map them to the general dimension fields too.
    # ------------------------------------------------------

    if horizontal_left is None:

        horizontal_left = dimension_35

    if vertical_top is None:

        vertical_top = dimension_11

    if vertical_spacing is None:

        vertical_spacing = dimension_310

    # ======================================================
    # OVERALL DIMENSIONS
    # ======================================================

    overall_width = plate_width
    overall_height = plate_height

    # ======================================================
    # SCALE
    # ======================================================

    scale = get_row_value(
        row,
        df,
        [
            "scale",
            "drawing scale"
        ]
    )

    if scale is not None:

        scale = str(
            scale
        ).strip()

    # ======================================================
    # DRAWING CALLOUT
    # ======================================================

    callout_reference = get_row_value(
        row,
        df,
        [
            "callout",
            "callout reference",
            "reference"
        ]
    )

    if callout_reference is not None:

        callout_reference = str(
            callout_reference
        ).strip()

    # ======================================================
    # BUILD FINAL PART DICTIONARY
    # ======================================================

    part = {

        # ----------------------------------------------
        # Basic information
        # ----------------------------------------------

        "part_no": part_no,

        "component_type":
            str(description).strip()
            if description is not None
            and not pd.isna(description)
            else None,

        "material":
            str(material).strip()
            if material is not None
            and not pd.isna(material)
            else None,

        "quantity":
            quantity,

        # ----------------------------------------------
        # Main dimensions
        # ----------------------------------------------

        "width":
            plate_width,

        "height":
            plate_height,

        "thickness":
            thickness,

        "overall_width":
            overall_width,

        "overall_height":
            overall_height,

        "source_size":
            str(size).strip()
            if size is not None
            and not pd.isna(size)
            else None,

        # ----------------------------------------------
        # Hole information
        # ----------------------------------------------

        "hole_count":
            hole_count,

        "hole_diameter":
            hole_diameter,

        "bolt":
            bolt,

        # ----------------------------------------------
        # Horizontal dimensions
        # ----------------------------------------------

        "horizontal_left":
            horizontal_left,

        "horizontal_spacing":
            horizontal_spacing,

        "horizontal_right":
            horizontal_right,

        # ----------------------------------------------
        # Vertical dimensions
        # ----------------------------------------------

        "vertical_top":
            vertical_top,

        "vertical_spacing":
            vertical_spacing,

        "vertical_bottom":
            vertical_bottom,

        # ----------------------------------------------
        # Part 16 compatibility names
        # ----------------------------------------------

        "dimension_35":
            dimension_35,

        "dimension_11":
            dimension_11,

        "dimension_310":
            dimension_310,

        # ----------------------------------------------
        # Drawing metadata
        # ----------------------------------------------

        "scale":
            scale,

        "callout":
            callout_reference
    }

    return part


# ==========================================================
# PRINT PART
# ==========================================================

def print_part(part):
    """
    Print parsed information in a readable format.
    """

    print(
        "\n========== PART INFORMATION =========="
    )

    for key, value in part.items():

        print(
            f"{key:25}: {value}"
        )

    print(
        "=======================================\n"
    )


# ==========================================================
# TESTING
# ==========================================================

if __name__ == "__main__":

    # ------------------------------------------------------
    # Change this to the Excel file you want to test.
    # ------------------------------------------------------

    excel_file = "BOMVision_Part13.xlsx"

    # ------------------------------------------------------
    # Read Excel
    # ------------------------------------------------------

    df = pd.read_excel(
        excel_file
    )

    # ------------------------------------------------------
    # Automatically detect first Part Number
    # ------------------------------------------------------

    part = parse_bom(
        df
    )

    # ------------------------------------------------------
    # Display parsed information
    # ------------------------------------------------------

    print_part(
        part
    )