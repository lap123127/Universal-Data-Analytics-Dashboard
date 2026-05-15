import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

# 页面设置
st.set_page_config(page_title="Universal Data Analytics Dashboard", layout="wide")
plt.style.use('seaborn-v0_8')

# 标题
st.title("📊 Universal Data Analytics Dashboard")
st.markdown("Upload any CSV or Excel file to get instant analysis!")

# 1. 文件上传模块
st.sidebar.header("📁 Upload Your Data")
uploaded_file = st.sidebar.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:
    # 读取数据
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.sidebar.success("✅ File uploaded successfully!")
    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
        st.stop()

    # 2. 数据预览
    st.subheader("🔍 Data Preview (First 5 Rows)")
    st.dataframe(df.head(), use_container_width=True)

    # 3. 数据概览卡片
    st.subheader("📋 Data Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Rows", df.shape[0])
    col2.metric("Total Columns", df.shape[1])
    col3.metric("Missing Values", df.isnull().sum().sum())
    col4.metric("Duplicate Rows", df.duplicated().sum())

    # 4. 基础数据清洗
    st.subheader("🧹 Data Cleaning")
    if st.button("Remove Duplicates & Drop Missing Values"):
        initial_rows = df.shape[0]
        df = df.drop_duplicates().dropna()
        st.success(f"✅ Cleaned! Rows reduced from {initial_rows} to {df.shape[0]}")

    # 5. 侧边栏筛选（先做基础的）
    st.sidebar.header("🔎 Basic Filters")
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    # 排除唯一ID字段，避免柱状图异常
    categorical_cols = [col for col in df.select_dtypes(include=['object', 'category']).columns.tolist() 
                    if not any(x in col.lower() for x in ['id','userid','user_id'])]

    if categorical_cols:
        selected_cat = st.sidebar.selectbox("Filter by Category Column", categorical_cols)
        unique_values = df[selected_cat].dropna().unique()
        selected_values = st.sidebar.multiselect("Select values to keep", unique_values, default=unique_values)
        df = df[df[selected_cat].isin(selected_values)]

    # 6. 自动生成4种图表（核心部分）
    st.subheader("📊 Auto-Generated Visualizations")
    if numeric_cols:
        # 直方图（分布）
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Distribution Histogram")
            selected_num = st.selectbox("Select a numeric column for histogram", numeric_cols)
            fig, ax = plt.subplots()
            sns.histplot(df[selected_num].dropna(), kde=True, ax=ax)
            st.pyplot(fig)

        # 柱状对比图
        with col2:
            if categorical_cols:
                st.markdown("### Category Bar Chart")
                bar_cat = st.selectbox("Select category column for bar chart", categorical_cols)
                bar_num = st.selectbox("Select numeric column to aggregate", numeric_cols)
                bar_data = df.groupby(bar_cat)[bar_num].mean().sort_values(ascending=False)
                fig, ax = plt.subplots()
                bar_data.plot(kind='bar', ax=ax)
                plt.xticks(rotation=45)
                st.pyplot(fig)

        # 相关性热力图
        if len(numeric_cols) >= 2:
            st.markdown("### Correlation Heatmap")
            corr = df[numeric_cols].corr()
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
            st.pyplot(fig)

        # 饼图（选一个分类字段）
        if categorical_cols:
            st.markdown("### Proportion Pie Chart")
            pie_col = st.selectbox("Select category column for pie chart", categorical_cols)
            pie_data = df[pie_col].value_counts()
            fig, ax = plt.subplots()
            ax.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%')
            st.pyplot(fig)

        # 7. 关键指标卡片（扩展）
        st.subheader("📈 Key Metrics")
        if numeric_cols:
            key_col = st.selectbox("Select column for key metrics", numeric_cols)
            mean_val = df[key_col].mean()
            max_val = df[key_col].max()
            min_val = df[key_col].min()
            count = df.shape[0]

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Records", count)
            col2.metric("Mean Value", round(mean_val, 2))
            col3.metric("Max Value", round(max_val, 2))
            col4.metric("Min Value", round(min_val, 2))

        # 8. 图表下载功能
        st.subheader("💾 Download Charts")
        if st.button("Download Last Chart as PNG"):
            buf = BytesIO()
            plt.tight_layout()
            plt.savefig(buf, format='png', bbox_inches='tight')
            buf.seek(0)
            st.download_button(
                label="Download PNG",
                data=buf,
                file_name="chart.png",
                mime="image/png"
            )
    else:
        st.warning("⚠️ No numeric columns found in your dataset. Charts cannot be generated.")

else:
    # 初始状态提示
    st.info("👆 Please upload a CSV or Excel file to get started!")
    st.markdown("""
    ### Supported Features:
    - ✅ CSV/Excel file upload
    - ✅ Data preview & overview
    - ✅ Basic data cleaning (remove duplicates, drop missing values)
    - ✅ Category filters
    - ✅ 4 types of visualizations (histogram, bar chart, pie chart, heatmap)
    - ✅ Key metrics cards
    - ✅ Chart download as PNG
    """)