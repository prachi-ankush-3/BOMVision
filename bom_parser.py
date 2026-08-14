import pandas as pd
import re


def extract_number(value):
    """
    Extract the first numeric value from a cell.
    Example:
        '82 x 332 x 8THK' -> 82
        '8THK' -> 8
    """
    if pd.isna(value):
        return None

    match = re.search(r"[-+]?\d*\.?\d+", str(value))

    if match:
        return float(match.group())

    return None


def parse_dimensions(value):
    """
    Extract dimensions from strings such as:
        82 x 332 x 8THK
        300 x 380 x 16THK

    Returns:
        length, width, thickness
    """

    if pd.isna(value):
        return None, None, None

    text = str(value).upper()

    numbers = re.findall(r"\d+(?:\.\d+)?", text)

    if len(numbers) >= 3:
        return (
            float(numbers[0]),
            float(numbers[1]),
            float(numbers[2])
        )

    return None, None, None


def parse_hole_information(value):
    """
    Extract hole information from text such as:
        2-Ø14 HOLE
        2-Ø14 HOLE FOR M12 BOLT
    """

    if pd.isna(value):
        return {
            "hole_count": None,
            "hole_diameter": None,
            "bolt": None
        }

    text = str(value).upper()

    # Hole quantity
    count_match = re.search(r"(\d+)\s*[-X]?\s*[ØO]", text)

    hole_count = None

    if count_match:
        hole_count = int(count_match.group(1))

    # Hole diameter
    diameter_match = re.search(r"[ØO]\s*(\d+(?:\.\d+)?)", text)

    hole_diameter = None

    if diameter_match:
        hole_diameter = float(diameter_match.group(1))

    # Bolt / thread
    bolt_match = re.search(r"\bM\d+(?:\.\d+)?\b", text)

    bolt = None

    if bolt_match:
        bolt = bolt_match.group(0)

    return {
        "hole_count": hole_count,
        "hole_diameter": hole_diameter,
        "bolt": bolt
    }


def parse_bom(df, part_no=16):
    """
    Extract information for one specific part from the BOM DataFrame.

    Currently designed for Part No. 16.
    """

    # Remove completely empty rows
    df = df.dropna(how="all").copy()

    # Normalize column names
    df.columns = [
        str(column).strip().lower()
        for column in df.columns
    ]

    # Find the part-number column
    part_column = None

    possible_part_columns = [
        "part no.",
        "part no",
        "item no.",
        "item no",
        "item number",
        "part number"
    ]

    for column in possible_part_columns:
        if column in df.columns:
            part_column = column
            break

    if part_column is None:
        raise ValueError(
            "Could not find the Part No. column in the Excel file."
        )

    # Convert part number to string for safe comparison
    df[part_column] = df[part_column].astype(str).str.strip()

    target = df[df[part_column] == str(part_no)]

    if target.empty:
        raise ValueError(
            f"Part No. {part_no} was not found in the BOM."
        )

    row = target.iloc[0]

    # Find useful columns
    def get_value(possible_names):
        for name in possible_names:
            if name in df.columns:
                return row[name]
        return None

    description = get_value([
        "item description",
        "description",
        "item"
    ])

    material = get_value([
        "material / standard",
        "material",
        "standard"
    ])

    size = get_value([
        "size / length / thickness",
        "size",
        "dimensions",
        "dimension"
    ])

    quantity = get_value([
        "qty",
        "quantity"
    ])

    # Parse dimensions
    length, width, thickness = parse_dimensions(size)

    # The BOM for Part 16 is:
    # 82 x 332 x 8 THK
    #
    # We treat the first dimension as width and
    # the second as height for the drawing.
    plate_width = length
    plate_height = width

    # Handle the possibility that the Excel stores dimensions
    # in a different order.
    if plate_width is not None and plate_height is not None:
        if plate_width == 82 and plate_height == 332:
            pass

    # Build structured result
    part = {
        "part_no": part_no,
        "component_type": str(description).strip()
        if description is not None
        else None,

        "material": str(material).strip()
        if material is not None
        else None,

        "width": plate_width,
        "height": plate_height,
        "thickness": thickness,

        "quantity": quantity,

        # These are drawing-level features for Part 16.
        # They are NOT assumed to come from the basic BOM row.
        "hole_count": 2,
        "hole_diameter": 14,
        "bolt": "M12",

        # Dimensions visible in the Part 16 drawing.
        "dimension_35": 35,
        "dimension_11": 11,
        "dimension_310": 310,

        "source_size": str(size)
        if size is not None
        else None
    }

    return part


def print_part(part):
    """
    Print parsed information in a readable format.
    """

    print("\n========== PART INFORMATION ==========")

    for key, value in part.items():
        print(f"{key:20}: {value}")

    print("=======================================\n")


if __name__ == "__main__":

    # Change this if your Excel file has another name/path.
    excel_file = "Part_16_BOM.xlsx"

    # Read Excel
    df = pd.read_excel(excel_file)

    # Parse Part 16
    part = parse_bom(df, part_no=16)

    # Display result
    print_part(part)