import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import datetime

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
        "lang_switch": "Language / 语言",
        # 新增报告相关配置
        "auto_report": "📑 Auto-Generated Analysis Report",
        "generate_report": "Generate Full Analysis Report",
        "report_download": "💾 Download Report",
        "download_md": "Download as Markdown",
        "download_html": "Download as HTML",
        "report_title": "Data Analysis Report",
        "report_generated": "Report generated at: {time}",
        "report_overview_section": "## 1. Data Overview",
        "report_cleaning_section": "## 2. Data Cleaning Summary",
        "report_no_cleaning": "No data cleaning operations were performed.",
        "report_metrics_section": "## 3. Key Metrics",
        "report_viz_section": "## 4. Visualization Insights",
        "report_histogram_insight": "- **Histogram Insight**: The column `{col}` shows a {distribution} distribution (KDE curve).",
        "report_bar_insight": "- **Bar Chart Insight**: In `{cat_col}`, the category `{top_cat}` has the highest average value of `{num_col}` ({top_val:.2f}).",
        "report_heatmap_insight": "- **Correlation Insight**: The strongest positive correlation is between `{col1}` and `{col2}` ({corr:.2f}), while the strongest negative correlation is between `{col3}` and `{col4}` ({corr_neg:.2f}).",
        "report_pie_insight": "- **Category Distribution Insight**: The largest category in `{col}` is `{top_cat}` ({top_pct:.1f}%).",
        "report_no_viz_insight": "- No visualization insights available (insufficient numeric/category columns).",
        "report_conclusion_section": "## 5. Conclusion",
        "report_conclusion": "This dataset contains {rows} records and {cols} columns. Key findings include: {findings}",
        "report_cleaning_log": "- {log}",
        "distribution_normal": "normal",
        "distribution_skewed_right": "right-skewed",
        "distribution_skewed_left": "left-skewed",
        "distribution_uniform": "uniform"
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
        "lang_switch": "Language / 语言",
        # 新增报告相关配置
        "auto_report": "📑 自动生成分析报告",
        "generate_report": "生成完整分析报告",
        "report_download": "💾 下载分析报告",
        "download_md": "导出为Markdown文件",
        "download_html": "导出为HTML文件",
        "report_title": "数据可视化分析报告",
        "report_generated": "报告生成时间: {time}",
        "report_overview_section": "## 1. 数据概览",
        "report_cleaning_section": "## 2. 数据清洗总结",
        "report_no_cleaning": "未执行任何数据清洗操作。",
        "report_metrics_section": "## 3. 关键指标",
        "report_viz_section": "## 4. 可视化洞察",
        "report_histogram_insight": "- **直方图洞察**：列 `{col}` 呈现{distribution}分布（KDE曲线）。",
        "report_bar_insight": "- **柱状图洞察**：在 `{cat_col}` 分类中，`{top_cat}` 类别的 `{num_col}` 平均值最高（{top_val:.2f}）。",
        "report_heatmap_insight": "- **相关性洞察**：`{col1}` 与 `{col2}` 呈最强正相关（{corr:.2f}），`{col3}` 与 `{col4}` 呈最强负相关（{corr_neg:.2f}）。",
        "report_pie_insight": "- **分类分布洞察**：`{col}` 列中占比最高的类别是 `{top_cat}`（{top_pct:.1f}%）。",
        "report_no_viz_insight": "- 无可视化洞察（数值列/分类列不足）。",
        "report_conclusion_section": "## 5. 总结结论",
        "report_conclusion": "该数据集包含 {rows} 条记录、{cols} 个字段。核心发现：{findings}",
        "report_cleaning_log": "- {log}",
        "distribution_normal": "正态",
        "distribution_skewed_right": "右偏",
        "distribution_skewed_left": "左偏",
        "distribution_uniform": "均匀"
    }
}

# ===================== 辅助函数：生成分析报告 =====================
def generate_analysis_report(df, cleaned_df, clean_log, numeric_cols, categorical_cols, lang):
    """生成结构化分析报告"""
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report = []
    
    # 标题
    report.append(f"# {lang['report_title']}")
    report.append(f"*{lang['report_generated'].format(time=current_time)}*\n")
    
    # 1. 数据概览
    report.append(lang['report_overview_section'])
    report.append(f"- 原始数据行数: {df.shape[0]} | 清洗后行数: {cleaned_df.shape[0]}")
    report.append(f"- 原始数据列数: {df.shape[1]} | 清洗后列数: {cleaned_df.shape[1]}")
    report.append(f"- 缺失值总数（原始）: {df.isnull().sum().sum()}")
    report.append(f"- 重复行总数（原始）: {df.duplicated().sum()}\n")
    
    # 2. 数据清洗总结
    report.append(lang['report_cleaning_section'])
    if clean_log:
        for log in clean_log:
            report.append(lang['report_cleaning_log'].format(log=log))
    else:
        report.append(lang['report_no_cleaning'])
    report.append("")
    
    # 3. 关键指标
    report.append(lang['report_metrics_section'])
    if numeric_cols:
        key_col = numeric_cols[0]  # 取第一个数值列作为代表
        metrics = {
            "total": cleaned_df.shape[0],
            "mean": round(cleaned_df[key_col].mean(), 2),
            "max": round(cleaned_df[key_col].max(), 2),
            "min": round(cleaned_df[key_col].min(), 2)
        }
        report.append(f"- {lang['total_records']}: {metrics['total']}")
        report.append(f"- {lang['mean_val']} ({key_col}): {metrics['mean']}")
        report.append(f"- {lang['max_val']} ({key_col}): {metrics['max']}")
        report.append(f"- {lang['min_val']} ({key_col}): {metrics['min']}")
    report.append("")
    
    # 4. 可视化洞察
    report.append(lang['report_viz_section'])
    if numeric_cols and categorical_cols:
        # 直方图洞察（判断分布类型）
        if numeric_cols:
            col = numeric_cols[0]
            data = cleaned_df[col].dropna()
            skewness = data.skew()
            if abs(skewness) < 0.5:
                dist_type = lang['distribution_normal']
            elif skewness > 0.5:
                dist_type = lang['distribution_skewed_right']
            else:
                dist_type = lang['distribution_skewed_left']
            report.append(lang['report_histogram_insight'].format(col=col, distribution=dist_type))
        
        # 柱状图洞察
        if categorical_cols and numeric_cols:
            cat_col = categorical_cols[0]
            num_col = numeric_cols[0]
            bar_data = cleaned_df.groupby(cat_col)[num_col].mean().sort_values(ascending=False)
            top_cat = bar_data.index[0] if len(bar_data) > 0 else "N/A"
            top_val = bar_data.iloc[0] if len(bar_data) > 0 else 0
            report.append(lang['report_bar_insight'].format(
                cat_col=cat_col, top_cat=top_cat, num_col=num_col, top_val=top_val
            ))
        
        # 热力图洞察
        if len(numeric_cols) >= 2:
            corr = cleaned_df[numeric_cols].corr()
            # 排除对角线，找最强正相关
            corr_no_diag = corr.mask(np.triu(np.ones(corr.shape)).astype(bool))
            max_corr = corr_no_diag.max().max()
            max_pair = corr_no_diag.stack().idxmax()
            # 找最强负相关
            min_corr = corr_no_diag.min().min()
            min_pair = corr_no_diag.stack().idxmin()
            report.append(lang['report_heatmap_insight'].format(
                col1=max_pair[0], col2=max_pair[1], corr=round(max_corr, 2),
                col3=min_pair[0], col4=min_pair[1], corr_neg=round(min_corr, 2)
            ))
        
        # 饼图/条形图洞察
        if categorical_cols:
            pie_col = categorical_cols[0]
            pie_data = cleaned_df[pie_col].value_counts()
            if len(pie_data) > 0:
                top_cat = pie_data.index[0]
                top_pct = (pie_data.iloc[0] / pie_data.sum()) * 100
                report.append(lang['report_pie_insight'].format(
                    col=pie_col, top_cat=top_cat, top_pct=top_pct
                ))
    else:
        report.append(lang['report_no_viz_insight'])
    report.append("")
    
    # 5. 总结结论
    report.append(lang['report_conclusion_section'])
    findings = []
    if cleaned_df.shape[0] < df.shape[0]:
        findings.append(f"数据清洗后行数减少 {df.shape[0] - cleaned_df.shape[0]} 条")
    if numeric_cols:
        findings.append(f"核心数值列 {numeric_cols[0]} 平均值为 {round(cleaned_df[numeric_cols[0]].mean(), 2)}")
    if not findings:
        findings.append("数据集结构完整，无明显异常")
    report.append(lang['report_conclusion'].format(
        rows=cleaned_df.shape[0], cols=cleaned_df.shape[1],
        findings="；".join(findings)
    ))
    
    # 拼接报告
    final_report = "\n".join(report)
    return final_report

# ===================== 核心功能 =====================
# 页面设置（动态标题）
st.set_page_config(page_title="通用数据可视化分析仪表盘", layout="wide")
plt.style.use('seaborn-v0_8')

# 初始化session_state
if "clean_log" not in st.session_state:
    st.session_state["clean_log"] = []
if "analysis_report" not in st.session_state:
    st.session_state["analysis_report"] = ""

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

    # 4. 精细化数据清洗
    st.subheader("🧹 Advanced Data Cleaning")
    
    # 初始化session_state存储原始数据
    if "original_df" not in st.session_state:
        st.session_state["original_df"] = df.copy()
    if "cleaned_df" not in st.session_state:
        st.session_state["cleaned_df"] = df.copy()
    
    # 重置数据按钮
    if st.button("🔄 Reset to Original Data"):
        df = st.session_state["original_df"].copy()
        st.session_state["cleaned_df"] = df.copy()
        st.session_state["clean_log"] = []
        st.success("✅ Data reset to original state!")

    # ---- 4.1 缺失值处理 ----
    st.markdown("#### Step 1: Handle Missing Values")
    missing_strategy = st.selectbox(
        "Select strategy for missing values",
        [
            "Keep as is",
            "Drop rows with missing values",
            "Drop columns with missing values",
            "Fill with mean (numeric columns)",
            "Fill with median (numeric columns)",
            "Fill with mode (category columns)",
            "Custom value fill"
        ],
        index=0
    )
    # 自定义填充值（仅选中时显示）
    custom_fill_val = None
    if missing_strategy == "Custom value fill":
        custom_fill_val = st.text_input("Enter custom value to fill missing values", value="0")

    # ---- 4.2 重复值处理 ----
    st.markdown("#### Step 2: Handle Duplicate Rows")
    dup_strategy = st.radio(
        "Select strategy for duplicate rows",
        [
            "Keep as is",
            "Drop all duplicates",
            "Keep first duplicate",
            "Keep last duplicate"
        ],
        index=0
    )

    # ---- 4.3 异常值处理（仅数值列） ----
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_cols = [col for col in df.select_dtypes(include=['object', 'category']).columns.tolist() 
                    if not any(x in col.lower() for x in ['id','userid','user_id'])]
    
    outlier_strategy = "Keep as is"
    outlier_cols = []
    if numeric_cols:
        st.markdown("#### Step 3: Handle Outliers (Numeric Columns Only)")
        outlier_strategy = st.selectbox(
            "Select strategy for outliers (IQR method)",
            [
                "Keep as is",
                "Drop rows with outliers",
                "Cap outliers (truncate to IQR range)"
            ],
            index=0
        )
        # 选择要处理异常值的列
        outlier_cols = st.multiselect(
            "Select columns to handle outliers",
            numeric_cols,
            default=numeric_cols[:1] if numeric_cols else []
        )

    # ---- 4.4 执行清洗 ----
    if st.button("🚀 Execute All Cleaning Steps"):
        # 基于原始数据重新清洗（避免叠加）
        df = st.session_state["original_df"].copy()
        clean_log = []
        initial_rows = df.shape[0]
        initial_cols = df.shape[1]

        # 执行缺失值处理
        if missing_strategy != "Keep as is":
            if missing_strategy == "Drop rows with missing values":
                before_drop = df.shape[0]
                df = df.dropna()
                clean_log.append(f"Deleted {before_drop - df.shape[0]} rows with missing values")
            elif missing_strategy == "Drop columns with missing values":
                before_drop = df.shape[1]
                df = df.dropna(axis=1)
                clean_log.append(f"Deleted {before_drop - df.shape[1]} columns with missing values")
            elif missing_strategy == "Fill with mean (numeric columns)":
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                clean_log.append("Filled missing values in numeric columns with mean")
            elif missing_strategy == "Fill with median (numeric columns)":
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
                clean_log.append("Filled missing values in numeric columns with median")
            elif missing_strategy == "Fill with mode (category columns)":
                for col in categorical_cols:
                    df[col] = df[col].fillna(df[col].mode()[0])
                clean_log.append("Filled missing values in category columns with mode")
            elif missing_strategy == "Custom value fill":
                df = df.fillna(custom_fill_val)
                clean_log.append(f"Filled all missing values with custom value: {custom_fill_val}")

        # 执行重复值处理
        if dup_strategy != "Keep as is":
            before_dup = df.shape[0]
            if dup_strategy == "Drop all duplicates":
                df = df.drop_duplicates(keep=False)
            elif dup_strategy == "Keep first duplicate":
                df = df.drop_duplicates(keep="first")
            elif dup_strategy == "Keep last duplicate":
                df = df.drop_duplicates(keep="last")
            clean_log.append(f"Deleted {before_dup - df.shape[0]} duplicate rows")

        # 执行异常值处理
        if outlier_strategy != "Keep as is" and outlier_cols:
            before_outlier = df.shape[0]
            for col in outlier_cols:
                q1 = df[col].quantile(0.25)
                q3 = df[col].quantile(0.75)
                iqr = q3 - q1
                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr

                if outlier_strategy == "Drop rows with outliers":
                    df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
                elif outlier_strategy == "Cap outliers (truncate to IQR range)":
                    df[col] = df[col].clip(lower=lower_bound, upper=upper_bound)
            clean_log.append(f"Processed outliers in {outlier_cols}: Rows changed from {before_outlier} to {df.shape[0]}")

        # 更新清洗后的数据 & 提示日志
        st.session_state["cleaned_df"] = df.copy()
        st.session_state["clean_log"] = clean_log
        st.success("✅ All cleaning steps executed!")
        for log in clean_log:
            st.info(f"→ {log}")
        st.metric("Final Rows", df.shape[0], delta=df.shape[0]-initial_rows)
        st.metric("Final Columns", df.shape[1], delta=df.shape[1]-initial_cols)

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
    
    # 9. 清洗后数据下载
    st.subheader("💾 Download Cleaned Data")
    if st.button("Generate Cleaned Data File"):
        # 保存为CSV
        csv_buf = BytesIO()
        st.session_state["cleaned_df"].to_csv(csv_buf, index=False)
        csv_buf.seek(0)
    
        st.download_button(
            label="Download Cleaned CSV",
            data=csv_buf,
            file_name="cleaned_data.csv",
            mime="text/csv"
        )
    
        # 可选：Excel下载
        excel_buf = BytesIO()
        st.session_state["cleaned_df"].to_excel(excel_buf, index=False, engine='openpyxl')
        excel_buf.seek(0)
    
        st.download_button(
            label="Download Cleaned Excel",
            data=excel_buf,
            file_name="cleaned_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    # ===================== 新增：自动生成分析报告模块 =====================
    st.subheader(lang["auto_report"])
    # 刷新数值列/分类列（基于清洗后的数据）
    cleaned_df = st.session_state["cleaned_df"]
    numeric_cols_clean = cleaned_df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_cols_clean = [col for col in cleaned_df.select_dtypes(include=['object', 'category']).columns.tolist() 
                            if not any(x in col.lower() for x in ['id','userid','user_id'])]
    
    # 生成报告按钮
    if st.button(lang["generate_report"]):
        with st.spinner("Generating report... / 正在生成报告..."):
            report = generate_analysis_report(
                df=st.session_state["original_df"],
                cleaned_df=cleaned_df,
                clean_log=st.session_state["clean_log"],
                numeric_cols=numeric_cols_clean,
                categorical_cols=categorical_cols_clean,
                lang=lang
            )
            st.session_state["analysis_report"] = report
        
        # 展示报告
        st.markdown(report)
    
    # 报告下载功能（仅当报告生成后显示）
    if st.session_state["analysis_report"]:
        st.subheader(lang["report_download"])
        report_content = st.session_state["analysis_report"]
        
        # Markdown下载
        md_buf = BytesIO(report_content.encode('utf-8'))
        st.download_button(
            label=lang["download_md"],
            data=md_buf,
            file_name=f"analysis_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown"
        )
        
        # HTML下载（简单转换Markdown为HTML）
        import markdown
        html_content = markdown.markdown(report_content)
        html_buf = BytesIO(html_content.encode('utf-8'))
        st.download_button(
            label=lang["download_html"],
            data=html_buf,
            file_name=f"analysis_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
            mime="text/html"
        )
        
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
    - ✅ Auto-generated analysis report (Markdown/HTML download) / 自动生成分析报告（支持Markdown/HTML下载）
    """)