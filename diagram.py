import os
import shutil

os.environ["PATH"] += os.pathsep + r"C:\Program Files (x86)\Graphviz\bin"

print("PATH =", os.environ["PATH"])
print("DOT =", shutil.which("dot"))

from graphviz import Digraph


def create_diagram(df):

    dot = Digraph("Architecture")
    dot.attr(rankdir="TB")

    for index, row in df.iterrows():
        parent = str(row["Parent"])
        component = str(row["Component"])

        dot.node(parent)
        dot.node(component)
        dot.edge(parent, component)

    dot.render("output/architecture", format="png", cleanup=True)

    return "output/architecture.png"