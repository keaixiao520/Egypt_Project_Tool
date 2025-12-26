import streamlit as st
import pandas as pd

# 1. 页面基本配置
st.set_page_config(page_title="萧工项目精算Pro", page_icon="🏗️", layout="wide")

# --- 👨‍💻 编程知识点：变量初始化 ---
# 我们继续使用 'project_data_2025' 这个新名字，避开之前的脏数据。
# 就像在工地上重新圈了一块干净的地皮。
if 'project_data_2025' not in st.session_state:
    st.session_state['project_data_2025'] = []

# --- 侧边栏：控制台 ---
with st.sidebar:
    st.title("👨‍💻 萧工工作台")
    st.caption("Status: Production (正式版)")
    
    # 急救按钮：编程中常叫 "Hard Reset"
    if st.button("🔴 清空所有数据"):
        st.session_state['project_data_2025'] = []
        st.rerun()
        
    st.divider()
    st.info("💡 编程心得：\n数据结构的设计决定了软件的上限。")

# --- 主页面：PM 成本与利润精算看板 ---
st.header("📊 埃及项目全周期成本精算")

# 第一部分：全局财务基准
# 使用 container 把它框起来，视觉更整洁
with st.container(border=True):
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        # step=10000.0 表示每次按加号增加一万，方便操作
        total_budget = st.number_input("💰 项目总预算 (CNY)", value=1000000.0, step=10000.0)
    with col_a2:
        total_revenue = st.number_input("💎 合同总金额 (CNY)", value=1200000.0, step=10000.0)

st.divider()

# 第二部分：专业分项录入
st.subheader("🛠️ 专业分项成本录入")

# 使用 expander 收纳录入框，不占用主屏空间
with st.expander("➕ 点击展开：新增分项明细", expanded=True):
    col1, col2, col3 = st.columns([2, 2, 2])
    with col1:
        major = st.selectbox("选择专业", ["建筑工程", "钢结构", "机电工程", "装修工程", "现场临建", "国际物流", "其他"])
    with col2:
        mat_cost = st.number_input("材料费 (Mat.)", min_value=0.0, step=1000.0, key="mat")
    with col3:
        ins_cost = st.number_input("安装费 (Ins.)", min_value=0.0, step=1000.0, key="ins")

    # 提交按钮逻辑
    if st.button("🚀 录入成本"):
        subtotal = mat_cost + ins_cost
        if subtotal > 0:
            # --- 👨‍💻 编程知识点：字典 (Dictionary) ---
            # 我们把一条数据打包成一个字典，方便后续分析
            new_entry = {
                "专业": major,
                "材料费": mat_cost,
                "安装费": ins_cost,
                "小计": subtotal
            }
            # 追加到我们的“新仓库”里
            st.session_state['project_data_2025'].append(new_entry)
            st.success(f"✅ {major} 成本已录入")
        else:
            st.warning("金额不能为 0")

# --- 第三部分：数据可视化 (Data Visualization) ---
# 检查仓库里有没有货
data_source = st.session_state['project_data_2025']

if len(data_source) > 0:
    # --- 👨‍💻 编程知识点：Pandas ---
    # 列表(List)是给人看的，DataFrame是给电脑算的。
    # 把它转成 DataFrame，才能进行求和、绘图。
    df = pd.DataFrame(data_source)
    
    # 核心计算逻辑
    current_total_cost = df["小计"].sum()
    estimated_profit = total_revenue - current_total_cost
    # 防止除以0的报错
    profit_margin = (estimated_profit / total_revenue) * 100 if total_revenue != 0 else 0
    budget_remaining = total_budget - current_total_cost

    # 1. 财务指标看板 (KPI Dashboard)
    st.subheader("📈 财务透视")
    m1, m2, m3, m4 = st.columns(4)
    
    m1.metric("已发生成本", f"¥{current_total_cost:,.0f}", delta=f"预算剩余: {budget_remaining:,.0f}")
    m2.metric("合同总收入", f"¥{total_revenue:,.0f}")
    
    # 动态颜色逻辑：赚钱是正常色，亏钱显示红色(inverse)
    profit_color = "normal" if estimated_profit >= 0 else "inverse"
    m3.metric("预估利润", f"¥{estimated_profit:,.0f}", delta="盈利" if estimated_profit > 0 else "亏损", delta_color=profit_color)
    m4.metric("利润率", f"{profit_margin:.2f}%")

    st.divider()
    
    # 2. 详细清单表格
    st.subheader("📋 成本明细表")
    # use_container_width 让表格自动撑满屏幕
    st.dataframe(df, use_container_width=True)
    
else:
    st.info("👋 欢迎回来，萧工！目前清单为空，请在上方录入您的第一笔成本。")
