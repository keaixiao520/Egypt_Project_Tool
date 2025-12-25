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

# --- 初始化“购物篮” ---
# 这是解决报错的关键：如果篮子不存在，先建一个空篮子
if 'items' not in st.session_state:
    st.session_state.items = []

# --- 主界面 ---
st.title("🏗️ 埃及建材出海总成本计算器 (多商品版)")
st.markdown("专注解决中埃贸易中“算不准、清关贵、汇率乱”的痛点。")

# --- 输入区域 ---
with st.container(border=True):
    st.subheader("➕ 添加新商品到清单")
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    with col1:
        name = st.text_input("商品名称", value="预制钢结构", key="input_name")
    with col2:
        price = st.number_input("采购单价 (CNY)", min_value=0.0, value=1000.0, key="input_price")
    with col3:
        qty = st.number_input("数量", min_value=1, value=10, key="input_qty")
    with col4:
        vol = st.number_input("单件体积 (CBM)", min_value=0.0, value=0.100, format="%.3f", key="input_vol")
    
    c5, c6, c7 = st.columns([1, 1, 1])
    with c5:
        duty = st.number_input("埃及关税率 (%)", min_value=0, max_value=100, value=10, key="input_duty")
    with c6:
        freight = st.number_input("预估海运费 (USD/CBM)", value=120, key="input_freight")
    with c7:
        st.write("##")
        if st.button("🚀 点击添加到清单", use_container_width=True):
            new_item = {
                "商品": name,
                "单价(CNY)": price,
                "数量": qty,
                "体积(CBM)": vol * qty,
                "关税率": duty / 100,
                "海运费(USD)": (vol * qty) * freight
            }
            st.session_state.items.append(new_item)
            st.toast(f"✅ 已成功添加: {name}")

# --- 清单展示区域 ---
st.markdown("---")
st.subheader("📋 我的采购清单")

# 只有当篮子里有东西时，才运行计算逻辑和显示表格
if len(st.session_state.items) > 0:
    # 1. 转化为表格数据
    df = pd.DataFrame(st.session_state.items)
    
    # 2. 执行计算
    df["货值(USD)"] = (df["单价(CNY)"] * df["数量"]) / usd_cny
    df["CIF(USD)"] = df["货值(USD)"] + df["海运费(USD)"]
    df["CIF(EGP)"] = df["CIF(USD)"] * usd_egp
    df["埃及关税(EGP)"] = df["CIF(EGP)"] * df["关税率"]
    df["增值税14%(EGP)"] = (df["CIF(EGP)"] + df["埃及关税(EGP)"]) * 0.14
    df["总计成本(EGP)"] = df["CIF(EGP)"] + df["埃及关税(EGP)"] + df["增值税14%(EGP)"]
    
    # 3. 显示精美表格
    st.dataframe(df, use_container_width=True)

    # 4. 显示总计看板
    st.divider()
    t_egp, t_cny, t_vol = st.columns(3)
    total_egp = df["总计成本(EGP)"].sum()
    total_cny = (total_egp / usd_egp) * usd_cny
    t_egp.metric("整批总额 (EGP)", f"{total_egp:,.2f}")
    t_cny.metric("整批总额 (CNY)", f"{total_cny:,.2f}")
    t_vol.metric("总计体积 (CBM)", f"{df['体积(CBM)'].sum():,.2f}")

    if st.button("🗑️ 清空所有清单"):
        st.session_state.items = []
        st.rerun()
else:
    # 篮子为空时，显示一段友好的提示，而不是报错
    st.info("💡 目前清单是空的。请在上方输入商品信息并点击“🚀 点击添加到清单”按钮。")