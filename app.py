import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import datetime
import markdown

# 核心多语言字典（你原来的，保持不动）
LANG_CONFIG = {
    "en": {
        "page_title": "Universal Data Visualization Dashboard",
        "main_title": "📊 Universal Data Analysis Dashboard",
        "main_desc": "Upload your CSV/Excel file for automatic cleaning, visualization and analysis",
        "lang_switch": "Language",
        "initial_prompt": "Please upload a CSV or Excel file to start analysis.",
        "supported_features": "Supported Features",
        "feature_1": "CSV / Excel file upload",
        "feature_2": "Data preview & overview",
        "feature_3": "Advanced data cleaning (missing values, duplicates, outliers)",
        "feature_4": "Category column filtering",
        "feature_5": "Automatic chart generation (histogram, bar, heatmap, pie)",
        "feature_6": "Key metrics display",
        "feature_7": "Chart export as PNG",
        "feature_8": "Automatic analysis report (Markdown / HTML)",

        "sidebar_upload": "File Upload",
        "upload_label": "Upload CSV/Excel file",
        "upload_success": "File uploaded successfully!",
        "upload_error": "Failed to read file: {e}",
        "basic_filters": "Basic Filters",
        "filter_cat_col": "Filter by Category Column",
        "filter_keep_vals": "Select values to keep",

        "data_preview": "Data Preview",
        "data_overview": "Data Overview",
        "total_rows": "Total Rows",
        "total_cols": "Total Columns",
        "missing_vals": "Missing Values",
        "duplicate_rows": "Duplicate Rows",

        "advanced_data_cleaning": "Advanced Data Cleaning",
        "reset_data": "Reset to Original Data",
        "reset_success": "Data reset to original state!",

        "step1_missing_title": "Step 1: Handle Missing Values",
        "missing_strategy_label": "Select strategy for missing values",
        "missing_keep": "Keep as is",
        "missing_drop_rows": "Drop rows with missing values",
        "missing_drop_cols": "Drop columns with missing values",
        "missing_fill_mean": "Fill with mean (numeric columns)",
        "missing_fill_median": "Fill with median (numeric columns)",
        "missing_fill_mode": "Fill with mode (category columns)",
        "missing_fill_custom": "Custom value fill",
        "custom_fill_tip": "Enter custom value to fill missing values",

        "step2_dup_title": "Step 2: Handle Duplicate Rows",
        "dup_strategy_label": "Select strategy for duplicate rows",
        "dup_keep": "Keep as is",
        "dup_drop_all": "Drop all duplicates",
        "dup_keep_first": "Keep first duplicate",
        "dup_keep_last": "Keep last duplicate",

        "step3_outlier_title": "Step 3: Handle Outliers (Numeric Columns Only)",
        "outlier_strategy_label": "Select strategy for outliers (IQR method)",
        "outlier_keep": "Keep as is",
        "outlier_drop": "Drop rows with outliers",
        "outlier_cap": "Cap outliers (truncate to IQR range)",
        "outlier_cols_label": "Select columns to handle outliers",
        "execute_clean": "Execute All Cleaning Steps",
        "clean_success": "All cleaning steps executed!",

        "auto_viz": "Automatic Visualization",
        "histogram_title": "Histogram (Value Distribution)",
        "histogram_select": "Select Numeric Column for Histogram",
        "bar_chart_title": "Bar Chart (Category vs Numeric)",
        "bar_cat_select": "Select Category Column for Bar Chart",
        "bar_num_select": "Select Numeric Column for Bar Chart",
        "heatmap_title": "Correlation Heatmap",
        "dist_title": "Distribution of {col}",
        "pie_bar_select": "Select Category Column for Pie Chart",

        "key_metrics": "Key Metrics",
        "key_col_select": "Select Metric Column for Key Metrics",
        "total_records": "Total Records",
        "mean_val": "Mean Value",
        "max_val": "Max Value",
        "min_val": "Min Value",

        "download_charts": "Download Charts",
        "download_last_chart": "Prepare Last Chart for Download",
        "download_png": "Download PNG",

        "download_cleaned_data": "Download Cleaned Data",
        "Generate Cleaned Data File": "Generate Cleaned Data File",
        "Download Cleaned CSV": "Download Cleaned CSV",
        "Download Cleaned Excel": "Download Cleaned Excel",

        "auto_report": "Automatic Analysis Report",
        "generate_report": "Generate Analysis Report",
        "report_download": "Download Report",
        "download_md": "Download Markdown Report",
        "download_html": "Download HTML Report",
        "report_title": "Data Analysis Report",
        "report_generated": "Report generated at: {time}",
        "report_overview_section": "Data Overview",
        "report_cleaning_section": "Data Cleaning Summary",
        "report_cleaning_log": "- {log}",
        "report_no_cleaning": "No cleaning steps were performed",
        "report_metrics_section": "Key Metrics",
        "report_viz_section": "Visualization Insights",
        "distribution_normal": "Normal Distribution",
        "distribution_skewed_right": "Right-Skewed Distribution",
        "distribution_skewed_left": "Left-Skewed Distribution",
        "report_histogram_insight": "- Histogram of {col}: {distribution}",
        "report_bar_insight": "- Bar Chart: {top_cat} has the highest {num_col} value ({top_val})",
        "report_heatmap_insight": "- Heatmap: Strongest positive correlation ({corr}) between {col1} & {col2}; Strongest negative correlation ({corr_neg}) between {col3} & {col4}",
        "report_pie_insight": "- Pie Chart: {top_cat} accounts for {top_pct:.1f}% of {col}",
        "report_no_viz_insight": "- Insufficient data for visualization insights",
        "report_conclusion_section": "Conclusion",
        "report_conclusion": "The cleaned dataset has {rows} rows and {cols} columns. Key findings: {findings}",
        "no_numeric_cols": "No numeric columns found for visualization!"
    },
    "zh": {
        "page_title": "通用数据可视化分析仪表盘",
        "main_title": "📊 通用数据可视化分析仪表盘",
        "main_desc": "上传CSV/Excel文件，自动完成数据清洗、可视化与分析",
        "lang_switch": "语言",
        "initial_prompt": "请上传CSV或Excel文件开始分析",
        "supported_features": "支持功能",
        "feature_1": "CSV / Excel 文件上传",
        "feature_2": "数据预览与概览",
        "feature_3": "高级数据清洗（缺失值、重复值、异常值）",
        "feature_4": "分类列筛选",
        "feature_5": "自动生成图表（直方图、柱状图、热力图、饼图）",
        "feature_6": "关键指标展示",
        "feature_7": "图表导出为PNG",
        "feature_8": "自动生成分析报告（Markdown / HTML）",

        "sidebar_upload": "文件上传",
        "upload_label": "上传CSV/Excel文件",
        "upload_success": "文件上传成功！",
        "upload_error": "读取文件失败：{e}",
        "basic_filters": "基础筛选",
        "filter_cat_col": "按分类列筛选",
        "filter_keep_vals": "选择保留的数值",

        "data_preview": "数据预览",
        "data_overview": "数据概览",
        "total_rows": "总行数",
        "total_cols": "总列数",
        "missing_vals": "缺失值总数",
        "duplicate_rows": "重复行数",

        "advanced_data_cleaning": "高级数据清洗",
        "reset_data": "重置为原始数据",
        "reset_success": "数据已重置为原始状态！",

        "step1_missing_title": "步骤1：处理缺失值",
        "missing_strategy_label": "选择缺失值处理策略",
        "missing_keep": "保持不变",
        "missing_drop_rows": "删除含缺失值的行",
        "missing_drop_cols": "删除含缺失值的列",
        "missing_fill_mean": "数值列填充均值",
        "missing_fill_median": "数值列填充中位数",
        "missing_fill_mode": "分类列填充众数",
        "missing_fill_custom": "自定义值填充",
        "custom_fill_tip": "输入用于填充缺失值的自定义数值",

        "step2_dup_title": "步骤2：处理重复行",
        "dup_strategy_label": "选择重复行处理策略",
        "dup_keep": "保持不变",
        "dup_drop_all": "删除全部重复行",
        "dup_keep_first": "保留第一条重复数据",
        "dup_keep_last": "保留最后一条重复数据",

        "step3_outlier_title": "步骤3：处理异常值（仅数值列）",
        "outlier_strategy_label": "选择异常值处理策略（IQR方法）",
        "outlier_keep": "保持不变",
        "outlier_drop": "删除含异常值的行",
        "outlier_cap": "截断异常值（限制在IQR区间）",
        "outlier_cols_label": "选择需要处理异常值的列",
        "execute_clean": "执行全部清洗步骤",
        "clean_success": "所有清洗步骤已完成！",

        "auto_viz": "自动可视化",
        "histogram_title": "直方图（数值分布）",
        "histogram_select": "选择直方图数值列",
        "bar_chart_title": "柱状图（分类 vs 数值）",
        "bar_cat_select": "选择柱状图分类列",
        "bar_num_select": "选择柱状图数值列",
        "heatmap_title": "相关性热力图",
        "dist_title": "{col} 分布情况",
        "pie_bar_select": "选择饼图分类列",

        "key_metrics": "关键指标",
        "key_col_select": "选择关键指标数值列",
        "total_records": "总记录数",
        "mean_val": "平均值",
        "max_val": "最大值",
        "min_val": "最小值",

        "download_charts": "下载图表",
        "download_last_chart": "准备下载最后一张图表",
        "download_png": "下载PNG图片",

        "download_cleaned_data": "下载清洗后的数据",
        "Generate Cleaned Data File": "生成清洗后数据文件",
        "Download Cleaned CSV": "下载清洗后CSV",
        "Download Cleaned Excel": "下载清洗后Excel",

        "auto_report": "自动生成分析报告",
        "generate_report": "生成分析报告",
        "report_download": "下载报告",
        "download_md": "下载Markdown报告",
        "download_html": "下载HTML报告",
        "report_title": "数据分析报告",
        "report_generated": "报告生成时间：{time}",
        "report_overview_section": "数据概览",
        "report_cleaning_section": "数据清洗总结",
        "report_cleaning_log": "- {log}",
        "report_no_cleaning": "未执行任何清洗步骤",
        "report_metrics_section": "关键指标",
        "report_viz_section": "可视化洞察",
        "distribution_normal": "正态分布",
        "distribution_skewed_right": "右偏分布",
        "distribution_skewed_left": "左偏分布",
        "report_histogram_insight": "- {col} 直方图：{distribution}",
        "report_bar_insight": "- 柱状图：{top_cat} 的 {num_col} 均值最高（{top_val}）",
        "report_heatmap_insight": "- 热力图：{col1} 与 {col2} 正相关性最强（{corr}）；{col3} 与 {col4} 负相关性最强（{corr_neg}）",
        "report_pie_insight": "- 饼图：{top_cat} 占 {col} 的 {top_pct:.1f}%",
        "report_no_viz_insight": "- 数据不足，无法生成可视化洞察",
        "report_conclusion_section": "总结结论",
        "report_conclusion": "清洗后数据集包含 {rows} 行、{cols} 列。核心发现：{findings}",
        "no_numeric_cols": "未找到数值列，无法进行可视化！"
    }
}

# ===================== 辅助函数：生成分析报告 =====================
def generate_analysis_report(df, cleaned_df, clean_log, numeric_cols, categorical_cols, lang):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report = []
    report.append(f"# {lang['report_title']}")
    report.append(f"*{lang['report_generated'].format(time=current_time)}*\n")
    report.append(lang['report_overview_section'])
    report.append(f"- 原始数据行数: {df.shape[0]} | 清洗后行数: {cleaned_df.shape[0]}")
    report.append(f"- 原始数据列数: {df.shape[1]} | 清洗后列数: {cleaned_df.shape[1]}")
    report.append(f"- 缺失值总数（原始）: {df.isnull().sum().sum()}")
    report.append(f"- 重复行总数（原始）: {df.duplicated().sum()}\n")
    report.append(lang['report_cleaning_section'])
    if clean_log:
        for log in clean_log:
            report.append(lang['report_cleaning_log'].format(log=log))
    else:
        report.append(lang['report_no_cleaning'])
    report.append("")
    report.append(lang['report_metrics_section'])
    if numeric_cols:
        key_col = numeric_cols[0]
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
    report.append(lang['report_viz_section'])
    if numeric_cols and categorical_cols:
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
        if categorical_cols and numeric_cols:
            cat_col = categorical_cols[0]
            num_col = numeric_cols[0]
            bar_data = cleaned_df.groupby(cat_col)[num_col].mean().sort_values(ascending=False)
            top_cat = bar_data.index[0] if len(bar_data) > 0 else "N/A"
            top_val = bar_data.il[0] if len(bar_data) > 0 else 0
            report.append(lang['report_bar_insight'].format(cat_col=cat_col, top_cat=top_cat, num_col=num_col, top_val=top_val))
        if len(numeric_cols) >= 2:
            corr = cleaned_df[numeric_cols].corr()
            corr_no_diag = corr.mask(np.triu(np.ones(corr.shape)).astype(bool))
            max_corr = corr_no_diag.max().max()
            max_pair = corr_no_diag.stack().idxmax()
            min_corr = corr_no_diag.min().min()
            min_pair = corr_no_diag.stack().idxmin()
            report.append(lang['report_heatmap_insight'].format(
                col1=max_pair[0], col2=max_pair[1], corr=round(max_corr, 2),
                col3=min_pair[0], col4=min_pair[1], corr_neg=round(min_corr, 2)
            ))
        if categorical_cols:
            pie_col = categorical_cols[0]
            pie_data = cleaned_df[pie_col].value_counts()
            if len(pie_data) > 0:
                top_cat = pie_data.index[0]
                top_pct = (pie_data.iloc[0] / pie_data.sum()) * 100
                report.append(lang['report_pie_insight'].format(col=pie_col, top_cat=top_cat, top_pct=top_pct))
    else:
        report.append(lang['report_no_viz_insight'])
    report.append("")
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
    return "\n".join(report)

# ===================== 核心功能 =====================
st.set_page_config(page_title="Dashboard", layout="wide")
plt.style.use('seaborn-v0_8')

if "clean_log" not in st.session_state:
    st.session_state["clean_log"] = []
if "analysis_report" not in st.session_state:
    st.session_state["analysis_report"] = ""

# 语言切换
st.sidebar.header(LANG_CONFIG["en"]["lang_switch"])
selected_lang = st.sidebar.radio("", ["en", "zh"], format_func=lambda x: "English" if x == "en" else "中文")
lang = LANG_CONFIG[selected_lang]

st.set_page_config(page_title=lang["page_title"], layout="wide")
st.title(lang["main_title"])
st.markdown(lang["main_desc"])

# 文件上传
st.sidebar.header(lang["sidebar_upload"])
uploaded_file = st.sidebar.file_uploader(lang["upload_label"], type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.sidebar.success(lang["upload_success"])
    except Exception as e:
        st.error(lang["upload_error"].format(e=e))
        st.stop()

    # 数据预览
    st.subheader(lang["data_preview"])
    st.dataframe(df.head(), use_container_width=True)

    # 数据概览
    st.subheader(lang["data_overview"])
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(lang["total_rows"], df.shape[0])
    c2.metric(lang["total_cols"], df.shape[1])
    c3.metric(lang["missing_vals"], df.isnull().sum().sum())
    c4.metric(lang["duplicate_rows"], df.duplicated().sum())

    # 高级数据清洗（全部语言化）
    st.subheader(lang["advanced_data_cleaning"])

    if "original_df" not in st.session_state:
        st.session_state["original_df"] = df.copy()
    if "cleaned_df" not in st.session_state:
        st.session_state["cleaned_df"] = df.copy()

    if st.button(lang["reset_data"]):
        df = st.session_state["original_df"].copy()
        st.session_state["cleaned_df"] = df.copy()
        st.session_state["clean_log"] = []
        st.success(lang["reset_success"])

    # 缺失值
    st.markdown(f"#### {lang['step1_missing_title']}")
    missing_strategy = st.selectbox(
        lang["missing_strategy_label"],
        [
            lang["missing_keep"],
            lang["missing_drop_rows"],
            lang["missing_drop_cols"],
            lang["missing_fill_mean"],
            lang["missing_fill_median"],
            lang["missing_fill_mode"],
            lang["missing_fill_custom"]
        ]
    )
    custom_fill_val = None
    if missing_strategy == lang["missing_fill_custom"]:
        custom_fill_val = st.text_input(lang["custom_fill_tip"], value="0")

    # 重复值
    st.markdown(f"#### {lang['step2_dup_title']}")
    dup_strategy = st.radio(
        lang["dup_strategy_label"],
        [
            lang["dup_keep"],
            lang["dup_drop_all"],
            lang["dup_keep_first"],
            lang["dup_keep_last"]
        ]
    )

    # 异常值
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_cols = [col for col in df.select_dtypes(include=['object', 'category']).columns.tolist() if not any(x in col.lower() for x in ['id','userid','user_id'])]
    outlier_strategy = lang["outlier_keep"]
    outlier_cols = []

    if numeric_cols:
        st.markdown(f"#### {lang['step3_outlier_title']}")
        outlier_strategy = st.selectbox(
            lang["outlier_strategy_label"],
            [
                lang["outlier_keep"],
                lang["outlier_drop"],
                lang["outlier_cap"]
            ]
        )
        outlier_cols = st.multiselect(lang["outlier_cols_label"], numeric_cols)

    # 执行清洗
    if st.button(lang["execute_clean"]):
        df = st.session_state["original_df"].copy()
        clean_log = []
        # 缺失值
        if missing_strategy == lang["missing_drop_rows"]:
            df = df.dropna()
        elif missing_strategy == lang["missing_drop_cols"]:
            df = df.dropna(axis=1)
        elif missing_strategy == lang["missing_fill_mean"]:
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
        elif missing_strategy == lang["missing_fill_median"]:
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
        elif missing_strategy == lang["missing_fill_mode"]:
            for c in categorical_cols:
                df[c] = df[c].fillna(df[c].mode()[0])
        elif missing_strategy == lang["missing_fill_custom"]:
            df = df.fillna(custom_fill_val)
        # 重复值
        if dup_strategy == lang["dup_drop_all"]:
            df = df.drop_duplicates(keep=False)
        elif dup_strategy == lang["dup_keep_first"]:
            df = df.drop_duplicates(keep="first")
        elif dup_strategy == lang["dup_keep_last"]:
            df = df.drop_duplicates(keep="last")
        # 异常值
        if outlier_strategy != lang["outlier_keep"] and outlier_cols:
            for c in outlier_cols:
                q1 = df[c].quantile(0.25)
                q3 = df[c].quantile(0.75)
                iqr = q3 - q1
                low = q1 - 1.5 * iqr
                high = q3 + 1.5 * iqr
                if outlier_strategy == lang["outlier_drop"]:
                    df = df[(df[c] >= low) & (df[c] <= high)]
                elif outlier_strategy == lang["outlier_cap"]:
                    df[c] = df[c].clip(low, high)
        st.session_state["cleaned_df"] = df.copy()
        st.success(lang["clean_success"])

    # 筛选
    st.sidebar.header(lang["basic_filters"])
    if categorical_cols:
        sc = st.sidebar.selectbox(lang["filter_cat_col"], categorical_cols)
        vs = df[sc].dropna().unique()
        sv = st.sidebar.multiselect(lang["filter_keep_vals"], vs, default=vs)
        df = df[df[sc].isin(sv)]

    # 可视化
    st.subheader(lang["auto_viz"])
    if numeric_cols:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(lang["histogram_title"])
            s = st.selectbox(lang["histogram_select"], numeric_cols, key="h1")
            fig, ax = plt.subplots()
            sns.histplot(df[s].dropna(), kde=True, ax=ax)
            st.pyplot(fig)
        with c2:
            if categorical_cols:
                st.markdown(lang["bar_chart_title"])
                bc = st.selectbox(lang["bar_cat_select"], categorical_cols, key="b1")
                bn = st.selectbox(lang["bar_num_select"], numeric_cols, key="b2")
                d = df.groupby(bc)[bn].mean().sort_values(ascending=False)
                fig, ax = plt.subplots()
                d.plot(kind='bar', ax=ax)
                plt.xticks(rotation=45)
                st.pyplot(fig)
        if len(numeric_cols) >= 2:
            st.markdown(lang["heatmap_title"])
            corr = df[numeric_cols].corr()
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
            st.pyplot(fig)
        if categorical_cols:
            pc = st.selectbox(lang["pie_bar_select"], categorical_cols, key="p1")
            st.subheader(lang["dist_title"].format(col=pc))
            pd = df[pc].value_counts()
            if len(pd) > 10:
                fig, ax = plt.subplots(figsize=(10, 12))
                pd.sort_values().plot(kind='barh', ax=ax, color='#20A8D8')
                st.pyplot(fig)
            else:
                fig, ax = plt.subplots(figsize=(8, 8))
                ax.pie(pd, labels=pd.index, autopct='%1.1f%%')
                ax.axis('equal')
                st.pyplot(fig)
        # 指标
        st.subheader(lang["key_metrics"])
        kc = st.selectbox(lang["key_col_select"], numeric_cols)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric(lang["total_records"], df.shape[0])
        c2.metric(lang["mean_val"], round(df[kc].mean(), 2))
        c3.metric(lang["max_val"], round(df[kc].max(), 2))
        c4.metric(lang["min_val"], round(df[kc].min(), 2))
        # 下载图表
        st.subheader(lang["download_charts"])
        if st.button(lang["download_last_chart"]):
            buf = BytesIO()
            plt.tight_layout()
            plt.savefig(buf, format='png', bbox_inches='tight')
            buf.seek(0)
            st.download_button(label=lang["download_png"], data=buf, file_name="chart.png", mime="image/png")
    else:
        st.warning(lang["no_numeric_cols"])

    # 下载清洗数据
    st.subheader(lang["download_cleaned_data"])
    if st.button(lang["Generate Cleaned Data File"]):
        csv_buf = BytesIO()
        st.session_state["cleaned_df"].to_csv(csv_buf, index=False)
        csv_buf.seek(0)
        st.download_button(label=lang["Download Cleaned CSV"], data=csv_buf, file_name="cleaned.csv", mime="text/csv")

        excel_buf = BytesIO()
        st.session_state["cleaned_df"].to_excel(excel_buf, index=False, engine='openpyxl')
        excel_buf.seek(0)
        st.download_button(label=lang["Download Cleaned Excel"], data=excel_buf, file_name="cleaned.xlsx", mime="excel")

    # 报告
    st.subheader(lang["auto_report"])
    if st.button(lang["generate_report"]):
        with st.spinner("..."):
            rep = generate_analysis_report(
                st.session_state["original_df"],
                st.session_state["cleaned_df"],
                st.session_state["clean_log"],
                numeric_cols, categorical_cols, lang
            )
            st.session_state["analysis_report"] = rep
        st.markdown(rep)

    if st.session_state["analysis_report"]:
        st.subheader(lang["report_download"])
        r = st.session_state["analysis_report"]
        st.download_button(label=lang["download_md"], data=r.encode(), file_name="report.md", mime="text/markdown")
        html = markdown.markdown(r)
        st.download_button(label=lang["download_html"], data=html.encode(), file_name="report.html", mime="text/html")

else:
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
    {lang["feature_8"]}
    """)