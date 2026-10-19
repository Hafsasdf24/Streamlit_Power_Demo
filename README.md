# Streamlit Power Demo

An interactive Streamlit application demonstrating Streamlit's reactive execution model, native charts, Matplotlib & Seaborn plots, interactive Plotly visuals, and persistent session state handling.

## Features
- **Streamlit Reactive Workflow:** Interactive sidebar widgets that reactively trigger top-to-bottom execution.
- **Native Charts:** Zero-config charts including line, area, bar, and scatter plots powered by Altair.
- **Matplotlib & Seaborn:** Thread-safe statistical figures including distribution KDE plots and feature correlation heatmaps.
- **Interactive Plotly:** Hover tooltips, regression lines, and 3D scatter plots.
- **Session State Management:** Demonstrates retaining data across reruns using `st.session_state`.

## Setup & Running Locally

1. **Activate virtual environment:**
   ```bash
   .venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit application:**
   ```bash
   streamlit run main.py
   ```
