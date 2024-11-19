import streamlit as st
import pandas as pd

def calculate_equal_principal(principal, annual_rate, months, prepayment=0):
    monthly_rate = annual_rate / 12 / 100
    monthly_principal = principal / months
    current_principal = principal
    payments = []

    for month in range(1, months + 1):
        if current_principal <= 0:
            break

        monthly_interest = current_principal * monthly_rate
        monthly_payment = monthly_principal + monthly_interest
        
        # 计算年月
        year = (month - 1) // 12 + 1
        month_in_year = (month - 1) % 12 + 1
        month_label = f"第{year}年{month_in_year}月"

        # 确保不产生负数
        principal_payment = min(monthly_principal, current_principal)
        total_payment = principal_payment + monthly_interest
        
        payments.append({
            "月份": month_label,
            "偿还本金": round(principal_payment, 2),
            "偿还利息": round(monthly_interest, 2),
            "总偿还": round(total_payment, 2),
            "提前还款": 0.0,
            "剩余待还本金": round(max(current_principal - principal_payment, 0), 2),
            "剩余待还全部": round(max(current_principal - principal_payment + monthly_interest, 0), 2)
        })
        
        current_principal -= principal_payment

        # 每年年底进行提前还款
        if month % 12 == 0 and prepayment > 0:
            current_principal -= prepayment
            payments[-1]["提前还款"] = round(prepayment, 2)
            payments[-1]["剩余待还本金"] = round(max(current_principal, 0), 2)
            payments[-1]["剩余待还全部"] = round(max(current_principal, 0), 2)

    return payments, payments[-1]["总偿还"] if payments else 0

def calculate_equal_installment(principal, annual_rate, months, prepayment=0):
    monthly_rate = annual_rate / 12 / 100
    if monthly_rate > 0:
        monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)
    else:
        monthly_payment = principal / months

    current_principal = principal
    payments = []

    for month in range(1, months + 1):
        if current_principal <= 0:
            break

        interest_payment = current_principal * monthly_rate
        principal_payment = monthly_payment - interest_payment
        
        # 确保不产生负数
        principal_payment = min(principal_payment, current_principal)
        total_payment = principal_payment + interest_payment

        # 计算年月
        year = (month - 1) // 12 + 1
        month_in_year = (month - 1) % 12 + 1
        month_label = f"第{year}年{month_in_year}月"

        payments.append({
            "月份": month_label,
            "偿还本金": round(principal_payment, 2),
            "偿还利息": round(interest_payment, 2),
            "总偿还": round(total_payment, 2),
            "提前还款": 0.0,
            "剩余待还本金": round(max(current_principal - principal_payment, 0), 2),
            "剩余待还全部": round(max(current_principal - principal_payment + interest_payment, 0), 2)
        })
        
        current_principal -= principal_payment

        # 每年年底进行提前还款
        if month % 12 == 0 and prepayment > 0:
            current_principal -= prepayment
            payments[-1]["提前还款"] = round(prepayment, 2)
            payments[-1]["剩余待还本金"] = round(max(current_principal, 0), 2)
            payments[-1]["剩余待还全部"] = round(max(current_principal, 0), 2)

    return payments, monthly_payment if payments else 0

# Streamlit页面设置
st.title("贷款计算器")

# 用户输入
total_loan = st.number_input("总贷款数 (元)", min_value=0.0, value=600000.0, step=10000.0)
total_months = st.number_input("总还款月数", min_value=1, value=360, step=1)
current_rate = st.number_input("当前利率 (%)", min_value=0.0, value=3.6, step=0.1)
prepayment_amount = st.number_input("每年提前还款金额 (元)/默认选择还款金额不变，减少还款期数", min_value=0.0, value=0.0, step=1000.0)

repayment_type = st.selectbox("贷款方式", ("等额本息", "等额本金"))

# 按钮计算
if st.button("计算"):
    if repayment_type == "等额本息":
        payments, monthly_payment = calculate_equal_installment(total_loan, current_rate, total_months, prepayment_amount)
    elif repayment_type == "等额本金":
        payments, monthly_payment = calculate_equal_principal(total_loan, current_rate, total_months, prepayment_amount)

    # 生成数据表
    df = pd.DataFrame(payments)

    # 表格导出
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="下载还款计划",
        data=csv,
        file_name='还款计划.csv',
        mime='text/csv',
    )

    # 输出结果
    st.write(f"每月还款金额: {monthly_payment:.2f} 元")
    remaining_months = len(payments)
    years_left = remaining_months // 12
    months_left = remaining_months % 12
    st.write(f"剩余还款时间: {years_left} 年 {months_left} 个月")
