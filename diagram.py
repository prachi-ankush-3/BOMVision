import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle


def create_part16_drawing(
    part,
    output_file="Part_16_Drawing.png"
):
    """
    BOMVision - Part No. 16 Engineering Drawing

    Reference dimensions:
        Width       = 82 mm
        Height      = 332 mm
        Thickness   = 8 mm
        Hole count  = 2
        Hole dia    = 14 mm
        Hole X      = 35 mm
        Hole offset = 11 mm
        Hole-to-hole= 310 mm
        Bolt        = M12

    Drawing is constructed using fixed engineering coordinates
    so that the generated image follows the supplied reference.
    """

    # ==========================================================
    # 1. READ BOM DATA
    # ==========================================================

    part_no = str(part.get("part_no", 16))

    width = float(part.get("width", 82))
    height = float(part.get("height", 332))
    thickness = float(part.get("thickness", 8))

    hole_count = int(part.get("hole_count", 2))
    hole_diameter = float(part.get("hole_diameter", 14))

    dimension_35 = float(part.get("dimension_35", 35))
    dimension_11 = float(part.get("dimension_11", 11))
    dimension_310 = float(part.get("dimension_310", 310))

    bolt = str(part.get("bolt", "M12"))

    # ==========================================================
    # 2. DRAWING COORDINATES
    # ==========================================================

    # Main plate
    x_left = 0
    x_right = width

    y_bottom = 0
    y_top = height

    # ----------------------------------------------------------
    # IMPORTANT:
    #
    # The actual plate is 82 x 332.
    #
    # Therefore:
    #
    #       width  = 82
    #       height = 332
    #
    # This keeps the correct narrow vertical appearance.
    # ----------------------------------------------------------

    # Chamfer
    chamfer = 8

    # Hole X position
    hole_x = dimension_35

    # Hole Y positions
    bottom_hole_y = dimension_11
    top_hole_y = height - dimension_11

    hole_radius = hole_diameter / 2

    # ==========================================================
    # 3. FIGURE
    # ==========================================================

    fig, ax = plt.subplots(
        figsize=(7.4, 12.5),
        dpi=200
    )

    # ==========================================================
    # 4. MAIN PLATE
    # ==========================================================
    #
    #                 82
    #        ┌────────────────┐
    #       /                 │
    #      │                  │
    #      │                  │
    #      │                  │
    #       \────────────────┘
    #
    # ==========================================================

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

    # ==========================================================
    # 5. HOLES
    # ==========================================================

    hole_positions = []

    if hole_count >= 1:
        hole_positions.append(
            (hole_x, bottom_hole_y)
        )

    if hole_count >= 2:
        hole_positions.append(
            (hole_x, top_hole_y)
        )

    for hx, hy in hole_positions:

        # ------------------------------------------------------
        # Hole circle
        # ------------------------------------------------------

        circle = Circle(
            (hx, hy),
            hole_radius,
            fill=False,
            edgecolor="black",
            linewidth=1.05
        )

        ax.add_patch(circle)

        # ------------------------------------------------------
        # Horizontal center line
        # ------------------------------------------------------

        ax.plot(
            [hx - 7, hx + 7],
            [hy, hy],
            color="black",
            linewidth=0.45
        )

        # ------------------------------------------------------
        # Vertical center line
        # ------------------------------------------------------

        ax.plot(
            [hx, hx],
            [hy - 7, hy + 7],
            color="black",
            linewidth=0.45
        )

    # ==========================================================
    # 6. DIMENSION SLASH
    # ==========================================================
    #
    # Reference uses:
    #
    #       /──────────────/
    #
    # NOT:
    #
    #       <──────────────>
    #
    # ==========================================================

    def slash_tick(
        x,
        y,
        size=5,
        linewidth=1.1
    ):

        ax.plot(
            [x - size, x + size],
            [y - size, y + size],
            color="black",
            linewidth=linewidth,
            solid_capstyle="butt"
        )

    # ==========================================================
    # 7. 82 MM DIMENSION
    # ==========================================================
    #
    #             82
    #       /────────────/
    #
    # ==========================================================

    dim82_y = y_top + 30

    # Left extension
    ax.plot(
        [x_left, x_left],
        [y_top - 3, dim82_y],
        color="black",
        linewidth=0.65
    )

    # Right extension
    ax.plot(
        [x_right, x_right],
        [y_top - 3, dim82_y],
        color="black",
        linewidth=0.65
    )

    # Horizontal dimension line
    ax.plot(
        [x_left, x_right],
        [dim82_y, dim82_y],
        color="black",
        linewidth=0.8
    )

    # Slash marks
    slash_tick(x_left, dim82_y)
    slash_tick(x_right, dim82_y)

    # 82 text
    ax.text(
        (x_left + x_right) / 2,
        dim82_y + 7,
        f"{width:g}",
        ha="center",
        va="bottom",
        fontsize=13
    )

    # ==========================================================
    # 8. 35 MM DIMENSION
    # ==========================================================
    #
    #              35
    #             /────/
    #                 |
    #                 |
    #                 |
    #
    #  IMPORTANT:
    #  35 is BELOW 82.
    #
    # ==========================================================

    dim35_y = y_top + 9

    # Left extension
    ax.plot(
        [hole_x, hole_x],
        [y_top + 2, dim35_y - 1],
        color="black",
        linewidth=0.65
    )

    # Hole position extension
    ax.plot(
        [x_right, x_right],
        [y_top + 2, dim35_y - 1],
        color="black",
        linewidth=0.65
    )

    # Horizontal dimension
    ax.plot(
        [hole_x, x_right],
        [dim35_y, dim35_y],
        color="black",
        linewidth=0.8
    )

    # Slash marks
    slash_tick(hole_x, dim35_y)
    slash_tick(x_right, dim35_y)

    # 35 text
    ax.text(
        (hole_x + x_right) / 2,
        dim35_y + 7,
        f"{dimension_35:g}",
        ha="center",
        va="bottom",
        fontsize=13
    )

    # ==========================================================
    # 9. 11 MM DIMENSION
    # ==========================================================
    #
    # Reference:
    #
    #         ──────────/
    #                 11
    #                 /
    #         ────────/
    #
    # ==========================================================

    dim11_x = x_right + 35

    # Top horizontal extension
    ax.plot(
        [x_right, dim11_x],
        [y_top, y_top],
        color="black",
        linewidth=0.65
    )

    # Hole center horizontal extension
    ax.plot(
        [hole_x, dim11_x],
        [top_hole_y, top_hole_y],
        color="black",
        linewidth=0.65
    )

    # Vertical dimension line
    ax.plot(
        [dim11_x, dim11_x],
        [top_hole_y, y_top],
        color="black",
        linewidth=0.8
    )

    # Slash at top
    slash_tick(
        dim11_x,
        y_top,
        size=5
    )

    # Slash at hole center
    slash_tick(
        dim11_x,
        top_hole_y,
        size=5
    )

    # 11 text
    ax.text(
        dim11_x - 9,
        (y_top + top_hole_y) / 2,
        f"{dimension_11:g}",
        rotation=90,
        ha="center",
        va="center",
        fontsize=12
    )

    # ==========================================================
    # 10. 310 MM DIMENSION
    # ==========================================================
    #
    # THIS IS IMPORTANT.
    #
    # The reference has horizontal lines coming directly
    # from both hole centers.
    #
    #       ○──────────────────╲
    #                           │
    #                          310
    #                           │
    #       ○──────────────────╱
    #
    # ==========================================================

    dim310_x = x_right + 75

    # ----------------------------------------------------------
    # TOP HORIZONTAL LINE
    # ----------------------------------------------------------

    ax.plot(
        [hole_x, dim310_x],
        [top_hole_y, top_hole_y],
        color="black",
        linewidth=0.8
    )

    # ----------------------------------------------------------
    # BOTTOM HORIZONTAL LINE
    # ----------------------------------------------------------

    ax.plot(
        [hole_x, dim310_x],
        [bottom_hole_y, bottom_hole_y],
        color="black",
        linewidth=0.8
    )

    # ----------------------------------------------------------
    # VERTICAL 310 LINE
    # ----------------------------------------------------------

    ax.plot(
        [dim310_x, dim310_x],
        [bottom_hole_y, top_hole_y],
        color="black",
        linewidth=0.8
    )

    # ----------------------------------------------------------
    # TOP SLASH
    # ----------------------------------------------------------

    slash_tick(
        dim310_x,
        top_hole_y,
        size=5
    )

    # ----------------------------------------------------------
    # BOTTOM SLASH
    # ----------------------------------------------------------

    slash_tick(
        dim310_x,
        bottom_hole_y,
        size=5
    )

    # ----------------------------------------------------------
    # 310 LABEL
    # ----------------------------------------------------------

    ax.text(
        dim310_x - 10,
        (top_hole_y + bottom_hole_y) / 2,
        f"{dimension_310:g}",
        rotation=90,
        ha="center",
        va="center",
        fontsize=13
    )

    # ==========================================================
    # 11. 332 MM OVERALL DIMENSION
    # ==========================================================
    #
    #       ─────────────────────╲
    #                             │
    #                            332
    #                             │
    #       ─────────────────────╱
    #
    # ==========================================================

    dim332_x = x_right + 110

    # Top extension
    ax.plot(
        [x_right, dim332_x],
        [y_top, y_top],
        color="black",
        linewidth=0.65
    )

    # Bottom extension
    ax.plot(
        [x_right, dim332_x],
        [y_bottom, y_bottom],
        color="black",
        linewidth=0.65
    )

    # Vertical 332 dimension
    ax.plot(
        [dim332_x, dim332_x],
        [y_bottom, y_top],
        color="black",
        linewidth=0.8
    )

    # Top slash
    slash_tick(
        dim332_x,
        y_top,
        size=5
    )

    # Bottom slash
    slash_tick(
        dim332_x,
        y_bottom,
        size=5
    )

    # 332 text
    ax.text(
        dim332_x - 10,
        height / 2,
        f"{height:g}",
        rotation=90,
        ha="center",
        va="center",
        fontsize=13
    )

    # ==========================================================
    # 12. HOLE CALLOUT
    # ==========================================================
    #
    #       2 - Ø14 HOLE
    #       ─────────────────────
    #       FOR M12 BOLT
    #             /
    #            /
    #           /
    #          ○
    #
    # ==========================================================

    note_x = x_right + 47
    note_y = y_top + 84

    # ----------------------------------------------------------
    # First line
    # ----------------------------------------------------------

    ax.text(
        note_x,
        note_y,
        f"{hole_count} – Ø{hole_diameter:g} HOLE",
        ha="left",
        va="bottom",
        fontsize=13
    )

    # ----------------------------------------------------------
    # Horizontal line below first line
    # ----------------------------------------------------------

    callout_line_y = note_y - 7

    ax.plot(
        [note_x - 4, note_x + 105],
        [callout_line_y, callout_line_y],
        color="black",
        linewidth=0.9
    )

    # ----------------------------------------------------------
    # FOR M12 BOLT
    # ----------------------------------------------------------

    ax.text(
        note_x,
        note_y - 20,
        f"FOR {bolt} BOLT",
        ha="left",
        va="bottom",
        fontsize=13
    )

    # ==========================================================
    # 13. LEADER LINE
    # ==========================================================

    # The leader starts from the left end of the
    # horizontal callout line and goes to the top hole.

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

    # ==========================================================
    # 14. PART NO. 16
    # ==========================================================

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

    # Underline
    ax.plot(
        [x_left - 18, x_left + 72],
        [part_y - 8, part_y - 8],
        color="black",
        linewidth=2.0
    )

    # ==========================================================
    # 15. SCALE
    # ==========================================================

    scale_y = -60

    ax.text(
        x_left - 13,
        scale_y,
        "(SCALE  1:2)",
        ha="left",
        va="top",
        fontsize=15
    )

    # Scale underline
    ax.plot(
        [x_left - 17, x_left + 68],
        [scale_y - 8, scale_y - 8],
        color="black",
        linewidth=2.0
    )

    # ==========================================================
    # 16. FINAL VIEW
    # ==========================================================

    ax.set_aspect("equal")

    # IMPORTANT:
    # Fixed limits prevent the image from becoming excessively wide.

    ax.set_xlim(
        -25,
        205
    )

    ax.set_ylim(
        -78,
        465
    )

    ax.axis("off")

    # ==========================================================
    # 17. SAVE
    # ==========================================================

    plt.savefig(
        output_file,
        dpi=200,
        facecolor="white",
        bbox_inches="tight",
        pad_inches=0.05
    )

    plt.close(fig)

    return output_file