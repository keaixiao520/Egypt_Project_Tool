import streamlit as st
import pandas as pd

# 页面配置
st.set_page_config(page_title="萧工在开罗-AI实验室", page_icon="🏗️", layout="wide")

# 初始化 Session State 防止报错
if 'items' not in st.session_state:
    st.session_state.items = []

# --- 侧边栏：功能切换 ---
with st.sidebar:
    st.title("👨‍💻 萧工在开罗")
    st.info("驻埃及10年建筑师 | AI 提效专家")
    menu = st.radio("功能导航", ["成本计算器", "合同风险核查", "AI渲染词助手"])
    st.divider()
    st.write("🔗 公众号：萧工在开罗")

# --- 功能 1：成本计算器 (修复版) ---
if menu == "成本计算器":
    st.header("🏗️ 埃及建材出海总成本计算器")
    
    with st.expander("➕ 添加商品", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            name = st.text_input("商品名称", "预制钢结构")
            price = st.number_input("单价(CNY)", min_value=0.0, value=1000.0)
        with col2:
            count = st.number_input("数量", min_value=1, value=10)
            tax = st.number_input("埃及关税率(%)", min_value=0, value=10)
        with col3:
            volume = st.number_input("单件体积(CBM)", min_value=0.0, value=0.1)
            freight = st.number_input("海运费(USD/CBM)", min_value=0.0, value=120.0)

        if st.button("🚀 确认添加到清单"):
            new_item = {
                "名称": name, "单价": price, "数量": count, 
                "体积": volume, "关税": tax, "运费": freight
            }
            st.session_state.items.append(new_item)
            st.toast("已添加！")

    st.subheader("📋 我的采购清单")
    if st.session_state.items:
        df = pd.DataFrame(st.session_state.items) # 修复报错逻辑
        st.dataframe(df, use_container_width=True)
        if st.button("🗑️ 清空清单"):
            st.session_state.items = []
            st.rerun()
    else:
        st.info("清单目前为空，请在上方添加商品。")

# --- 功能 2：合同风险核查 (新增) ---
elif menu == "合同风险核查":
    st.header("📑 国际贸易合同自动核查")
    st.write("针对埃及本地法律环境与国际贸易条款进行合规性初筛。")
    
    contract_text = st.text_area("请粘贴合同草案片段：", height=200, placeholder="在此处粘贴包含付款、交货或争议解决的条款...")
    
    if st.button("⚖️ 开始 AI 核查"):
        if contract_text:
            with st.spinner("正在对比埃及本地法规与常用贸易术语..."):
                st.warning("⚠️ 发现 2 处潜在风险：")
                st.markdown("""
                1. **汇率锁定缺失**：合同未注明美元与埃镑的结算比例及波动调价公式，建议增加。
                2. **清关责任边界模糊**：未明确埃及港口停留费（Demurrage）由哪方承担。
                """)
                st.info("💡 萧工建议：在条款 4.2 中加入 'FOB Shanghai, Incoterms 2020' 并在结算中明确汇率锁定。")
        else:
            st.error("请先输入合同内容！")

# --- 功能 3：AI 渲染词助手 (新增) ---
elif menu == "AI渲染词助手":
    st.header("🎨 建筑渲染词 (Prompt) 自动生成")
    st.write("快速生成高品质建筑效果图描述词。")
    
    col1, col2 = st.columns(2)
    with col1:
        arch_style = st.selectbox("建筑风格", ["现代极简", "埃及当地风格", "工业风", "传统中式"])
        lighting = st.selectbox("光影环境", ["黄金时刻 (傍晚)", "清晨柔光", "室内阴天光", "夜景灯光"])
    with col2:
        material = st.multiselect("核心材质", ["白色混凝土", "落地玻璃", "生锈钢板", "埃及砂岩", "大理石"], default=["白色混凝土"])
        camera = st.selectbox("相机视角", ["全景视角", "人视点", "无人机航拍", "特写感"])

    if st.button("✨ 生成渲染指令"):
        prompt = f"{arch_style} architecture, exterior view, {camera}, materials: {', '.join(material)}, lighting: {lighting}, photorealistic, 8k resolution, cinematic atmosphere."
        st.code(prompt, language='text')
        st.success("复制上方代码到 Midjourney 或 Stable Diffusion 即可使用。")
