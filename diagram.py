import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle


def create_part16_drawing(part, output_file="Part_16_Drawing.png"):

    # -----------------------------
    # Read data from BOM parser
    # -----------------------------

    part_no = part["part_no"]

    width = float(part["width"])
    height = float(part["height"])
    thickness = float(part["thickness"])

    hole_count = int(part["hole_count"])
    hole_diameter = float(part["hole_diameter"])

    dimension_35 = float(part["dimension_35"])
    dimension_11 = float(part["dimension_11"])
    dimension_310 = float(part["dimension_310"])

    bolt = part["bolt"]
    material = part["material"]

    # -----------------------------
    # Create figure
    # -----------------------------

    fig, ax = plt.subplots(figsize=(8.27, 11.69))

    # Position of plate
    x0 = 30
    y0 = 40

    # -----------------------------
    # Draw plate
    # -----------------------------

    plate = Rectangle(
        (x0, y0),
        width,
        height,
        fill=False,
        linewidth=1.5
    )

    ax.add_patch(plate)

    # -----------------------------
    # Hole positions
    # -----------------------------

    hole_x = x0 + dimension_35

    hole_bottom_y = y0 + dimension_11
    hole_top_y = y0 + height - dimension_11

    hole_radius = hole_diameter / 2

    # Bottom hole
    if hole_count >= 1:

        bottom_hole = Circle(
            (hole_x, hole_bottom_y),
            hole_radius,
            fill=False,
            linewidth=1.2
        )

        ax.add_patch(bottom_hole)

    # Top hole
    if hole_count >= 2:

        top_hole = Circle(
            (hole_x, hole_top_y),
            hole_radius,
            fill=False,
            linewidth=1.2
        )

        ax.add_patch(top_hole)

    # -----------------------------
    # Center marks
    # -----------------------------

    for hx, hy in [
        (hole_x, hole_bottom_y),
        (hole_x, hole_top_y)
    ]:

        ax.plot(
            [hx - 8, hx + 8],
            [hy, hy],
            linewidth=0.5
        )

        ax.plot(
            [hx, hx],
            [hy - 8, hy + 8],
            linewidth=0.5
        )

    # -----------------------------
    # Width dimension - 82
    # -----------------------------

    dimension_y = y0 - 25

    ax.plot(
        [x0, x0],
        [y0, dimension_y],
        linewidth=0.5
    )

    ax.plot(
        [x0 + width, x0 + width],
        [y0, dimension_y],
        linewidth=0.5
    )

    ax.annotate(
        "",
        xy=(x0 + width, dimension_y),
        xytext=(x0, dimension_y),
        arrowprops=dict(
            arrowstyle="<->",
            linewidth=0.8
        )
    )

    ax.text(
        x0 + width / 2,
        dimension_y + 5,
        "82",
        ha="center",
        fontsize=9
    )

    # -----------------------------
    # Height dimension - 332
    # -----------------------------

    dimension_x = x0 + width + 35

    ax.plot(
        [x0 + width, dimension_x],
        [y0, y0],
        linewidth=0.5
    )

    ax.plot(
        [x0 + width, dimension_x],
        [y0 + height, y0 + height],
        linewidth=0.5
    )

    ax.annotate(
        "",
        xy=(dimension_x, y0 + height),
        xytext=(dimension_x, y0),
        arrowprops=dict(
            arrowstyle="<->",
            linewidth=0.8
        )
    )

    ax.text(
        dimension_x + 5,
        y0 + height / 2,
        "332",
        rotation=90,
        va="center",
        fontsize=9
    )

    # -----------------------------
    # 310 dimension
    # -----------------------------

    dimension_x_310 = x0 + width + 15

    start_310 = y0 + dimension_11
    end_310 = y0 + height - dimension_11

    ax.annotate(
        "",
        xy=(dimension_x_310, end_310),
        xytext=(dimension_x_310, start_310),
        arrowprops=dict(
            arrowstyle="<->",
            linewidth=0.8
        )
    )

    ax.text(
        dimension_x_310 + 4,
        (start_310 + end_310) / 2,
        "310",
        rotation=90,
        va="center",
        fontsize=9
    )

    # -----------------------------
    # 35 dimension
    # -----------------------------

    dimension_y_35 = y0 + height + 20

    ax.annotate(
        "",
        xy=(hole_x, dimension_y_35),
        xytext=(x0, dimension_y_35),
        arrowprops=dict(
            arrowstyle="<->",
            linewidth=0.8
        )
    )

    ax.text(
        (x0 + hole_x) / 2,
        dimension_y_35 + 5,
        "35",
        ha="center",
        fontsize=9
    )

    # -----------------------------
    # Hole information
    # -----------------------------

    ax.text(
        x0 - 5,
        y0 + height + 55,
        f"{hole_count} - Ø{hole_diameter} HOLE",
        fontsize=9
    )

    ax.text(
        x0 - 5,
        y0 + height + 45,
        f"FOR {bolt} BOLT",
        fontsize=9
    )

    # -----------------------------
    # Thickness
    # -----------------------------

    ax.text(
        x0 + width / 2,
        y0 + height + 5,
        f"{thickness} THK.",
        ha="center",
        fontsize=9
    )

    # -----------------------------
    # Part number
    # -----------------------------

    ax.text(
        x0 - 10,
        y0 - 55,
        f"PART NO. {part_no}",
        fontsize=12,
        fontweight="bold"
    )

    # -----------------------------
    # Material
    # -----------------------------

    ax.text(
        x0 - 10,
        y0 - 65,
        f"MATERIAL: {material}",
        fontsize=8
    )

    # -----------------------------
    # Scale
    # -----------------------------

    ax.text(
        x0 + width + 40,
        y0 - 55,
        "SCALE 1:2",
        fontsize=8
    )

    # -----------------------------
    # Drawing settings
    # -----------------------------

    ax.set_aspect("equal")

    ax.set_xlim(
        x0 - 60,
        x0 + width + 80
    )

    ax.set_ylim(
        y0 - 80,
        y0 + height + 80
    )

    ax.axis("off")

    # -----------------------------
    # Save image
    # -----------------------------

    plt.savefig(
        output_file,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close(fig)

    return output_file