import streamlit as st
import pandas as pd

st.set_page_config(page_title="中埃贸易成本管家", page_icon="🏗️", layout="wide")

# --- 侧边栏：配置与联系方式 ---
st.sidebar.header("⚙️ 全局汇率配置")
usd_cny = st.sidebar.number_input("汇率: 1 USD = ? CNY", value=7.25)
usd_egp = st.sidebar.number_input("汇率: 1 USD = ? EGP", value=48.50)

st.sidebar.markdown("---")
st.sidebar.header("👤 商务咨询 / 合作")
st.sidebar.info("10年埃及一线建筑师经验，为您提供：\n- 埃及清关、海运实战建议\n- 当地建材市场准入调研\n- 中埃跨境贸易撮合")
st.sidebar.write("💬 **微信号**: [此处填你的微信号]")
st.sidebar.write("📧 **邮箱**: [此处填你的邮箱]")
if st.sidebar.button("预约 1对1 深度咨询"):
    st.sidebar.success("请通过上述方式联系，我会第一时间回复！")

# --- 主界面 ---
st.title("🏗️ 埃及建材出海总成本计算器 (多商品版)")
st.markdown("专注解决中埃贸易中“算不准、清关贵、汇率乱”的痛点。")

# --- 初始化商品清单 ---
if 'items' not in st.session_state:
    st.session_state.items = []

# --- 输入区域 ---
with st.expander("➕ 添加新商品到清单", expanded=True):
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    with col1:
        name = st.text_input("商品名称", value="预制钢结构")
    with col2:
        price = st.number_input("采购单价 (CNY)", min_value=0.0, value=1000.0)
    with col3:
        qty = st.number_input("数量", min_value=1, value=10)
    with col4:
        vol = st.number_input("单件体积 (CBM)", min_value=0.0, value=0.1, format="%.3f")
    
    c5, c6, c7 = st.columns([1, 1, 1])
    with c5:
        duty = st.number_input("埃及关税率 (%)", min_value=0, max_value=100, value=10)
    with c6:
        freight = st.number_input("预估海运费 (USD/CBM)", value=120)
    with c7:
        st.write("##")
        if st.button("添加到清单"):
            new_item = {
                "商品": name,
                "单价(CNY)": price,
                "数量": qty,
                "体积(CBM)": vol * qty,
                "关税率": duty / 100,
                "海运费(USD)": (vol * qty) * freight
            }
            st.session_state.items.append(new_item)
            st.success(f"已添加 {name}")

# --- 清单展示 ---
if st.session_state.items:
    st.subheader("📋 当前采购清单")
    df = pd.DataFrame(st.session_state.items)
    
    # 计算各项税费
    df["货值(USD)"] = (df["单价(CNY)"] * df["数量"]) / usd_cny
    df["CIF(USD)"] = df["货值(USD)"] + df["海运费(USD)"]
    df["CIF(EGP)"] = df["CIF(USD)"] * usd_egp
    df["埃及关税(EGP)"] = df["CIF(EGP)"] * df["关税率"]
    df["增值税14%(EGP)"] = (df["CIF(EGP)"] + df["埃及关税(EGP)"]) * 0.14
    df["总计成本(EGP)"] = df["CIF(EGP)"] + df["埃及关税(EGP)"] + df["增值税14%(EGP)"]
    
    st.dataframe(df.style.format(precision=2), use_container_width=True)

    if st.button("清空清单"):
        st.session_state.items = []
        st.rerun()

    # --- 总计看板 ---
    st.divider()
    st.header("💰 项目总预算预估")
    total_egp = df["总计成本(EGP)"].sum()
    total_cny = (total_egp / usd_egp) * usd_cny
    
    k1, k2, k3 = st.columns(3)
    k1.metric("整批货物总成本 (EGP)", f"{total_egp:,.2f}")
    k2.metric("约合人民币总额 (CNY)", f"{total_cny:,.2f}")
    k3.metric("总计体积 (CBM)", f"{df['体积(CBM)'].sum():,.2f}")

else:
    st.info("清单为空，请在上方添加商品。")

st.markdown("---")
st.caption("注：本工具仅供概算参考。埃及清关受ACI系统、反倾销税、进出口资质等多种因素影响，实际请以具体报关单为准。")