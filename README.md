# 🚀 BOMVision

**BOMVision** is a Python-based application that automatically converts **Bill of Materials (BOM) Excel files** into hierarchical **architecture diagrams**. Built with **Streamlit**, **Pandas**, and **Graphviz**, it helps users visualize component relationships and product structures in a clean and interactive way.

---

## ✨ Features

* 📂 Upload BOM Excel (.xlsx) files
* 📊 Automatically analyzes parent-child relationships
* 🏗️ Generates architecture diagrams
* ⚡ Interactive Streamlit web interface
* 💾 Export diagrams as PNG images
* 🔄 Supports multi-level component hierarchies

---

## 🛠️ Tech Stack

* Python 3.11+
* Streamlit
* Pandas
* Graphviz

---

## 📁 Project Structure

```text
BOMVision/
│── app.py
│── diagram.py
|── excel_reader.py
│── requirements.txt
│── output/
│── input/
└── README.md
```

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/prachi-ankush-3/BOMVision.git
cd BOMVision
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Graphviz

Download and install Graphviz from:

https://graphviz.org/download/

After installation, add the **Graphviz `bin` folder** to your system **PATH**.

Example:

```text
C:\Program Files (x86)\Graphviz\bin
```

Verify the installation:

```bash
dot -V
```

---

## ▶️ Run the Application

Navigate to the project folder and run:

```bash
"C:\Users\ASUS\AppData\Local\Programs\Python\Python311\python.exe" -m streamlit run app.py
```

After running the command, Streamlit will open the application in your default web browser.

---

## 📄 Input Format

The uploaded Excel file should contain the following columns:

| Parent      | Component    |
| ----------- | ------------ |
| Computer    | Motherboard  |
| Motherboard | CPU          |
| CPU         | Cache Memory |

---

## 📤 Output

The application generates:

* Architecture Diagram (.png)
* Hierarchical visualization of the BOM
* Parent-child component relationships

---

## 📸 Example Workflow

1. Upload a BOM Excel file.
2. The application reads the parent-child relationships.
3. Graphviz generates the architecture diagram.
4. View and save the generated diagram.

---

## 👩‍💻 Author

**Prachi Ankush**

GitHub: https://github.com/prachi-ankush-3
