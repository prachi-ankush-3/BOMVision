import os
import shutil

os.environ["PATH"] += os.pathsep + r"C:\Program Files (x86)\Graphviz\bin"

print("PATH =", os.environ["PATH"])
print("DOT =", shutil.which("dot"))

import pandas as pd
from graphviz import Digraph

def create_diagram(df):
    dot = Digraph("Architecture")
    dot.attr(rankdir="TB")

    if len(df.columns) == 2:

        for _, row in df.iterrows():
            parent = str(row.iloc[0])
            child = str(row.iloc[1])

            dot.node(parent)
            dot.node(child)
            dot.edge(parent, child)

    else:

        for _, row in df.iterrows():
            values = [str(v) for v in row if pd.notna(v)]

            for i in range(len(values)-1):
                dot.node(values[i])
                dot.node(values[i+1])
                dot.edge(values[i], values[i+1])

    dot.render("output/architecture", format="png", cleanup=True)

    return "output/architecture.png"