import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle


# ==========================================================
# COMMON HELPERS
# ==========================================================

def safe_float(value, default=0):
    """Safely convert value to float."""
    if value is None:
        return default

    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def safe_int(value, default=0):
    """Safely convert value to int."""
    if value is None:
        return default

    try:
        return int(float(value))
    except (ValueError, TypeError):
        return default


def slash_tick(ax, x, y, size=5, linewidth=1.1):
    """Engineering drawing slash dimension marker."""
    ax.plot(
        [x - size, x + size],
        [y - size, y + size],
        color="black",
        linewidth=linewidth,
        solid_capstyle="butt"
    )


def setup_axes(ax, xmin, xmax, ymin, ymax):
    """Common drawing setup."""
    ax.set_aspect("equal")
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.axis("off")


# ==========================================================
# PART 13 DRAWING
# ==========================================================

def create_part13_drawing(
    part,
    output_file="Part_13_Drawing.png"
):
    """
    BOMVision - Part No. 13 Engineering Drawing

    Dimensions:
        Width       = 380 mm
        Height      = 300 mm
        Thickness   = 16 mm

        Holes       = 4
        Hole dia    = 18 mm
        Bolt        = M16

        Horizontal:
            65 - 250 - 65

        Vertical:
            75 - 150 - 75

        Callout:
            F1

        Scale:
            1:4
    """

    # ======================================================
    # 1. READ BOM DATA
    # ======================================================

    part_no = str(part.get("part_no") or 13)

    width = safe_float(
        part.get("width"),
        380
    )

    height = safe_float(
        part.get("height"),
        300
    )

    thickness = safe_float(
        part.get("thickness"),
        16
    )

    hole_count = safe_int(
        part.get("hole_count"),
        4
    )

    hole_diameter = safe_float(
        part.get("hole_diameter"),
        18
    )

    bolt = str(
        part.get("bolt") or "M16"
    )

    horizontal_left = safe_float(
        part.get("horizontal_left"),
        65
    )

    horizontal_spacing = safe_float(
        part.get("horizontal_spacing"),
        250
    )

    horizontal_right = safe_float(
        part.get("horizontal_right"),
        65
    )

    vertical_top = safe_float(
        part.get("vertical_top"),
        75
    )

    vertical_spacing = safe_float(
        part.get("vertical_spacing"),
        150
    )

    vertical_bottom = safe_float(
        part.get("vertical_bottom"),
        75
    )

    scale = str(
        part.get("scale") or "1:4"
    )

    callout = str(
        part.get("callout") or "F1"
    )

    # ======================================================
    # 2. MAIN PLATE
    # ======================================================

    x_left = 0
    x_right = width

    y_bottom = 0
    y_top = height

    chamfer = min(
        8,
        width / 20,
        height / 20
    )

    # ======================================================
    # 3. HOLE POSITIONS
    # ======================================================

    left_hole_x = horizontal_left

    right_hole_x = (
        horizontal_left +
        horizontal_spacing
    )

    bottom_hole_y = vertical_bottom

    top_hole_y = (
        vertical_bottom +
        vertical_spacing
    )

    hole_radius = hole_diameter / 2

    hole_positions = []

    if hole_count >= 1:
        hole_positions.append(
            (left_hole_x, bottom_hole_y)
        )

    if hole_count >= 2:
        hole_positions.append(
            (right_hole_x, bottom_hole_y)
        )

    if hole_count >= 3:
        hole_positions.append(
            (left_hole_x, top_hole_y)
        )

    if hole_count >= 4:
        hole_positions.append(
            (right_hole_x, top_hole_y)
        )

    # ======================================================
    # 4. FIGURE
    # ======================================================

    fig, ax = plt.subplots(
        figsize=(13, 10),
        dpi=200
    )

    # ======================================================
    # 5. MAIN PLATE
    # ======================================================

    plate_points = [
        (x_left + chamfer, y_top),
        (x_right - chamfer, y_top),
        (x_right, y_top - chamfer),
        (x_right, y_bottom + chamfer),
        (x_right - chamfer, y_bottom),
        (x_left + chamfer, y_bottom),
        (x_left, y_bottom + chamfer),
        (x_left, y_top - chamfer)
    ]

    plate = Polygon(
        plate_points,
        closed=True,
        fill=False,
        edgecolor="black",
        linewidth=1.4,
        joinstyle="miter"
    )

    ax.add_patch(plate)

    # ======================================================
    # 6. HOLES
    # ======================================================

    for hx, hy in hole_positions:

        circle = Circle(
            (hx, hy),
            hole_radius,
            fill=False,
            edgecolor="black",
            linewidth=1.1
        )

        ax.add_patch(circle)

        center_size = min(
            14,
            hole_diameter * 0.9
        )

        # Horizontal center line
        ax.plot(
            [
                hx - center_size,
                hx + center_size
            ],
            [hy, hy],
            color="black",
            linewidth=0.45
        )

        # Vertical center line
        ax.plot(
            [hx, hx],
            [
                hy - center_size,
                hy + center_size
            ],
            color="black",
            linewidth=0.45
        )

    # ======================================================
    # 7. OVERALL WIDTH - 380
    # ======================================================

    width_dim_y = y_top + 55

    ax.plot(
        [x_left, x_left],
        [y_top, width_dim_y],
        color="black",
        linewidth=0.65
    )

    ax.plot(
        [x_right, x_right],
        [y_top, width_dim_y],
        color="black",
        linewidth=0.65
    )

    ax.plot(
        [x_left, x_right],
        [width_dim_y, width_dim_y],
        color="black",
        linewidth=0.85
    )

    slash_tick(
        ax,
        x_left,
        width_dim_y
    )

    slash_tick(
        ax,
        x_right,
        width_dim_y
    )

    ax.text(
        width / 2,
        width_dim_y + 9,
        f"{width:g}",
        ha="center",
        va="bottom",
        fontsize=14
    )

    # ======================================================
    # 8. HORIZONTAL 65 - 250 - 65
    # ======================================================

    hole_dim_y = y_top + 18

    # Extension lines
    for x in [
        x_left,
        left_hole_x,
        right_hole_x,
        x_right
    ]:
        ax.plot(
            [x, x],
            [y_top, hole_dim_y],
            color="black",
            linewidth=0.65
        )

    # ------------------------------------------------------
    # LEFT 65
    # ------------------------------------------------------

    ax.plot(
        [x_left, left_hole_x],
        [hole_dim_y, hole_dim_y],
        color="black",
        linewidth=0.8
    )

    slash_tick(
        ax,
        x_left,
        hole_dim_y
    )

    slash_tick(
        ax,
        left_hole_x,
        hole_dim_y
    )

    ax.text(
        (x_left + left_hole_x) / 2,
        hole_dim_y + 7,
        f"{horizontal_left:g}",
        ha="center",
        va="bottom",
        fontsize=12
    )

    # ------------------------------------------------------
    # MIDDLE 250
    # ------------------------------------------------------

    ax.plot(
        [left_hole_x, right_hole_x],
        [hole_dim_y, hole_dim_y],
        color="black",
        linewidth=0.8
    )

    slash_tick(
        ax,
        left_hole_x,
        hole_dim_y
    )

    slash_tick(
        ax,
        right_hole_x,
        hole_dim_y
    )

    ax.text(
        (left_hole_x + right_hole_x) / 2,
        hole_dim_y + 7,
        f"{horizontal_spacing:g}",
        ha="center",
        va="bottom",
        fontsize=12
    )

    # ------------------------------------------------------
    # RIGHT 65
    # ------------------------------------------------------

    ax.plot(
        [right_hole_x, x_right],
        [hole_dim_y, hole_dim_y],
        color="black",
        linewidth=0.8
    )

    slash_tick(
        ax,
        right_hole_x,
        hole_dim_y
    )

    slash_tick(
        ax,
        x_right,
        hole_dim_y
    )

    ax.text(
        (right_hole_x + x_right) / 2,
        hole_dim_y + 7,
        f"{horizontal_right:g}",
        ha="center",
        va="bottom",
        fontsize=12
    )

    # ======================================================
    # 9. VERTICAL DIMENSIONS
    #
    #       75
    #       |
    #      300  <-- overall height
    #       |
    #      150  <-- hole spacing
    #       |
    #       75
    #
    # These are separated so 300 and 150
    # do NOT overlap.
    # ======================================================

    # Main vertical dimension position
    vertical_dim_x = x_right + 55

    # Separate overall height dimension
    overall_height_x = x_right + 105

    # ------------------------------------------------------
    # EXTENSION LINES
    # ------------------------------------------------------

    # Top edge
    ax.plot(
        [x_right, overall_height_x],
        [y_top, y_top],
        color="black",
        linewidth=0.65
    )

    # Top hole
    ax.plot(
        [x_right, overall_height_x],
        [top_hole_y, top_hole_y],
        color="black",
        linewidth=0.65
    )

    # Bottom hole
    ax.plot(
        [x_right, overall_height_x],
        [bottom_hole_y, bottom_hole_y],
        color="black",
        linewidth=0.65
    )

    # Bottom edge
    ax.plot(
        [x_right, overall_height_x],
        [y_bottom, y_bottom],
        color="black",
        linewidth=0.65
    )

    # ------------------------------------------------------
    # 75 - TOP
    # ------------------------------------------------------

    ax.plot(
        [vertical_dim_x, vertical_dim_x],
        [top_hole_y, y_top],
        color="black",
        linewidth=0.8
    )

    slash_tick(
        ax,
        vertical_dim_x,
        top_hole_y
    )

    slash_tick(
        ax,
        vertical_dim_x,
        y_top
    )

    ax.text(
        vertical_dim_x + 10,
        (top_hole_y + y_top) / 2,
        f"{vertical_top:g}",
        rotation=90,
        ha="center",
        va="center",
        fontsize=12
    )

    # ------------------------------------------------------
    # 150 - HOLE SPACING
    # ------------------------------------------------------

    ax.plot(
        [vertical_dim_x, vertical_dim_x],
        [bottom_hole_y, top_hole_y],
        color="black",
        linewidth=0.8
    )

    slash_tick(
        ax,
        vertical_dim_x,
        bottom_hole_y
    )

    slash_tick(
        ax,
        vertical_dim_x,
        top_hole_y
    )

    ax.text(
        vertical_dim_x + 10,
        (bottom_hole_y + top_hole_y) / 2,
        f"{vertical_spacing:g}",
        rotation=90,
        ha="center",
        va="center",
        fontsize=12
    )

    # ------------------------------------------------------
    # 75 - BOTTOM
    # ------------------------------------------------------

    ax.plot(
        [vertical_dim_x, vertical_dim_x],
        [y_bottom, bottom_hole_y],
        color="black",
        linewidth=0.8
    )

    slash_tick(
        ax,
        vertical_dim_x,
        y_bottom
    )

    slash_tick(
        ax,
        vertical_dim_x,
        bottom_hole_y
    )

    ax.text(
        vertical_dim_x + 10,
        (y_bottom + bottom_hole_y) / 2,
        f"{vertical_bottom:g}",
        rotation=90,
        ha="center",
        va="center",
        fontsize=12
    )

    # ------------------------------------------------------
    # OVERALL HEIGHT - 300
    #
    # Put it farther to the right so it cannot merge
    # with the 150 dimension.
    # ------------------------------------------------------

    ax.plot(
        [overall_height_x, overall_height_x],
        [y_bottom, y_top],
        color="black",
        linewidth=0.85
    )

    slash_tick(
        ax,
        overall_height_x,
        y_top
    )

    slash_tick(
        ax,
        overall_height_x,
        y_bottom
    )

    ax.text(
        overall_height_x + 11,
        height / 2,
        f"{height:g}",
        rotation=90,
        ha="center",
        va="center",
        fontsize=14
    )

    # ======================================================
    # 10. THICKNESS NOTE
    # ======================================================

    thickness_x = (
        x_left +
        width * 0.62
    )

    thickness_y = (
        y_bottom +
        height * 0.48
    )

    ax.text(
        thickness_x,
        thickness_y,
        f"{thickness:g} THK.",
        fontsize=13,
        ha="center",
        va="center"
    )

    # ======================================================
    # 11. HOLE CALLOUT
    #
    # IMPORTANT:
    # The callout is now BELOW the drawing.
    #
    # Required:
    # 4-Ø18 HOLE
    # FOR M16 BOLT
    # F1
    # ======================================================

    callout_x = x_right - 20

    # Position well below the 75 dimension
    callout_y = y_bottom - 38

    # Main callout text
    ax.text(
        callout_x,
        callout_y,
        f"{hole_count}-Ø{hole_diameter:g} HOLE",
        ha="left",
        va="center",
        fontsize=13
    )

    # Second line
    ax.text(
        callout_x,
        callout_y - 22,
        f"FOR {bolt} BOLT",
        ha="left",
        va="center",
        fontsize=13
    )

    # ======================================================
    # F1 CIRCLE
    # ======================================================

    f1_x = callout_x + 120
    f1_y = callout_y - 11

    circle_f1 = Circle(
        (f1_x, f1_y),
        10,
        fill=False,
        edgecolor="black",
        linewidth=1.0
    )

    ax.add_patch(circle_f1)

    ax.text(
        f1_x,
        f1_y,
        callout,
        ha="center",
        va="center",
        fontsize=10
    )

    # ======================================================
    # F1 LEADER LINE
    #
    # Connect F1 to the lower-right hole.
    # ======================================================

    leader_start_x = f1_x - 10
    leader_start_y = f1_y

    leader_end_x = right_hole_x + 5
    leader_end_y = bottom_hole_y - 5

    ax.plot(
        [
            leader_start_x,
            leader_end_x
        ],
        [
            leader_start_y,
            leader_end_y
        ],
        color="black",
        linewidth=0.95
    )

    # Small arrow/endpoint at hole
    ax.plot(
        [
            leader_end_x - 4,
            leader_end_x
        ],
        [
            leader_end_y + 2,
            leader_end_y
        ],
        color="black",
        linewidth=0.95
    )

    ax.plot(
        [
            leader_end_x - 2,
            leader_end_x
        ],
        [
            leader_end_y + 5,
            leader_end_y
        ],
        color="black",
        linewidth=0.95
    )

    # ======================================================
    # 12. PART NUMBER
    #
    # No underline.
    # No extra lines below it.
    # ======================================================

    part_y = y_bottom - 85

    ax.text(
        x_left,
        part_y,
        f"PART NO.{part_no}",
        ha="left",
        va="top",
        fontsize=16,
        fontweight="bold"
    )

    # ======================================================
    # 13. SCALE
    #
    # No underline.
    # No extra lines below it.
    # ======================================================

    scale_y = y_bottom - 112

    ax.text(
        x_left,
        scale_y,
        f"(SCALE  {scale})",
        ha="left",
        va="top",
        fontsize=14
    )

    # ======================================================
    # 14. FINAL VIEW
    # ======================================================

    setup_axes(
        ax,
        -35,
        width + 185,
        -135,
        height + 100
    )

    plt.savefig(
        output_file,
        dpi=200,
        facecolor="white",
        bbox_inches="tight",
        pad_inches=0.08
    )

    plt.close(fig)

    return output_file


# ==========================================================
# PART 16 DRAWING
# ==========================================================

def create_part16_drawing(
    part,
    output_file="Part_16_Drawing.png"
):
    """
    BOMVision - Part No. 16 Engineering Drawing.
    """

    # ======================================================
    # READ BOM DATA
    # ======================================================

    part_no = str(
        part.get("part_no") or 16
    )

    width = safe_float(
        part.get("width"),
        82
    )

    height = safe_float(
        part.get("height"),
        332
    )

    thickness = safe_float(
        part.get("thickness"),
        8
    )

    hole_count = safe_int(
        part.get("hole_count"),
        2
    )

    hole_diameter = safe_float(
        part.get("hole_diameter"),
        14
    )

    dimension_35 = safe_float(
        part.get("dimension_35"),
        35
    )

    dimension_11 = safe_float(
        part.get("dimension_11"),
        11
    )

    dimension_310 = safe_float(
        part.get("dimension_310"),
        310
    )

    bolt = str(
        part.get("bolt") or "M12"
    )

    # ======================================================
    # COORDINATES
    # ======================================================

    x_left = 0
    x_right = width

    y_bottom = 0
    y_top = height

    chamfer = 8

    hole_x = dimension_35

    bottom_hole_y = dimension_11

    top_hole_y = (
        height -
        dimension_11
    )

    hole_radius = (
        hole_diameter / 2
    )

    # ======================================================
    # FIGURE
    # ======================================================

    fig, ax = plt.subplots(
        figsize=(7.4, 12.5),
        dpi=200
    )

    # ======================================================
    # MAIN PLATE
    # ======================================================

    plate_points = [
        (x_left + chamfer, y_top),
        (x_right, y_top),
        (x_right, y_bottom),
        (x_left + chamfer, y_bottom),
        (x_left, y_bottom + chamfer),
        (x_left, y_top - chamfer)
    ]

    plate = Polygon(
        plate_points,
        closed=True,
        fill=False,
        edgecolor="black",
        linewidth=1.35,
        joinstyle="miter"
    )

    ax.add_patch(plate)

    # ======================================================
    # HOLES
    # ======================================================

    hole_positions = []

    if hole_count >= 1:
        hole_positions.append(
            (
                hole_x,
                bottom_hole_y
            )
        )

    if hole_count >= 2:
        hole_positions.append(
            (
                hole_x,
                top_hole_y
            )
        )

    for hx, hy in hole_positions:

        circle = Circle(
            (hx, hy),
            hole_radius,
            fill=False,
            edgecolor="black",
            linewidth=1.05
        )

        ax.add_patch(circle)

        ax.plot(
            [hx - 7, hx + 7],
            [hy, hy],
            color="black",
            linewidth=0.45
        )

        ax.plot(
            [hx, hx],
            [hy - 7, hy + 7],
            color="black",
            linewidth=0.45
        )

    # ======================================================
    # 82 DIMENSION
    # ======================================================

    dim82_y = y_top + 30

    ax.plot(
        [x_left, x_left],
        [y_top - 3, dim82_y],
        color="black",
        linewidth=0.65
    )

    ax.plot(
        [x_right, x_right],
        [y_top - 3, dim82_y],
        color="black",
        linewidth=0.65
    )

    ax.plot(
        [x_left, x_right],
        [dim82_y, dim82_y],
        color="black",
        linewidth=0.8
    )

    slash_tick(
        ax,
        x_left,
        dim82_y
    )

    slash_tick(
        ax,
        x_right,
        dim82_y
    )

    ax.text(
        (x_left + x_right) / 2,
        dim82_y + 7,
        f"{width:g}",
        ha="center",
        va="bottom",
        fontsize=13
    )

    # ======================================================
    # 35 DIMENSION
    # ======================================================

    dim35_y = y_top + 9

    ax.plot(
        [hole_x, hole_x],
        [y_top + 2, dim35_y - 1],
        color="black",
        linewidth=0.65
    )

    ax.plot(
        [x_right, x_right],
        [y_top + 2, dim35_y - 1],
        color="black",
        linewidth=0.65
    )

    ax.plot(
        [hole_x, x_right],
        [dim35_y, dim35_y],
        color="black",
        linewidth=0.8
    )

    slash_tick(
        ax,
        hole_x,
        dim35_y
    )

    slash_tick(
        ax,
        x_right,
        dim35_y
    )

    ax.text(
        (hole_x + x_right) / 2,
        dim35_y + 7,
        f"{dimension_35:g}",
        ha="center",
        va="bottom",
        fontsize=13
    )

    # ======================================================
    # 11 DIMENSION
    # ======================================================

    dim11_x = x_right + 35

    ax.plot(
        [x_right, dim11_x],
        [y_top, y_top],
        color="black",
        linewidth=0.65
    )

    ax.plot(
        [hole_x, dim11_x],
        [top_hole_y, top_hole_y],
        color="black",
        linewidth=0.65
    )

    ax.plot(
        [dim11_x, dim11_x],
        [top_hole_y, y_top],
        color="black",
        linewidth=0.8
    )

    slash_tick(
        ax,
        dim11_x,
        y_top,
        size=5
    )

    slash_tick(
        ax,
        dim11_x,
        top_hole_y,
        size=5
    )

    ax.text(
        dim11_x - 9,
        (y_top + top_hole_y) / 2,
        f"{dimension_11:g}",
        rotation=90,
        ha="center",
        va="center",
        fontsize=12
    )

    # ======================================================
    # 310 DIMENSION
    # ======================================================

    dim310_x = x_right + 75

    ax.plot(
        [hole_x, dim310_x],
        [top_hole_y, top_hole_y],
        color="black",
        linewidth=0.8
    )

    ax.plot(
        [hole_x, dim310_x],
        [bottom_hole_y, bottom_hole_y],
        color="black",
        linewidth=0.8
    )

    ax.plot(
        [dim310_x, dim310_x],
        [bottom_hole_y, top_hole_y],
        color="black",
        linewidth=0.8
    )

    slash_tick(
        ax,
        dim310_x,
        top_hole_y,
        size=5
    )

    slash_tick(
        ax,
        dim310_x,
        bottom_hole_y,
        size=5
    )

    ax.text(
        dim310_x - 10,
        (top_hole_y + bottom_hole_y) / 2,
        f"{dimension_310:g}",
        rotation=90,
        ha="center",
        va="center",
        fontsize=13
    )

    # ======================================================
    # OVERALL HEIGHT
    # ======================================================

    dim_height_x = x_right + 110

    ax.plot(
        [x_right, dim_height_x],
        [y_top, y_top],
        color="black",
        linewidth=0.65
    )

    ax.plot(
        [x_right, dim_height_x],
        [y_bottom, y_bottom],
        color="black",
        linewidth=0.65
    )

    ax.plot(
        [dim_height_x, dim_height_x],
        [y_bottom, y_top],
        color="black",
        linewidth=0.8
    )

    slash_tick(
        ax,
        dim_height_x,
        y_top,
        size=5
    )

    slash_tick(
        ax,
        dim_height_x,
        y_bottom,
        size=5
    )

    ax.text(
        dim_height_x - 10,
        height / 2,
        f"{height:g}",
        rotation=90,
        ha="center",
        va="center",
        fontsize=13
    )

    # ======================================================
    # HOLE CALLOUT
    # ======================================================

    note_x = x_right + 47
    note_y = y_top + 84

    ax.text(
        note_x,
        note_y,
        f"{hole_count} – Ø{hole_diameter:g} HOLE",
        ha="left",
        va="bottom",
        fontsize=13
    )

    callout_line_y = note_y - 7

    ax.plot(
        [note_x - 4, note_x + 105],
        [callout_line_y, callout_line_y],
        color="black",
        linewidth=0.9
    )

    ax.text(
        note_x,
        note_y - 20,
        f"FOR {bolt} BOLT",
        ha="left",
        va="bottom",
        fontsize=13
    )

    # ======================================================
    # LEADER
    # ======================================================

    leader_start_x = note_x - 4
    leader_start_y = callout_line_y

    leader_end_x = hole_x + 2
    leader_end_y = top_hole_y + 4

    ax.plot(
        [leader_start_x, leader_end_x],
        [leader_start_y, leader_end_y],
        color="black",
        linewidth=0.95
    )

    # ======================================================
    # PART NUMBER
    # ======================================================

    part_y = -32

    ax.text(
        x_left - 15,
        part_y,
        f"PART NO.{part_no}",
        ha="left",
        va="top",
        fontsize=17,
        fontweight="bold"
    )

    # ======================================================
    # SCALE
    # ======================================================

    scale = str(
        part.get("scale") or "1:2"
    )

    scale_y = -60

    ax.text(
        x_left - 13,
        scale_y,
        f"(SCALE  {scale})",
        ha="left",
        va="top",
        fontsize=15
    )

    # ======================================================
    # FINAL VIEW
    # ======================================================

    setup_axes(
        ax,
        -25,
        205,
        -78,
        465
    )

    plt.savefig(
        output_file,
        dpi=200,
        facecolor="white",
        bbox_inches="tight",
        pad_inches=0.05
    )

    plt.close(fig)

    return output_file


# ==========================================================
# GENERIC DRAWING FUNCTION
# ==========================================================

def create_engineering_drawing(
    part,
    output_file=None
):
    """
    Automatically select the correct drawing
    based on Part Number.
    """

    if part is None:
        raise ValueError(
            "Part data is empty."
        )

    part_no = safe_int(
        part.get("part_no"),
        0
    )

    if output_file is None:
        output_file = (
            f"Part_{part_no}_Drawing.png"
        )

    if part_no == 13:

        return create_part13_drawing(
            part,
            output_file
        )

    elif part_no == 16:

        return create_part16_drawing(
            part,
            output_file
        )

    else:

        raise ValueError(
            f"No drawing template is available "
            f"for Part No. {part_no}."
        )


# ==========================================================
# BACKWARD COMPATIBILITY
# ==========================================================

def create_drawing(
    part,
    output_file=None
):
    """
    Alias for generic drawing function.
    """

    return create_engineering_drawing(
        part,
        output_file
    )