import streamlit as st

st.set_page_config(page_title="中埃贸易成本助手", page_icon="🏗️")

st.title("🏗️ 埃及建材到港成本 AI 计算器")
st.caption("由 AI 驱动的建筑师出海工具 v1.0")

# 侧边栏：核心汇率
st.sidebar.header("实时汇率配置")
usd_cny = st.sidebar.number_input("1 USD 等于多少 CNY", value=7.25)
usd_egp = st.sidebar.number_input("1 USD 等于多少 EGP (参考)", value=48.50)

# 第一部分：产品选择
st.subheader("1. 产品与物流信息")
col1, col2 = st.columns(2)

with col1:
    category = st.selectbox("选择建材类别 (自动匹配HS Code参考)", 
                           ["预制钢结构 (HS 7308)", "建筑陶瓷 (HS 6907)", "铝合金门窗 (HS 7610)", "LED照明 (HS 9405)", "其他"])
    unit_price_cny = st.number_input("国内采购单价 (CNY)", value=100.0)

with col2:
    quantity = st.number_input("采购总数量", value=1000, step=10)
    volume_per_unit = st.number_input("单件体积 (CBM)", value=0.05, format="%.3f")

# 第二部分：税费预估
st.subheader("2. 埃及关税预估")
# 根据选择自动给一个建议关税
suggested_duty = 0.10
if "陶瓷" in category: suggested_duty = 0.40
elif "铝合金" in category: suggested_duty = 0.20

duty_rate = st.slider("设定埃及关税率 (%)", 0, 60, int(suggested_duty*100)) / 100
freight_usd_cbm = st.number_input("海运费预估 (USD/CBM)", value=120)

# 计算逻辑
total_fob_usd = (unit_price_cny * quantity) / usd_cny
total_freight_usd = (volume_per_unit * quantity) * freight_usd_cbm
cif_usd = total_fob_usd + total_freight_usd
cif_egp = cif_usd * usd_egp

duty_egp = cif_egp * duty_rate
vat_egp = (cif_egp + duty_egp) * 0.14  # 埃及14%增值税
total_cost_egp = cif_egp + duty_egp + vat_egp
unit_cost_egp = total_cost_egp / quantity

# 结果展示
st.divider()
st.header("📊 成本分析结果")
c1, c2 = st.columns(2)
with c1:
    st.metric("埃及到港单价 (EGP)", f"{unit_cost_egp:,.2f}")
with c2:
    st.metric("约合人民币 (CNY)", f"{(unit_cost_egp/usd_egp)*usd_cny:,.2f}")

st.warning(f"注：此成本包含 CIF 价 + {duty_rate*100:.0f}% 关税 + 14% 增值税。不含当地清关小费及陆运。")