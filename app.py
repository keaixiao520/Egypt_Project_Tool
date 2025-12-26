# --- 功能 1：项目成本利润管家 (优化版) ---
if menu == "成本计算器":
    st.header("📊 项目成本与利润精算看板")
    
    # 1. 顶部全局预算设置
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        total_budget = st.number_input("项目总预算 (CNY)", min_value=0.0, value=1000000.0, step=10000.0)
    with col_b2:
        total_revenue = st.number_input("预估总收入/合同额 (CNY)", min_value=0.0, value=1200000.0, step=10000.0)

    st.divider()

    # 2. 专业分项录入
    st.subheader("🛠️ 各专业成本明细")
    col1, col2, col3 = st.columns([2, 2, 2])
    
    with col1:
        major = st.selectbox("选择专业", ["建筑工程", "钢结构", "机电工程", "装修工程", "其他"])
    with col2:
        mat_cost = st.number_input(f"{major}-材料费 (CNY)", min_value=0.0, value=0.0)
    with col3:
        ins_cost = st.number_input(f"{major}-安装/人工费 (CNY)", min_value=0.0, value=0.0)

    if st.button("➕ 计入成本清单"):
        new_detail = {
            "专业": major,
            "材料费": mat_cost,
            "安装费": ins_cost,
            "小计": mat_cost + ins_cost
        }
        st.session_state.items.append(new_detail)
        st.toast(f"{major} 成本已录入")

    # 3. 数据处理与展示
    if st.session_state.items:
        df = pd.DataFrame(st.session_state.items)
        
        # 计算核心指标
        total_cost = df["小计"].sum()
        total_profit = total_revenue - total_cost
        profit_margin = (total_profit / total_revenue) * 100 if total_revenue != 0 else 0
        budget_remaining = total_budget - total_cost

        # 4. 关键指标可视化 (KPI)
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        kpi1.metric("总成本", f"¥{total_cost:,.2f}", delta=f"预算剩余: ¥{budget_remaining:,.0f}")
        kpi2.metric("总收入", f"¥{total_revenue:,.2f}")
        kpi3.metric("预估利润", f"¥{total_profit:,.2f}", delta="盈利" if total_profit > 0 else "亏损", delta_color="normal")
        kpi4.metric("利润率", f"{profit_margin:.2f}%")

        st.dataframe(df, use_container_width=True)
        
        if st.button("🗑️ 重置所有数据"):
            st.session_state.items = []
            st.rerun()
    else:
        st.info("请在上方录入各专业的材料与安装成本。")
