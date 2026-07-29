import os
import pandas as pd
from graphviz import Digraph

# Graphviz Path
os.environ["PATH"] += os.pathsep + r"C:\Program Files (x86)\Graphviz\bin"


def create_diagram(df):

    dot = Digraph("Architecture", format="png")

    dot.attr(
        rankdir="TB",
        bgcolor="white",
        splines="ortho",
        nodesep="0.8",
        ranksep="1.2",
        pad="0.5"
    )

    dot.attr(
        "edge",
        color="#757575",
        penwidth="2",
        arrowsize="0.8"
    )

    visited = {}

    colors = [
        ("#0D47A1", "#BBDEFB"),   # Root
        ("#2E7D32", "#C8E6C9"),   # Module
        ("#EF6C00", "#FFE0B2"),   # Submodule
        ("#6A1B9A", "#E1BEE7"),   # Component
        ("#00838F", "#B2EBF2"),   # Child
        ("#5D4037", "#D7CCC8"),   # Leaf
        ("#455A64", "#CFD8DC")
    ]

    for _, row in df.iterrows():

        values = [str(v) for v in row if pd.notna(v)]

        for level, node in enumerate(values):

            if node not in visited:

                idx = min(level, len(colors)-1)

                border, fill = colors[idx]

                fontsize = "18" if level == 0 else "13"

                dot.node(
                    node,
                    shape="box",
                    style="rounded,filled",
                    fillcolor=fill,
                    color=border,
                    penwidth="2.5",
                    fontname="Segoe UI",
                    fontsize=fontsize,
                    margin="0.25"
                )

                visited[node] = True

        for i in range(len(values)-1):

            dot.edge(values[i], values[i+1])

    os.makedirs("output", exist_ok=True)

    dot.render(
        "output/architecture",
        cleanup=True
    )

    return "output/architecture.png"