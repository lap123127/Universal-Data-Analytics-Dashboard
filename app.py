import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

# ===================== 多语言配置 =====================
# 定义中英文对照字典
LANG_CONFIG = {
    "en": {
        "page_title": "Universal Data Analytics Dashboard",
        "main_title": "📊 Universal Data Analytics Dashboard",
        "main_desc": "Upload any CSV or Excel file to get instant analysis!",
        "sidebar_upload": "📁 Upload Your Data",
        "upload_label": "Upload CSV or Excel file",
        "upload_success": "✅ File uploaded successfully!",
        "upload_error": "❌ Error reading file: {e}",
        "data_preview": "🔍 Data Preview (First 5 Rows)",
        "data_overview": "📋 Data Overview",
        "total_rows": "Total Rows",
        "total_cols": "Total Columns",
        "missing_vals": "Missing Values",
        "duplicate_rows": "Duplicate Rows",
        "data_cleaning": "🧹 Data Cleaning",
        "clean_btn": "Remove Duplicates & Drop Missing Values",
        "clean_success": "✅ Cleaned! Rows reduced from {initial} to {final}",
        "basic_filters": "🔎 Basic Filters",
        "filter_cat_col": "Filter by Category Column",
        "filter_keep_vals": "Select values to keep",
        "auto_viz": "📊 Auto-Generated Visualizations",
        "histogram_title": "### Distribution Histogram",
        "histogram_select": "Select a numeric column for histogram",
        "bar_chart_title": "### Category Bar Chart",
        "bar_cat_select": "Select category column for bar chart",
        "bar_num_select": "Select numeric column to aggregate",
        "heatmap_title": "### Correlation Heatmap",
        "pie_bar_select": "Select column for Pie/Bar Chart",
        "dist_title": "{col} Distribution",
        "key_metrics": "📈 Key Metrics",
        "key_col_select": "Select column for key metrics",
        "total_records": "Total Records",
        "mean_val": "Mean Value",
        "max_val": "Max Value",
        "min_val": "Min Value",
        "download_charts": "💾 Download Charts",
        "download_last_chart": "Download Last Chart as PNG",
        "download_png": "Download PNG",
        "no_numeric_cols": "⚠️ No numeric columns found in your dataset. Charts cannot be generated.",
        "initial_prompt": "👆 Please upload a CSV or Excel file to get started!",
        "supported_features": "### Supported Features:",
        "feature_1": "- ✅ CSV/Excel file upload",
        "feature_2": "- ✅ Data preview & overview",
        "feature_3": "- ✅ Basic data cleaning (remove duplicates, drop missing values)",
        "feature_4": "- ✅ Category filters",
        "feature_5": "- ✅ 4 types of visualizations (histogram, bar chart, pie chart, heatmap)",
        "feature_6": "- ✅ Key metrics cards",
        "feature_7": "- ✅ Chart download as PNG",
        "lang_switch": "Language / 语言"
    },
    "zh": {
        "page_title": "通用数据可视化分析仪表盘",
        "main_title": "📊 通用数据可视化分析仪表盘",
        "main_desc": "上传任意CSV或Excel文件，立即生成数据分析报告！",
        "sidebar_upload": "📁 上传数据文件",
        "upload_label": "上传CSV或Excel文件",
        "upload_success": "✅ 文件上传成功！",
        "upload_error": "❌ 读取文件失败: {e}",
        "data_preview": "🔍 数据预览（前5行）",
        "data_overview": "📋 数据概览",
        "total_rows": "总行数",
        "total_cols": "总列数",
        "missing_vals": "缺失值数量",
        "duplicate_rows": "重复行数量",
        "data_cleaning": "🧹 数据清洗",
        "clean_btn": "删除重复行 & 剔除缺失值",
        "clean_success": "✅ 清洗完成！行数从 {initial} 减少到 {final}",
        "basic_filters": "🔎 基础筛选",
        "filter_cat_col": "按分类列筛选",
        "filter_keep_vals": "选择保留的数值",
        "auto_viz": "📊 自动生成可视化图表",
        "histogram_title": "### 数值分布直方图",
        "histogram_select": "选择直方图的数值列",
        "bar_chart_title": "### 分类柱状对比图",
        "bar_cat_select": "选择柱状图的分类列",
        "bar_num_select": "选择聚合的数值列",
        "heatmap_title": "### 相关性热力图",
        "pie_bar_select": "选择饼图/条形图的列",
        "dist_title": "{col} 分布情况",
        "key_metrics": "📈 关键指标",
        "key_col_select": "选择关键指标的数值列",
        "total_records": "总记录数",
        "mean_val": "平均值",
        "max_val": "最大值",
        "min_val": "最小值",
        "download_charts": "💾 下载图表",
        "download_last_chart": "下载最后生成的图表为PNG",
        "download_png": "下载PNG文件",
        "no_numeric_cols": "⚠️ 数据集中未找到数值列，无法生成图表。",
        "initial_prompt": "👆 请上传CSV或Excel文件开始分析！",
        "supported_features": "### 支持功能：",
        "feature_1": "- ✅ CSV/Excel文件上传",
        "feature_2": "- ✅ 数据预览与概览",
        "feature_3": "- ✅ 基础数据清洗（删除重复行、剔除缺失值）",
        "feature_4": "- ✅ 分类列筛选",
        "feature_5": "- ✅ 4种可视化图表（直方图、柱状图、饼图、热力图）",
        "feature_6": "- ✅ 关键指标卡片",
        "feature_7": "- ✅ 图表导出为PNG格式",
        "lang_switch": "Language / 语言"
    }
}

# ===================== 核心功能 =====================
# 页面设置（动态标题）
st.set_page_config(page_title="通用数据可视化分析仪表盘", layout="wide")
plt.style.use('seaborn-v0_8')

# 侧边栏语言切换
st.sidebar.header(LANG_CONFIG["en"]["lang_switch"])
selected_lang = st.sidebar.radio("", ["en", "zh"], format_func=lambda x: "English" if x=="en" else "中文")
lang = LANG_CONFIG[selected_lang]

# 更新页面标题
st.set_page_config(page_title=lang["page_title"], layout="wide")

# 标题
st.title(lang["main_title"])
st.markdown(lang["main_desc"])

# 1. 文件上传模块
st.sidebar.header(lang["sidebar_upload"])
uploaded_file = st.sidebar.file_uploader(lang["upload_label"], type=["csv", "xlsx"])

if uploaded_file is not None:
    # 读取数据
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.sidebar.success(lang["upload_success"])
    except Exception as e:
        st.error(lang["upload_error"].format(e=e))
        st.stop()

    # 2. 数据预览
    st.subheader(lang["data_preview"])
    st.dataframe(df.head(), use_container_width=True)

    # 3. 数据概览卡片
    st.subheader(lang["data_overview"])
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(lang["total_rows"], df.shape[0])
    col2.metric(lang["total_cols"], df.shape[1])
    col3.metric(lang["missing_vals"], df.isnull().sum().sum())
    col4.metric(lang["duplicate_rows"], df.duplicated().sum())

    # 4. 基础数据清洗
    st.subheader(lang["data_cleaning"])
    if st.button(lang["clean_btn"]):
        initial_rows = df.shape[0]
        df = df.drop_duplicates().dropna()
        st.success(lang["clean_success"].format(initial=initial_rows, final=df.shape[0]))

    # 5. 侧边栏筛选（先做基础的）
    st.sidebar.header(lang["basic_filters"])
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    # 排除唯一ID字段，避免柱状图异常
    categorical_cols = [col for col in df.select_dtypes(include=['object', 'category']).columns.tolist() 
                    if not any(x in col.lower() for x in ['id','userid','user_id'])]

    if categorical_cols:
        selected_cat = st.sidebar.selectbox(lang["filter_cat_col"], categorical_cols)
        unique_values = df[selected_cat].dropna().unique()
        selected_values = st.sidebar.multiselect(lang["filter_keep_vals"], unique_values, default=unique_values)
        df = df[df[selected_cat].isin(selected_values)]

    # 6. 自动生成4种图表（核心部分）
    st.subheader(lang["auto_viz"])
    if numeric_cols:
        # 直方图（分布）
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(lang["histogram_title"])
            selected_num = st.selectbox(lang["histogram_select"], numeric_cols)
            fig, ax = plt.subplots()
            sns.histplot(df[selected_num].dropna(), kde=True, ax=ax)
            st.pyplot(fig)

        # 柱状对比图
        with col2:
            if categorical_cols:
                st.markdown(lang["bar_chart_title"])
                bar_cat = st.selectbox(lang["bar_cat_select"], categorical_cols)
                bar_num = st.selectbox(lang["bar_num_select"], numeric_cols)
                bar_data = df.groupby(bar_cat)[bar_num].mean().sort_values(ascending=False)
                fig, ax = plt.subplots()
                bar_data.plot(kind='bar', ax=ax)
                plt.xticks(rotation=45)
                st.pyplot(fig)

        # 相关性热力图
        if len(numeric_cols) >= 2:
            st.markdown(lang["heatmap_title"])
            corr = df[numeric_cols].corr()
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
            st.pyplot(fig)

        # 智能图表：自动判断类别数量，永不重叠
        if categorical_cols:
            pie_col = st.selectbox(lang["pie_bar_select"], categorical_cols, index=0)
            st.subheader(lang["dist_title"].format(col=pie_col))
            pie_data = df[pie_col].value_counts()

            # 类别超过10个 → 自动用横向条形图（避免重叠）
            if len(pie_data) > 10:
                fig, ax = plt.subplots(figsize=(10, 12))
                pie_data_sorted = pie_data.sort_values()
                pie_data_sorted.plot(kind='barh', ax=ax, color='#20A8D8')
                
                # 添加数值标签
                for i, v in enumerate(pie_data_sorted):
                    ax.text(v + 1, i, str(v), va='center', fontsize=10)
                
                plt.tight_layout()
                st.pyplot(fig)
            # 类别少 → 用饼图，好看清晰
            else:
                fig, ax = plt.subplots(figsize=(8, 8))
                ax.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%')
                ax.axis('equal')  # 保证饼图正圆
                plt.tight_layout()
                st.pyplot(fig)

        # 7. 关键指标卡片（扩展）
        st.subheader(lang["key_metrics"])
        key_col = st.selectbox(lang["key_col_select"], numeric_cols)
        mean_val = df[key_col].mean()
        max_val = df[key_col].max()
        min_val = df[key_col].min()
        count = df.shape[0]

        col1, col2, col3, col4 = st.columns(4)
        col1.metric(lang["total_records"], count)
        col2.metric(lang["mean_val"], round(mean_val, 2))
        col3.metric(lang["max_val"], round(max_val, 2))
        col4.metric(lang["min_val"], round(min_val, 2))

        # 8. 图表下载功能
        st.subheader(lang["download_charts"])
        if st.button(lang["download_last_chart"]):
            buf = BytesIO()
            plt.tight_layout()
            plt.savefig(buf, format='png', bbox_inches='tight')
            buf.seek(0)
            st.download_button(
                label=lang["download_png"],
                data=buf,
                file_name="chart.png",
                mime="image/png"
            )
    else:
        st.warning(lang["no_numeric_cols"])

else:
    # 初始状态提示
    st.info(lang["initial_prompt"])
    st.markdown(f"""
    {lang["supported_features"]}
    {lang["feature_1"]}
    {lang["feature_2"]}
    {lang["feature_3"]}
    {lang["feature_4"]}
    {lang["feature_5"]}
    {lang["feature_6"]}
    {lang["feature_7"]}
    """)