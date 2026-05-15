import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO, StringIO
import datetime
import markdown
import zipfile  # 新增：用于ZIP打包
import base64   # 新增：处理ZIP文件下载

# 核心多语言字典（新增ZIP相关配置）
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
        "feature_9": "Download all charts as ZIP",  # 新增

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
        "download_last_chart": "Download Last Generated Chart (PNG)",  # 优化文案
        "download_png": "Download PNG",
        "download_all_charts": "Download All Charts (ZIP)",  # 新增
        "no_charts_to_download": "No charts generated yet! Please create visualizations first.",  # 新增
        "zip_filename": "data_visualizations_{time}.zip",  # 新增
        "download_zip": "Download ZIP File",  # 新增

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
        "feature_9": "一键下载所有图表为ZIP压缩包",  # 新增

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
        "download_last_chart": "下载最后生成的图表（PNG）",  # 优化文案
        "download_png": "下载PNG图片",
        "download_all_charts": "下载所有图表（ZIP压缩包）",  # 新增
        "no_charts_to_download": "暂无生成的图表！请先创建可视化图表。",  # 新增
        "zip_filename": "数据可视化图表_{time}.zip",  # 新增
        "download_zip": "下载ZIP压缩包",  # 新增

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

# ===================== 新增辅助函数：保存图表到BytesIO =====================
def save_plot_to_bytes(fig, dpi=300):
    """将matplotlib图表保存为BytesIO对象（PNG格式）"""
    buf = BytesIO()
    fig.savefig(buf, format='png', dpi=dpi, bbox_inches='tight')
    buf.seek(0)
    return buf

# ===================== 新增辅助函数：打包所有图表为ZIP =====================
def create_charts_zip(charts_dict):
    """将所有图表打包为ZIP文件，返回BytesIO对象"""
    zip_buf = BytesIO()
    with zipfile.ZipFile(zip_buf, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for chart_name, chart_buf in charts_dict.items():
            # 清理文件名特殊字符
            safe_name = chart_name.replace('/', '_').replace('\\', '_').replace(':', '_')
            zipf.writestr(f"{safe_name}.png", chart_buf.getvalue())
    zip_buf.seek(0)
    return zip_buf

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
            top_val = bar_data.iloc[0] if len(bar_data) > 0 else 0
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

# 初始化Session State
if "clean_log" not in st.session_state:
    st.session_state["clean_log"] = []
if "analysis_report" not in st.session_state:
    st.session_state["analysis_report"] = ""
if "generated_charts" not in st.session_state:  # 新增：存储所有生成的图表
    st.session_state["generated_charts"] = {}
if "last_chart_buf" not in st.session_state:    # 新增：存储最后一张图表
    st.session_state["last_chart_buf"] = None

# 语言切换
st.sidebar.header(LANG_CONFIG["en"]["lang_switch"])
selected_lang = st.sidebar.radio("", ["en", "zh"], format_func=lambda x: "English" if x == "en" else "中文")
lang = LANG_CONFIG[selected_lang]

st.set_page_config(page_title=lang["page_title"], layout="wide")
st.title(lang["main_title"])
st.markdown(lang["main_desc"])

# 展示支持的功能（新增ZIP功能）
st.subheader(lang["supported_features"])
features = [lang[f"feature_{i}"] for i in range(1, 10)]
for feat in features:
    st.markdown(f"✅ {feat}")

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

    # 高级数据清洗
    st.subheader(lang["advanced_data_cleaning"])

    if "original_df" not in st.session_state:
        st.session_state["original_df"] = df.copy()
    if "cleaned_df" not in st.session_state:
        st.session_state["cleaned_df"] = df.copy()

    if st.button(lang["reset_data"]):
        df = st.session_state["original_df"].copy()
        st.session_state["cleaned_df"] = df.copy()
        st.session_state["clean_log"] = []
        st.session_state["generated_charts"] = {}  # 重置图表记录
        st.session_state["last_chart_buf"] = None
        st.success(lang["reset_success"])

    # 缺失值处理
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

    # 重复值处理
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

    # 异常值处理
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_cols = [col for col in df.select_dtypes(include=['object', 'category']).columns.tolist() if not any(x in col.lower() for x in ['id','userid','user_id'])]
    outlier_strategy = lang["outlier_keep"]
    outlier_cols = []

    if numeric_cols:
        st.markdown(f"#### {lang['step3_outlier_title']}")
        outlier_strategy = st.selectbox(
            lang["outlier_strategy_label"],
            [lang["outlier_keep"], lang["outlier_drop"], lang["outlier_cap"]]
        )
        outlier_cols = st.multiselect(lang["outlier_cols_label"], numeric_cols, default=numeric_cols)

    # 执行清洗
    if st.button(lang["execute_clean"]):
        cleaned_df = st.session_state["original_df"].copy()
        clean_log = []

        # 处理缺失值
        if missing_strategy != lang["missing_keep"]:
            if missing_strategy == lang["missing_drop_rows"]:
                before = cleaned_df.shape[0]
                cleaned_df = cleaned_df.dropna()
                clean_log.append(f"删除含缺失值的行：{before - cleaned_df.shape[0]} 行")
            elif missing_strategy == lang["missing_drop_cols"]:
                before = cleaned_df.shape[1]
                cleaned_df = cleaned_df.dropna(axis=1)
                clean_log.append(f"删除含缺失值的列：{before - cleaned_df.shape[1]} 列")
            elif missing_strategy == lang["missing_fill_mean"]:
                for col in numeric_cols:
                    if cleaned_df[col].isnull().sum() > 0:
                        mean_val = cleaned_df[col].mean()
                        cleaned_df[col] = cleaned_df[col].fillna(mean_val)
                clean_log.append(f"数值列填充均值")
            elif missing_strategy == lang["missing_fill_median"]:
                for col in numeric_cols:
                    if cleaned_df[col].isnull().sum() > 0:
                        median_val = cleaned_df[col].median()
                        cleaned_df[col] = cleaned_df[col].fillna(median_val)
                clean_log.append(f"数值列填充中位数")
            elif missing_strategy == lang["missing_fill_mode"]:
                for col in categorical_cols:
                    if cleaned_df[col].isnull().sum() > 0:
                        mode_val = cleaned_df[col].mode()[0]
                        cleaned_df[col] = cleaned_df[col].fillna(mode_val)
                clean_log.append(f"分类列填充众数")
            elif missing_strategy == lang["missing_fill_custom"]:
                cleaned_df = cleaned_df.fillna(custom_fill_val)
                clean_log.append(f"自定义值填充缺失值：{custom_fill_val}")

        # 处理重复值
        if dup_strategy != lang["dup_keep"]:
            before = cleaned_df.shape[0]
            if dup_strategy == lang["dup_drop_all"]:
                cleaned_df = cleaned_df.drop_duplicates(keep=False)
            elif dup_strategy == lang["dup_keep_first"]:
                cleaned_df = cleaned_df.drop_duplicates(keep='first')
            elif dup_strategy == lang["dup_keep_last"]:
                cleaned_df = cleaned_df.drop_duplicates(keep='last')
            clean_log.append(f"处理重复行：删除 {before - cleaned_df.shape[0]} 行")

        # 处理异常值
        if outlier_strategy != lang["outlier_keep"] and outlier_cols:
            before = cleaned_df.shape[0]
            for col in outlier_cols:
                q1 = cleaned_df[col].quantile(0.25)
                q3 = cleaned_df[col].quantile(0.75)
                iqr = q3 - q1
                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr

                if outlier_strategy == lang["outlier_drop"]:
                    cleaned_df = cleaned_df[(cleaned_df[col] >= lower_bound) & (cleaned_df[col] <= upper_bound)]
                elif outlier_strategy == lang["outlier_cap"]:
                    cleaned_df[col] = np.where(cleaned_df[col] < lower_bound, lower_bound, cleaned_df[col])
                    cleaned_df[col] = np.where(cleaned_df[col] > upper_bound, upper_bound, cleaned_df[col])
            clean_log.append(f"处理异常值（{outlier_strategy}）：{before - cleaned_df.shape[0]} 行")

        st.session_state["cleaned_df"] = cleaned_df
        st.session_state["clean_log"] = clean_log
        st.success(lang["clean_success"])

    # 自动可视化
    st.subheader(lang["auto_viz"])
    cleaned_df = st.session_state["cleaned_df"]
    numeric_cols_clean = cleaned_df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_cols_clean = [col for col in cleaned_df.select_dtypes(include=['object', 'category']).columns.tolist() if not any(x in col.lower() for x in ['id','userid','user_id'])]

    if not numeric_cols_clean:
        st.warning(lang["no_numeric_cols"])
    else:
        # 直方图
        st.markdown(f"##### {lang['histogram_title']}")
        hist_col = st.selectbox(lang["histogram_select"], numeric_cols_clean, key="hist")
        fig_hist, ax_hist = plt.subplots(figsize=(10, 5))
        sns.histplot(cleaned_df[hist_col].dropna(), kde=True, ax=ax_hist)
        ax_hist.set_title(lang["dist_title"].format(col=hist_col))
        st.pyplot(fig_hist)
        # 保存直方图到session
        hist_buf = save_plot_to_bytes(fig_hist)
        st.session_state["last_chart_buf"] = hist_buf
        st.session_state["generated_charts"][f"直方图_{hist_col}"] = hist_buf

        # 柱状图
        if categorical_cols_clean:
            st.markdown(f"##### {lang['bar_chart_title']}")
            bar_cat = st.selectbox(lang["bar_cat_select"], categorical_cols_clean, key="bar_cat")
            bar_num = st.selectbox(lang["bar_num_select"], numeric_cols_clean, key="bar_num")
            bar_data = cleaned_df.groupby(bar_cat)[bar_num].mean().sort_values(ascending=False)
            fig_bar, ax_bar = plt.subplots(figsize=(10, 5))
            bar_data.plot(kind='bar', ax=ax_bar)
            ax_bar.set_title(f"{bar_cat} vs {bar_num}")
            ax_bar.set_xticklabels(ax_bar.get_xticklabels(), rotation=45, ha='right')
            st.pyplot(fig_bar)
            # 保存柱状图到session
            bar_buf = save_plot_to_bytes(fig_bar)
            st.session_state["last_chart_buf"] = bar_buf
            st.session_state["generated_charts"][f"柱状图_{bar_cat}_vs_{bar_num}"] = bar_buf

        # 热力图
        if len(numeric_cols_clean) >= 2:
            st.markdown(f"##### {lang['heatmap_title']}")
            fig_heat, ax_heat = plt.subplots(figsize=(10, 8))
            corr = cleaned_df[numeric_cols_clean].corr()
            sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax_heat)
            st.pyplot(fig_heat)
            # 保存热力图到session
            heat_buf = save_plot_to_bytes(fig_heat)
            st.session_state["last_chart_buf"] = heat_buf
            st.session_state["generated_charts"][f"热力图_相关性分析"] = heat_buf

        # 饼图
        if categorical_cols_clean:
            st.markdown(f"##### {lang['pie_bar_select']}")
            pie_col = st.selectbox(lang["pie_bar_select"], categorical_cols_clean, key="pie")
            pie_data = cleaned_df[pie_col].value_counts().head(10)  # 只展示前10个类别
            fig_pie, ax_pie = plt.subplots(figsize=(8, 8))
            pie_data.plot(kind='pie', autopct='%1.1f%%', ax=ax_pie)
            ax_pie.set_ylabel('')
            ax_pie.set_title(f"{pie_col} 分布")
            st.pyplot(fig_pie)
            # 保存饼图到session
            pie_buf = save_plot_to_bytes(fig_pie)
            st.session_state["last_chart_buf"] = pie_buf
            st.session_state["generated_charts"][f"饼图_{pie_col}"] = pie_buf

    # 关键指标
    st.subheader(lang["key_metrics"])
    if numeric_cols_clean:
        key_col = st.selectbox(lang["key_col_select"], numeric_cols_clean, key="key_metric")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric(lang["total_records"], cleaned_df.shape[0])
        c2.metric(lang["mean_val"], round(cleaned_df[key_col].mean(), 2))
        c3.metric(lang["max_val"], round(cleaned_df[key_col].max(), 2))
        c4.metric(lang["min_val"], round(cleaned_df[key_col].min(), 2))

    # 下载图表（新增ZIP打包功能）
    st.subheader(lang["download_charts"])
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"##### {lang['download_last_chart']}")
        if st.session_state["last_chart_buf"] is not None:
            st.download_button(
                label=lang["download_png"],
                data=st.session_state["last_chart_buf"],
                file_name=f"last_chart_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                mime="image/png"
            )
        else:
            st.info(lang["no_charts_to_download"])
    
    with col2:
        st.markdown(f"##### {lang['download_all_charts']}")
        if st.session_state["generated_charts"]:
            # 生成ZIP文件
            zip_buf = create_charts_zip(st.session_state["generated_charts"])
            # 生成下载文件名
            zip_filename = lang["zip_filename"].format(time=datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
            # 提供ZIP下载
            st.download_button(
                label=lang["download_zip"],
                data=zip_buf,
                file_name=zip_filename,
                mime="application/zip"
            )
            # 展示生成的图表列表
            st.markdown("**生成的图表列表：**")
            for chart_name in st.session_state["generated_charts"].keys():
                st.markdown(f"- {chart_name}")
        else:
            st.info(lang["no_charts_to_download"])

    # 下载清洗后的数据
    st.subheader(lang["download_cleaned_data"])
    if st.button(lang["Generate Cleaned Data File"]):
        # CSV下载
        csv_buf = StringIO()
        cleaned_df.to_csv(csv_buf, index=False)
        csv_buf.seek(0)
        st.download_button(
            label=lang["Download Cleaned CSV"],
            data=csv_buf,
            file_name=f"cleaned_data_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
        # Excel下载
        excel_buf = BytesIO()
        cleaned_df.to_excel(excel_buf, index=False, engine="openpyxl")
        excel_buf.seek(0)
        st.download_button(
            label=lang["Download Cleaned Excel"],
            data=excel_buf,
            file_name=f"cleaned_data_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    # 自动生成分析报告
    st.subheader(lang["auto_report"])
    if st.button(lang["generate_report"]):
        report = generate_analysis_report(
            st.session_state["original_df"],
            cleaned_df,
            st.session_state["clean_log"],
            numeric_cols_clean,
            categorical_cols_clean,
            lang
        )
        st.session_state["analysis_report"] = report
        st.markdown(report)
        
        # 下载报告
        st.markdown(f"##### {lang['report_download']}")
        # MD下载
        st.download_button(
            label=lang["download_md"],
            data=report,
            file_name=f"analysis_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown"
        )
        # HTML下载
        html_report = markdown.markdown(report)
        st.download_button(
            label=lang["download_html"],
            data=html_report,
            file_name=f"analysis_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
            mime="text/html"
        )

else:
    st.info(lang["initial_prompt"])