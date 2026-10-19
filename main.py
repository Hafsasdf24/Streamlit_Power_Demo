import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# ==============================================================================
# 1. STREAMLIT PAGE CONFIGURATION
# ==============================================================================
# st.set_page_config MUST be the first Streamlit command called in your script.
st.set_page_config(
    page_title="Streamlit Workflow & Visualizations Guide",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. INTRO & WORKFLOW EXPLANATION
# ==============================================================================
st.title("📊 Understanding the Streamlit Workflow")
st.markdown("""
Welcome! This app demonstrates how **Streamlit's reactive model** works and how to build
**native charts**, **Matplotlib/Seaborn figures**, and **interactive Plotly visuals**.

> 💡 **Core Concept:** Streamlit scripts run **from top to bottom** every time a user interacts
> with any widget (slider, dropdown, button, etc.). Widgets act as variables that return their current state.
""")

# ==============================================================================
# 3. SIDEBAR CONTROLS (Input Widgets)
# ==============================================================================
with st.sidebar:
    st.header("⚙️ Interactive Controls")
    st.caption("Changing these inputs triggers a top-to-bottom rerun.")
    
    num_points = st.slider("Number of Data Points", min_value=30, max_value=300, value=120, step=10)
    noise_level = st.slider("Data Volatility / Noise", min_value=0.1, max_value=2.0, value=0.8, step=0.1)
    
    categories = ["Electronics", "Fashion", "Home & Living"]
    selected_categories = st.multiselect(
        "Filter Categories",
        options=categories,
        default=categories
    )
    
    random_seed = st.number_input("Random Seed", min_value=1, max_value=9999, value=42, step=1)
    
    st.divider()
    st.markdown("### 🧠 How Streamlit Works")
    st.info(
        "1. **Code is pure Python**.\n"
        "2. **State flows downward**.\n"
        "3. **Widgets return values** directly into variables.\n"
        "4. Use `st.session_state` to remember values across reruns."
    )

# Fallback in case user deselects all categories
if not selected_categories:
    selected_categories = categories
    st.warning("⚠️ At least one category must be selected. Defaulting to all categories.")

# ==============================================================================
# 4. SYNTHETIC DATA GENERATION
# ==============================================================================
np.random.seed(random_seed)

dates = pd.date_range(start="2024-01-01", periods=num_points, freq="D")
base_trend = np.linspace(50, 150, num_points)
noise = np.random.normal(0, noise_level * 15, num_points)

df = pd.DataFrame({
    "Date": dates,
    "Sales": np.maximum(10, base_trend + noise).round(2),
    "Profit": np.maximum(2, (base_trend * 0.3) + np.random.normal(0, noise_level * 5, num_points)).round(2),
    "Units_Sold": np.random.randint(5, 50, size=num_points),
    "Category": np.random.choice(categories, size=num_points),
    "Satisfaction_Score": np.random.uniform(3.0, 5.0, size=num_points).round(2)
})

# Filter data based on sidebar selection
filtered_df = df[df["Category"].isin(selected_categories)].reset_index(drop=True)

# ==============================================================================
# 5. KEY PERFORMANCE INDICATORS (KPIs / Metrics)
# ==============================================================================
st.subheader("📌 Key Metrics (`st.metric`)")

col1, col2, col3, col4 = st.columns(4)
with col1:
    total_sales = filtered_df["Sales"].sum()
    st.metric(label="Total Sales", value=f"${total_sales:,.2f}", delta=f"+{noise_level * 5:.1f}%")

with col2:
    avg_profit = filtered_df["Profit"].mean()
    st.metric(label="Avg Profit / Day", value=f"${avg_profit:.2f}", delta="4.2%")

with col3:
    total_units = filtered_df["Units_Sold"].sum()
    st.metric(label="Total Units Sold", value=f"{total_units:,}", delta="-1.5%")

with col4:
    avg_score = filtered_df["Satisfaction_Score"].mean()
    st.metric(label="Avg Satisfaction", value=f"{avg_score:.2f} ⭐", delta="0.2")

st.divider()

# ==============================================================================
# 6. TABBED VISUALIZATION DEMONSTRATION
# ==============================================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 1. Built-in Streamlit Charts",
    "🎨 2. Matplotlib & Seaborn",
    "✨ 3. Interactive Plotly",
    "🔄 4. Session State & Data Flow"
])

# ------------------------------------------------------------------------------
# TAB 1: Streamlit Built-in Charts
# ------------------------------------------------------------------------------
with tab1:
    st.markdown("### Native Streamlit Visualizations")
    st.write(
        "Streamlit provides fast, zero-configuration chart wrappers (`st.line_chart`, "
        "`st.area_chart`, `st.bar_chart`, `st.scatter_chart`) powered by Altair."
    )
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.caption("**Line Chart (`st.line_chart`)** - Sales & Profit Trend over Time")
        chart_data = filtered_df.set_index("Date")[["Sales", "Profit"]]
        st.line_chart(chart_data)
        
    with c2:
        st.caption("**Area Chart (`st.area_chart`)** - Cumulative Volume")
        st.area_chart(chart_data)

    c3, c4 = st.columns(2)
    
    with c3:
        st.caption("**Bar Chart (`st.bar_chart`)** - Units Sold by Category")
        category_units = filtered_df.groupby("Category")["Units_Sold"].sum()
        st.bar_chart(category_units)
        
    with c4:
        st.caption("**Scatter Chart (`st.scatter_chart`)** - Sales vs Profit")
        st.scatter_chart(
            data=filtered_df,
            x="Sales",
            y="Profit",
            color="Category",
            size="Units_Sold"
        )

# ------------------------------------------------------------------------------
# TAB 2: Matplotlib & Seaborn
# ------------------------------------------------------------------------------
with tab2:
    st.markdown("### Matplotlib & Seaborn (`st.pyplot`)")
    st.write(
        "When you need publication-quality statistical plots or fine-grained style control, "
        "render a Matplotlib figure using `st.pyplot(fig)`."
    )
    
    # Best Practice Note:
    # Always create an explicit figure and axes (fig, ax = plt.subplots()) instead of plt.plot()
    # to avoid thread-safety and shared figure state issues in Streamlit.
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Subplot 1: Seaborn Distribution Plot
    sns.set_theme(style="whitegrid")
    sns.histplot(
        data=filtered_df,
        x="Sales",
        hue="Category",
        kde=True,
        ax=ax1,
        palette="viridis",
        element="step"
    )
    ax1.set_title("Sales Distribution by Category", fontsize=12, fontweight="bold")
    ax1.set_xlabel("Sales ($)")
    ax1.set_ylabel("Count")

    # Subplot 2: Correlation Heatmap
    numeric_cols = ["Sales", "Profit", "Units_Sold", "Satisfaction_Score"]
    corr_matrix = filtered_df[numeric_cols].corr()
    sns.heatmap(
        corr_matrix,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        square=True,
        ax=ax2,
        cbar_kws={"shrink": 0.8}
    )
    ax2.set_title("Feature Correlation Matrix", fontsize=12, fontweight="bold")
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)  # Free memory
    
    with st.expander("🔍 Streamlit Best Practice: Thread-Safe Matplotlib"):
        st.code("""
# Recommended: Create explicit fig, ax objects
fig, ax = plt.subplots()
ax.plot(x, y)
st.pyplot(fig)
plt.close(fig)  # Prevents figure leaking in multi-user environments
        """, language="python")

# ------------------------------------------------------------------------------
# TAB 3: Interactive Plotly Visualizations
# ------------------------------------------------------------------------------
with tab3:
    st.markdown("### Interactive Visualizations with Plotly (`st.plotly_chart`)")
    st.write(
        "Plotly enables rich interactivity: hovering for tooltips, zooming, panning, "
        "and isolating specific traces directly inside the browser."
    )
    
    col_p1, col_p2 = st.columns(2)
    
    with col_p1:
        # Plotly Scatter Plot with regression line
        fig_scatter = px.scatter(
            filtered_df,
            x="Sales",
            y="Profit",
            color="Category",
            size="Units_Sold",
            hover_data=["Date", "Satisfaction_Score"],
            title="Interactive: Sales vs Profit (Bubble Size = Units Sold)",
            template="plotly_white"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    with col_p2:
        # Plotly Box Plot showing spread & outliers
        fig_box = px.box(
            filtered_df,
            x="Category",
            y="Satisfaction_Score",
            color="Category",
            points="all",
            title="Interactive: Satisfaction Score Spread by Category",
            template="plotly_white"
        )
        st.plotly_chart(fig_box, use_container_width=True)

    # Plotly 3D Surface / Mesh Demo
    with st.expander("🌐 Bonus: Interactive 3D Scatter Plot"):
        fig_3d = px.scatter_3d(
            filtered_df,
            x="Sales",
            y="Profit",
            z="Satisfaction_Score",
            color="Category",
            size="Units_Sold",
            title="3D Performance Space",
            template="plotly_dark"
        )
        st.plotly_chart(fig_3d, use_container_width=True)

# ------------------------------------------------------------------------------
# TAB 4: Streamlit Reactive Architecture & Session State
# ------------------------------------------------------------------------------
with tab4:
    st.markdown("### Managing State Across Reruns (`st.session_state`)")
    st.write(
        "Because Streamlit reruns the script upon any interaction, normal Python variables "
        "reset to their original values. To remember state between reruns, use `st.session_state`."
    )
    
    # Initialize session state variables if they do not exist
    if "counter" not in st.session_state:
        st.session_state.counter = 0
    if "bookmarks" not in st.session_state:
        st.session_state.bookmarks = []

    c_state1, c_state2 = st.columns(2)
    
    with c_state1:
        st.markdown("#### Counter Demo")
        st.write(f"Current persistent count: **{st.session_state.counter}**")
        
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("➕ Increment Counter"):
                st.session_state.counter += 1
                st.rerun()
        with btn_col2:
            if st.button("🔄 Reset Counter"):
                st.session_state.counter = 0
                st.rerun()

    with c_state2:
        st.markdown("#### Dynamic Bookmark / Tagging Demo")
        new_tag = st.text_input("Add a quick note / tag:")
        if st.button("Save Tag") and new_tag:
            st.session_state.bookmarks.append(new_tag)
        
        st.write("Saved Tags:", st.session_state.bookmarks if st.session_state.bookmarks else "No tags yet.")

    st.markdown("---")
    st.markdown("### 📋 Filtered Dataset Explorer (`st.dataframe`)")
    st.dataframe(filtered_df, use_container_width=True)

# ==============================================================================
# 7. FOOTER
# ==============================================================================
st.markdown("---")
st.caption(
    "Run this application with: `streamlit run main.py` | "
    "Streamlit Docs: [docs.streamlit.io](https://docs.streamlit.io)"
)
