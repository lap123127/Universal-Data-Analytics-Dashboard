import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO, StringIO
import datetime
import markdown
import zipfile
import base64
import warnings
import requests
import json

# 屏蔽Matplotlib字体警告，适配云端部署
warnings.filterwarnings('ignore')
# 终极中文适配：自动检测系统字体 + 兜底方案
import matplotlib.font_manager as fm

# 手动指定字体文件（Windows绝对兼容）
try:
    # Windows系统优先用"微软雅黑"（几乎所有Windows都有）
    font_path = 'C:/Windows/Fonts/msyh.ttc'
    font_prop = fm.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()
except:
    # 其他系统兜底
    plt.rcParams['font.sans-serif'] = [
        'Microsoft YaHei',  # Windows 微软雅黑
        'SimHei',           # Windows 黑体
        'PingFang SC',      # Mac 苹方
        'WenQuanYi Micro Hei', # Linux
        'DejaVu Sans'       # 最后兜底
    ]
plt.rcParams['axes.unicode_minus'] = False  # 负号正常显示

# 你的API Key
API_KEY = "sk-13584a16dcf94b3fb0a982b4296df6e6"
LANG_CONFIG = {
    "en": {
        "page_title": "Universal Data Visualization Dashboard",
        "main_title": "📊 Universal Data Analysis Dashboard",
        "main_desc": "Upload your CSV/Excel file for automatic cleaning, visualization and AI analysis",
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
        "feature_8": "Automatic analysis report",
        "feature_9": "Download all charts as ZIP",
        "feature_10": "AI-powered analysis (300 words max)",
        "ai_disclaimer": "⚠️ Disclaimer: AI-generated content is for reference only.",
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
        "custom_fill_tip": "Enter custom value",
        "step2_dup_title": "Step 2: Handle Duplicate Rows",
        "dup_strategy_label": "Select strategy for duplicate rows",
        "dup_keep": "Keep as is",
        "dup_drop_all": "Drop all duplicates",
        "dup_keep_first": "Keep first duplicate",
        "dup_keep_last": "Keep last duplicate",
        "step3_outlier_title": "Step 3: Handle Outliers",
        "outlier_strategy_label": "Select strategy for outliers",
        "outlier_keep": "Keep as is",
        "outlier_drop": "Drop rows with outliers",
        "outlier_cap": "Cap outliers",
        "outlier_cols_label": "Select columns",
        "execute_clean": "Execute All Cleaning Steps",
        "clean_success": "All cleaning steps executed!",
        "auto_viz": "Automatic Visualization",
        "histogram_title": "Histogram",
        "histogram_select": "Select Numeric Column",
        "bar_chart_title": "Bar Chart",
        "bar_cat_select": "Select Category Column",
        "bar_num_select": "Select Numeric Column",
        "heatmap_title": "Correlation Heatmap",
        "pie_chart_title": "Pie Chart",
        "dist_title": "Distribution of {col}",
        "pie_bar_select": "Select Category Column",
        "key_metrics": "Key Metrics",
        "key_col_select": "Select Metric Column",
        "total_records": "Total Records",
        "mean_val": "Mean",
        "max_val": "Max",
        "min_val": "Min",
        "median_val": "Median",
        "download_charts": "Download Charts",
        "download_last_chart": "Download Last Chart",
        "download_png": "Download PNG",
        "download_all_charts": "Download All Charts (ZIP)",
        "no_charts_to_download": "No charts yet.",
        "zip_filename": "charts_{time}.zip",
        "download_zip": "Download ZIP",
        "download_cleaned_data": "Download Cleaned Data",
        "download_cleaned_csv": "Download CSV",
        "download_cleaned_excel": "Download Excel",
        "auto_report": "Automatic Report",
        "generate_report": "Generate Report",
        "ai_report": "AI Analysis (300 words max)",
        "generate_ai_report": "🚀 Start AI Analysis",
        "ai_report_loading": "Generating AI report...",
        "ai_report_error": "Failed: {e}",
        "report_download": "Download Report",
        "download_md": "Download MD",
        "download_html": "Download HTML",
        "report_title": "Analysis Report",
        "report_generated": "Generated at: {time}",
        "no_numeric_cols": "No numeric columns found!",
        "no_categorical_cols": "No categorical columns found!"
    },
    "zh": {
        "page_title": "通用数据可视化分析仪表盘",
        "main_title": "📊 通用数据可视化分析仪表盘",
        "main_desc": "上传CSV/Excel文件，自动完成数据清洗、可视化与AI分析",
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
        "feature_8": "自动生成分析报告",
        "feature_9": "一键下载所有图表为ZIP",
        "feature_10": "AI 智能数据分析（300字内）",
        "ai_disclaimer": "⚠️ 免责声明：AI 生成内容仅供参考，本工具不承担任何责任。",
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
        "custom_fill_tip": "输入自定义数值",
        "step2_dup_title": "步骤2：处理重复行",
        "dup_strategy_label": "选择重复行处理策略",
        "dup_keep": "保持不变",
        "dup_drop_all": "删除全部重复行",
        "dup_keep_first": "保留第一条重复数据",
        "dup_keep_last": "保留最后一条重复数据",
        "step3_outlier_title": "步骤3：处理异常值",
        "outlier_strategy_label": "选择异常值处理策略",
        "outlier_keep": "保持不变",
        "outlier_drop": "删除含异常值的行",
        "outlier_cap": "截断异常值",
        "outlier_cols_label": "选择处理列",
        "execute_clean": "执行全部清洗步骤",
        "clean_success": "所有清洗步骤已完成！",
        "auto_viz": "自动可视化",
        "histogram_title": "直方图",
        "histogram_select": "选择数值列",
        "bar_chart_title": "柱状图",
        "bar_cat_select": "选择分类列",
        "bar_num_select": "选择数值列",
        "heatmap_title": "相关性热力图",
        "pie_chart_title": "饼图",
        "dist_title": "{col} 分布情况",
        "pie_bar_select": "选择分类列",
        "key_metrics": "关键指标",
        "key_col_select": "选择指标列",
        "total_records": "总记录数",
        "mean_val": "平均值",
        "max_val": "最大值",
        "min_val": "最小值",
        "median_val": "中位数",
        "download_charts": "下载图表",
        "download_last_chart": "下载最后一张图表",
        "download_png": "下载PNG",
        "download_all_charts": "下载所有图表（ZIP）",
        "no_charts_to_download": "暂无生成图表。",
        "zip_filename": "图表_{time}.zip",
        "download_zip": "下载ZIP",
        "download_cleaned_data": "下载清洗后数据",
        "download_cleaned_csv": "下载CSV",
        "download_cleaned_excel": "下载Excel",
        "auto_report": "自动分析报告",
        "generate_report": "生成报告",
        "ai_report": "AI 分析报告（300字内）",
        "generate_ai_report": "🚀 启动 AI 分析",
        "ai_report_loading": "正在生成 AI 报告...",
        "ai_report_error": "生成失败：{e}",
        "report_download": "下载报告",
        "download_md": "下载MD报告",
        "download_html": "下载HTML报告",
        "report_title": "数据分析报告",
        "report_generated": "报告生成时间：{time}",
        "no_numeric_cols": "未找到数值列！",
        "no_categorical_cols": "未找到分类列！"
    }
}
# 过滤无用ID列：user_id/id/编号/序号
def get_valid_columns(df):
    exclude_keywords = ["id", "userid", "user_id", "uuid", "no", "num", "number", "index", "编号", "序号"]
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    valid_num_cols = [col for col in numeric_cols if not any(k in str(col).lower() for k in exclude_keywords)]
    valid_cat_cols = [col for col in cat_cols if not any(k in str(col).lower() for k in exclude_keywords)]
    return valid_num_cols, valid_cat_cols

# AI调用函数
def call_qwen_ai(data_summary, lang="zh"):
    url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
    if lang == "zh":
        prompt = f"""你是数据分析师，根据以下数据生成**300字以内**精简分析报告：
1.数据概况 2.核心指标 3.关键发现 4.简短建议
数据：{data_summary}"""
    else:
        prompt = f"""As data analyst, write a report within 300 words:
1.Overview 2.Metrics 3.Insights 4.Suggestions
Data: {data_summary}"""
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {"model": "qwen3.6-flash", "messages": [{"role": "user", "content": prompt}], "temperature": 0.7, "max_tokens": 450}
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=25)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        raise Exception(str(e))

# 保存图表
def save_plot_to_bytes(fig, dpi=150):
    buf = BytesIO()
    fig.savefig(buf, format='png', dpi=dpi, bbox_inches='tight')
    buf.seek(0)
    return buf

# 打包图表为ZIP
def create_charts_zip(charts_dict):
    zip_buf = BytesIO()
    with zipfile.ZipFile(zip_buf, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for name, buf in charts_dict.items():
            safe_name = name.replace('/', '_').replace('\\', '_').replace(':', '_')
            zipf.writestr(f"{safe_name}.png", buf.getvalue())
    zip_buf.seek(0)
    return zip_buf

# 生成基础文本报告
def generate_analysis_report(df, cleaned_df, clean_log, num_cols, cat_cols, lang):
    t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rep = [f"# {lang['report_title']}", f"*{lang['report_generated'].format(time=t)}*"]
    rep.append(f"- 原始行数：{df.shape[0]} → 清洗后：{cleaned_df.shape[0]}")
    rep.append(f"- 总列数：{df.shape[1]}")
    rep.append(f"- 缺失值：{df.isnull().sum().sum()}")
    rep.append(f"- 重复行：{df.duplicated().sum()}")
    return "\n".join(rep)

# 异常值处理
def handle_outliers(df, cols, strategy):
    cdf = df.copy()
    for col in cols:
        if col not in cdf.select_dtypes(include=[np.number]).columns:
            continue
        q1, q3 = cdf[col].quantile([0.25, 0.75])
        iqr = q3 - q1
        if strategy == "drop":
            cdf = cdf[(cdf[col] >= q1-1.5*iqr) & (cdf[col] <= q3+1.5*iqr)]
        elif strategy == "cap":
            cdf[col] = np.clip(cdf[col], q1-1.5*iqr, q3+1.5*iqr)
    return cdf
def main():
    st.set_page_config(page_title="Dashboard", layout="wide")
    
    # 初始化会话状态
    if "original_df" not in st.session_state: st.session_state["original_df"] = None
    if "cleaned_df" not in st.session_state: st.session_state["cleaned_df"] = None
    if "clean_log" not in st.session_state: st.session_state["clean_log"] = []
    if "analysis_report" not in st.session_state: st.session_state["analysis_report"] = ""
    if "ai_analysis_report" not in st.session_state: st.session_state["ai_analysis_report"] = ""
    if "generated_charts" not in st.session_state: st.session_state["generated_charts"] = {}
    if "last_chart_buf" not in st.session_state: st.session_state["last_chart_buf"] = None

    # 语言选择
    st.sidebar.header("🌐 Language")
    sel_lang = st.sidebar.radio("", ["zh", "en"], format_func=lambda x: "中文" if x == "zh" else "English", key="lang_radio")
    lang = LANG_CONFIG[sel_lang]

    st.title(lang["main_title"])
    st.markdown(lang["main_desc"])

    # 功能列表
    st.subheader(lang["supported_features"])
    for i in range(1, 11):
        st.markdown(f"✅ {lang[f'feature_{i}']}")

    # 文件上传
    st.sidebar.header(lang["sidebar_upload"])
    file = st.sidebar.file_uploader(lang["upload_label"], type=["csv", "xlsx"], key="file_uploader")
    if not file:
        st.info(lang["initial_prompt"])
        return

    # 读取文件
    try:
        if file.name.endswith(".csv"):
            # 优先GBK（Windows中文文件默认编码），失败再试UTF-8
            try:
                df = pd.read_csv(file, encoding='gbk')
            except UnicodeDecodeError:
                df = pd.read_csv(file, encoding='utf-8')
        else:
            # Excel文件指定engine，避免编码问题
            df = pd.read_excel(file, engine='openpyxl')
        st.session_state["original_df"] = df.copy()
        st.session_state["cleaned_df"] = df.copy()
        st.sidebar.success(lang["upload_success"])
    except Exception as e:
        st.error(lang["upload_error"].format(e=e))
        return

    # 过滤ID列
    num_cols, cat_cols = get_valid_columns(st.session_state["cleaned_df"])

    # 基础筛选
    st.sidebar.subheader(lang["basic_filters"])
    if cat_cols:
        sc = st.sidebar.selectbox(lang["filter_cat_col"], cat_cols, key="filter_cat")
        vs = st.sidebar.multiselect(lang["filter_keep_vals"], st.session_state["cleaned_df"][sc].unique(), default=list(st.session_state["cleaned_df"][sc].unique()), key="filter_vals")
        st.session_state["cleaned_df"] = st.session_state["cleaned_df"][st.session_state["cleaned_df"][sc].isin(vs)]

    # 数据预览
    st.subheader(lang["data_preview"])
    st.dataframe(st.session_state["cleaned_df"].head(8), use_container_width=True)

    # 数据概览
    st.subheader(lang["data_overview"])
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(lang["total_rows"], st.session_state["cleaned_df"].shape[0])
    c2.metric(lang["total_cols"], st.session_state["cleaned_df"].shape[1])
    c3.metric(lang["missing_vals"], st.session_state["cleaned_df"].isnull().sum().sum())
    c4.metric(lang["duplicate_rows"], st.session_state["cleaned_df"].duplicated().sum())

    # 数据清洗模块
    st.subheader(lang["advanced_data_cleaning"])
    if st.button(lang["reset_data"], key="reset_btn"):
        st.session_state["cleaned_df"] = st.session_state["original_df"].copy()
        st.session_state["clean_log"] = []
        st.success(lang["reset_success"])

    st.markdown(f"### {lang['step1_missing_title']}")
    m_strat = st.selectbox(lang["missing_strategy_label"], [
        lang["missing_keep"], lang["missing_drop_rows"], lang["missing_drop_cols"],
        lang["missing_fill_mean"], lang["missing_fill_median"], lang["missing_fill_mode"], lang["missing_fill_custom"]
    ], key="missing_strat")
    custom_val = st.text_input(lang["custom_fill_tip"], key="custom_fill") if m_strat == lang["missing_fill_custom"] else None

    st.markdown(f"### {lang['step2_dup_title']}")
    d_strat = st.selectbox(lang["dup_strategy_label"], [
        lang["dup_keep"], lang["dup_drop_all"], lang["dup_keep_first"], lang["dup_keep_last"]
    ], key="dup_strat")

    st.markdown(f"### {lang['step3_outlier_title']}")
    o_strat = st.selectbox(lang["outlier_strategy_label"], [
        lang["outlier_keep"], lang["outlier_drop"], lang["outlier_cap"]
    ], key="outlier_strat")
    o_cols = st.multiselect(lang["outlier_cols_label"], num_cols, default=num_cols, key="outlier_cols") if num_cols else []

    if st.button(lang["execute_clean"], key="clean_btn"):
        log = []
        if m_strat != lang["missing_keep"]: log.append(f"缺失值：{m_strat}")
        if d_strat != lang["dup_keep"]: log.append(f"重复行：{d_strat}")
        if o_strat != lang["outlier_keep"] and o_cols: log.append(f"异常值：{o_strat}")
        st.session_state["clean_log"] = log
        st.success(lang["clean_success"])

    # 可视化模块（修复热力图+饼图）
    st.subheader(lang["auto_viz"])
    t1, t2, t3, t4 = st.tabs([lang["histogram_title"], lang["bar_chart_title"], lang["heatmap_title"], lang["pie_chart_title"]])

    with t1:
        if num_cols:
            col = st.selectbox(lang["histogram_select"], num_cols, key="hist_unique")
            fig, ax = plt.subplots(figsize=(10,5))
            sns.histplot(st.session_state["cleaned_df"][col], kde=True, ax=ax)
            # 显式指定字体 + 调整标签
            ax.set_title(lang["dist_title"].format(col=col), fontproperties='Microsoft YaHei', fontsize=12)
            ax.set_xlabel(col, fontproperties='Microsoft YaHei', fontsize=11)
            ax.set_ylabel("频数" if sel_lang == "zh" else "Frequency", fontproperties='Microsoft YaHei', fontsize=11)
            # 坐标轴刻度也指定字体
            for label in ax.get_xticklabels() + ax.get_yticklabels():
                label.set_fontproperties('Microsoft YaHei')
            plt.tight_layout()
            st.pyplot(fig)
            st.session_state["last_chart_buf"] = save_plot_to_bytes(fig)
        else:
            st.warning(lang["no_numeric_cols"])

    with t2:
        if cat_cols and num_cols:
            bc = st.selectbox(lang["bar_cat_select"], cat_cols, key="bar_cat_unique")
            bn = st.selectbox(lang["bar_num_select"], num_cols, key="bar_num_unique")
            fig, ax = plt.subplots(figsize=(10,5))
            sns.barplot(x=st.session_state["cleaned_df"][bc], y=st.session_state["cleaned_df"][bn], ax=ax)
            plt.xticks(rotation=45, fontproperties='Microsoft YaHei', fontsize=10)
            ax.set_xlabel(bc, fontproperties='Microsoft YaHei', fontsize=11)
            ax.set_ylabel(bn, fontproperties='Microsoft YaHei', fontsize=11)
            # 坐标轴刻度指定字体
            for label in ax.get_yticklabels():
                label.set_fontproperties('Microsoft YaHei')
            plt.tight_layout()
            st.pyplot(fig)
            st.session_state["last_chart_buf"] = save_plot_to_bytes(fig)
        else:
            st.warning(lang["no_categorical_cols"] if not cat_cols else lang["no_numeric_cols"])

    with t3:
        if len(num_cols)>=2:
            fig, ax = plt.subplots(figsize=(10,6))
            corr = st.session_state["cleaned_df"][num_cols].corr()
            sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax, fmt=".2f")
            ax.set_title(lang["heatmap_title"], fontproperties='Microsoft YaHei', fontsize=12)
            # 刻度标签指定字体
            for label in ax.get_xticklabels() + ax.get_yticklabels():
                label.set_fontproperties('Microsoft YaHei')
            plt.tight_layout()
            st.pyplot(fig)
            st.session_state["last_chart_buf"] = save_plot_to_bytes(fig)
        else:
            st.warning(lang["no_numeric_cols"])

    with t4:
        if cat_cols:
            pc = st.selectbox(lang["pie_bar_select"], cat_cols, key="pie_unique")
            cnt = st.session_state["cleaned_df"][pc].value_counts()
            fig, ax = plt.subplots(figsize=(8,8))
            ax.pie(cnt, labels=cnt.index, autopct="%1.1f%%")
            ax.set_title(lang["pie_chart_title"], fontproperties='Microsoft YaHei', fontsize=12)
            # 饼图标签指定字体
            for text in ax.texts:
                text.set_fontproperties('Microsoft YaHei')
            plt.tight_layout()
            st.pyplot(fig)
            st.session_state["last_chart_buf"] = save_plot_to_bytes(fig)
        else:
            st.warning(lang["no_categorical_cols"])

    # 下载图表
    st.subheader(lang["download_charts"])
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state["last_chart_buf"]:
            st.download_button(lang["download_png"], st.session_state["last_chart_buf"], "chart.png", "image/png", key="dl_png")
    with col2:
        if st.session_state["generated_charts"]:
            z = create_charts_zip(st.session_state["generated_charts"])
            st.download_button(lang["download_zip"], z, lang["zip_filename"].format(time=datetime.datetime.now().strftime("%Y%m%d%H%M%S")), "application/zip", key="dl_zip")

    # 关键指标
    st.subheader(lang["key_metrics"])
    if num_cols:
        kc = st.selectbox(lang["key_col_select"], num_cols, key="metric_unique")
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric(lang["total_records"], st.session_state["cleaned_df"][kc].count())
        c2.metric(lang["mean_val"], round(st.session_state["cleaned_df"][kc].mean(),2))
        c3.metric(lang["max_val"], round(st.session_state["cleaned_df"][kc].max(),2))
        c4.metric(lang["min_val"], round(st.session_state["cleaned_df"][kc].min(),2))
        c5.metric(lang["median_val"], round(st.session_state["cleaned_df"][kc].median(),2))

    # 自动报告
    st.subheader(lang["auto_report"])
    if st.button(lang["generate_report"], key="gen_report"):
        r = generate_analysis_report(st.session_state["original_df"], st.session_state["cleaned_df"], st.session_state["clean_log"], num_cols, cat_cols, lang)
        st.session_state["analysis_report"] = r
        st.markdown(r)

    # AI 分析（改为独立启动按钮，无勾选框）
    st.divider()
    st.subheader(lang["ai_report"])
    st.warning(lang["ai_disclaimer"])

    if st.button(lang["generate_ai_report"], type="primary", key="gen_ai"):
        with st.spinner(lang["ai_report_loading"]):
            try:
                summary = f"行数：{st.session_state['cleaned_df'].shape[0]}，列数：{st.session_state['cleaned_df'].shape[1]}，有效数值列：{num_cols}，分类列：{cat_cols}"
                ai_report = call_qwen_ai(summary, sel_lang)
                st.session_state["ai_analysis_report"] = ai_report
                st.markdown("---")
                st.markdown(ai_report)
            except Exception as e:
                st.error(lang["ai_report_error"].format(e=str(e)))

    # 下载AI报告
    if st.session_state["ai_analysis_report"]:
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(lang["download_md"], st.session_state["ai_analysis_report"], "ai_report.md", key="dl_md")
        with col2:
            html = markdown.markdown(st.session_state["ai_analysis_report"])
            st.download_button(lang["download_html"], html, "ai_report.html", key="dl_html")

if __name__ == "__main__":
    main()