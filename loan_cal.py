import streamlit as st
import numpy as np

def calculate_equal_principal(principal, annual_rate, months, prepayment=0):
    monthly_rate = annual_rate / 12 / 100
    monthly_principal = principal / months
    remaining_months = months
    payments = []

    for month in range(1, months + 1):
        monthly_interest = (principal - (month - 1) * monthly_principal) * monthly_rate
        monthly_payment = monthly_principal + monthly_interest
        payments.append(monthly_payment)

        # 每年提前还款
        if month % 12 == 0 and prepayment > 0:
            principal -= prepayment
            remaining_months = months - month

        if principal <= 0:
            remaining_months = month
            break

    return payments, remaining_months

def calculate_equal_installment(principal, annual_rate, months, prepayment=0):
    monthly_rate = annual_rate / 12 / 100
    if monthly_rate > 0:
        monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)
    else:
        monthly_payment = principal / months

    remaining_months = months

    for month in range(1, months + 1):
        interest_payment = principal * monthly_rate
        principal_payment = monthly_payment - interest_payment
        principal -= principal_payment

        # 每年提前还款
        if month % 12 == 0 and prepayment > 0:
            principal -= prepayment
            remaining_months = months - month

        if principal <= 0:
            remaining_months = month
            break

    return monthly_payment, remaining_months

# Streamlit页面设置
st.title("贷款计算器")

# 用户输入
total_loan = st.number_input("总贷款数 (元)", min_value=600000.0)
total_months = st.number_input("总还款月数", min_value=360)
current_rate = st.number_input("当前利率 (%)", min_value=3.6)
prepayment_amount = st.number_input("每年提前还款金额 (元)", min_value=0.0, value=0.0)

repayment_type = st.selectbox("贷款方式", ("等额本息", "等额本金"))

# 按钮计算
if st.button("计算"):
    if repayment_type == "等额本息":
        monthly_payment, remaining_months = calculate_equal_installment(total_loan, current_rate, total_months, prepayment_amount)
    elif repayment_type == "等额本金":
        payments, remaining_months = calculate_equal_principal(total_loan, current_rate, total_months, prepayment_amount)
        monthly_payment = payments[0] if payments else 0

    # 计算剩余年限和月份
    years_left = remaining_months // 12
    months_left = remaining_months % 12

    # 输出结果
    st.write(f"每月还款金额: {monthly_payment:.2f} 元")
    st.write(f"剩余还款时间: {years_left} 年 {months_left} 个月")
