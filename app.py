import streamlit as st
import pandas as pd

# 1. 页面基本配置
st.set_page_config(page_title="中埃贸易成本管家", layout="wide")

# 2. 彻底初始化“篮子” (增加强制类型检查)
if 'items' not in st.session_state or not isinstance(st.session_state.items, list):
    st.session_state.items = []

# --- 侧边栏 ---
st.sidebar.header("⚙️ 汇率配置")
usd_cny = st.sidebar.number_input("1 USD = ? CNY", value=7.25)
usd_egp = st.sidebar.number_input("1 USD = ? EGP", value=48.50)
st.sidebar.markdown("---")
st.sidebar.write("👤 **商务咨询**")
st.sidebar.write("微信: [填你的微信号]")

# --- 主界面 ---
st.title("🏗️ 埃及建材出海总成本计算器")

# --- 输入区 (用 Form 包装，这是最稳妥的防崩溃方法) ---
with st.form("my_form", clear_on_submit=True):
    st.subheader("➕ 添加商品")
    c1, c2, c3, c4 = st.columns(4)
    with c1: name = st.text_input("商品名称", value="预制钢结构")
    with c2: price = st.number_input("单价(CNY)", value=1000.0)
    with c3: qty = st.number_input("数量", value=10, step=1)
    with c4: vol = st.number_input("单件体积(CBM)", value=0.1, format="%.3f")
    
    c5, c6 = st.columns(2)
    with c5: duty = st.number_input("埃及关税率(%)", value=10)
    with c6: freight = st.number_input("海运费(USD/CBM)", value=120)
    
    submit = st.form_submit_button("🚀 确认添加到清单")
    
    if submit:
        # 点击提交时，才把数据塞进篮子
        new_item = {
            "商品": name,
            "单价": price,
            "数量": qty,
            "体积": vol * qty,
            "关税率": duty / 100,
            "运费": (vol * qty) * freight
        }
        st.session_state.items.append(new_item)
        st.toast("添加成功！")

# --- 显示区 ---
st.markdown("---")
st.subheader("📋 我的采购清单")

# 只有篮子不为空，才展示
if st.session_state.items:
    # 转换为表格
    df_raw = pd.DataFrame(st.session_state.items)
    
    # 执行计算逻辑
    df_raw["货值(USD)"] = (df_raw["单价"] * df_raw["数量"]) / usd_cny
    df_raw["CIF(USD)"] = df_raw["货值(USD)"] + df_raw["运费"]
    df_raw["埃及关税(EGP)"] = (df_raw["CIF(USD)"] * usd_egp) * df_raw["关税率"]
    df_raw["增值税(EGP)"] = (df_raw["CIF(USD)"] * usd_egp + df_raw["埃及关税(EGP)"]) * 0.14
    df_raw["总价(EGP)"] = (df_raw["CIF(USD)"] * usd_egp) + df_raw["埃及关税(EGP)"] + df_raw["增值税(EGP)"]
    
    # 只选出我们要看的列显示
    show_df = df_raw[["商品", "数量", "体积", "总价(EGP)"]]
    st.table(show_df) # 用 Table 格式最稳，不会报错
    
    # 总计
    total_egp = df_raw["总价(EGP)"].sum()
    st.metric("📦 整批货物总预算 (EGP)", f"{total_egp:,.2f}")
    
    if st.button("🗑️ 清空重来"):
        st.session_state.items = []
        st.rerun()
else:
    st.info("清单为空，请在上方填写并点击‘确认添加’")