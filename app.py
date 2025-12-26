import streamlit as st
import pandas as pd

# 1. 页面基本配置
st.set_page_config(page_title="萧工在开罗-项目经理精算器", page_icon="📊", layout="wide")

# --- 侧边栏 ---
with st.sidebar:
    st.title("👨‍💻 萧工项目实验室")
    st.info("驻埃及10年建筑师 | PM 数字化转型")
    # 添加一个手动重置按钮，方便以后急救
    if st.button("⚠️ 强制重置系统数据"):
        st.session_state.items = []
        st.rerun()
    st.divider()
    st.write("🔗 公众号：萧工在开罗")

# 2. 核心：安全初始化 (带防错机制)
if 'items' not in st.session_state:
    st.session_state.items = []

# 确保 items 必须是列表，如果不是（比如旧缓存导致的），强制重置
if not isinstance(st.session_state.items, list):
    st.session_state.items = []

# --- 主页面：PM 成本与利润精算看板 ---
st.header("📊 项目全周期成本与利润精算 (PM版)")

# 第一部分：全局财务基准设置
with st.container(border=True):
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        total_budget = st.number_input("项目总预算 (CNY)", min_value=0.0, value=1000000.0, step=10000.0)
    with col_a2:
        total_revenue = st.number_input("合同总金额/预估收益 (CNY)", min_value=0.0, value=1200000.0, step=10000.0)

st.divider()

# 第二部分：专业分项录入
st.subheader("🛠️ 专业分项成本录入")
with st.expander("点击展开：新增分项明细", expanded=True):
    col1, col2, col3 = st.columns([2, 2, 2])
    with col1:
        major = st.selectbox("选择专业", ["建筑工程", "钢结构", "机电工程", "装修工程", "现场临建", "其他"])
    with col2:
        mat_cost = st.number_input("材料费 (CNY)", min_value=0.0, value=0.0, key="mat")
    with col3:
        ins_cost = st.number_input("安装/人工费 (CNY)", min_value=0.0, value=0.0, key="ins")

    if st.button("🚀 录入当前专业成本"):
        subtotal = mat_cost + ins_cost
        if subtotal > 0:
            new_entry = {
                "专业": major,
                "材料费": mat_cost,
                "安装费": ins_cost,
                "小计": subtotal
            }
            st.session_state.items.append(new_entry)
            st.success(f"✅ {major} 成本已录入")
        else:
            st.warning("金额不能为 0，请检查录入。")

# 第三部分：看板与明细展示 (这里加了“防崩卫士”)
if st.session_state.items:
    try:
        # 尝试生成表格
        df = pd.DataFrame(st.session_state.items)
        
        # 核心计算逻辑
        total_cost = df["小计"].sum()
        total_profit = total_revenue - total_cost
        profit_margin = (total_profit / total_revenue) * 100 if total_revenue != 0 else 0
        budget_remaining = total_budget - total_cost

        # 4. KPI 视觉指标
        st.subheader("📈 项目财务指标看板")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("已发生成本 (Cost)", f"¥{total_cost:,.2f}", delta=f"预算剩余: ¥{budget_remaining:,.0f}")
        m2.metric("合同收益 (Revenue)", f"¥{total_revenue:,.2f}")
        
        profit_color = "normal" if total_profit >= 0 else "inverse"
        m3.metric("预估利润 (Profit)", f"¥{total_profit:,.2f}", delta="盈利" if total_profit >= 0 else "亏损", delta_color=profit_color)
        m4.metric("利润率", f"{profit_margin:.2f}%")

        st.divider()
        
        # 5. 明细表
        st.subheader("📋 成本明细清单")
        st.dataframe(df, use_container_width=True)
        
        if st.button("🗑️ 清空所有数据"):
            st.session_state.items = []
            st.rerun()

    except Exception as e:
        # 🚨 防崩卫士触发：如果报错，自动自我修复
        st.warning("检测到数据格式异常（可能是旧版本缓存），正在自动修复...")
        st.session_state.items = [] # 强制清空坏数据
        st.rerun() # 自动刷新页面
else:
    st.info("💡 尚未录入数据。请在上方选择专业并填入材料/安装费。")
