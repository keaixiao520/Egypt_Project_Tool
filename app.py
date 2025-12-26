import streamlit as st
import pandas as pd

# 1. 页面配置
st.set_page_config(page_title="萧工成本精算Pro", page_icon="🏗️", layout="wide")

# --- 编程自学小贴士 ---
# 之前报错是因为 st.session_state.items 里存了脏数据。
# 今天我们改用 'project_data_2025' 这个新名字，系统就会自动创建一个全新的列表。
# --------------------

# 2. 初始化新仓库 (注意名字变了)
if 'project_data_2025' not in st.session_state:
    st.session_state['project_data_2025'] = []

# --- 侧边栏 ---
with st.sidebar:
    st.header("🏗️ 萧工工作台")
    st.success("✅ 系统状态：全新纯净版")
    
    # 强制清空按钮
    if st.button("🗑️ 删库跑路 (清空数据)"):
        st.session_state['project_data_2025'] = []
        st.rerun()

# --- 主界面 ---
st.title("📊 埃及项目成本精算 (Dev版)")

# 输入区
with st.container(border=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        name = st.text_input("分项名称", "钢结构主体")
    with col2:
        cost = st.number_input("成本 (CNY)", value=0.0, step=1000.0)
    with col3:
        revenue = st.number_input("报价 (CNY)", value=0.0, step=1000.0)

    if st.button("📥 写入数据库"):
        if cost > 0 or revenue > 0:
            # 写入新仓库
            new_row = {"分项": name, "成本": cost, "报价": revenue, "利润": revenue - cost}
            st.session_state['project_data_2025'].append(new_row)
            st.toast(f"已录入: {name}")
        else:
            st.warning("金额不能全为0")

# --- 数据展示区 (核心防报错逻辑) ---
# 检查新仓库是否非空
data_source = st.session_state['project_data_2025']

if len(data_source) > 0:
    # 转换为 DataFrame
    df = pd.DataFrame(data_source)
    
    # 计算总和
    total_cost = df["成本"].sum()
    total_profit = df["利润"].sum()
    
    # 展示看板
    k1, k2 = st.columns(2)
    k1.metric("总成本", f"¥{total_cost:,.0f}")
    k2.metric("总利润", f"¥{total_profit:,.0f}")
    
    # 展示表格
    st.dataframe(df, use_container_width=True)
else:
    st.info("👋 欢迎来到新系统，目前数据库为空，请在上方录入数据。")
