import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

st.set_page_config(page_title="INMINH CAFÉ - QUẢN LÍ DOANH THU", layout="wide")
st.title("INMINH CAFÉ - QUẢN LÍ DOANH THU")

# === MENU DATA ===
data = [
    ["Bạc xỉu", 500, 17000, 5177], ["Bạc xỉu", 800, 22000, 7404], ["Bạc xỉu", 1000, 27000, 9842],
    ["Cà phê muối", 500, 16000, 1722], ["Cà phê muối", 800, 21000, 1776], ["Cà phê muối", 1000, 26000, 2041],
    ["Cà phê sữa", 500, 15000, 3759], ["Cà phê sữa", 800, 19000, 4569], ["Cà phê sữa", 1000, 23000, 5824],
    ["Cà phê đen", 500, 12000, 3535], ["Cà phê đen", 800, 17000, 4409], ["Cà phê đen", 1000, 20000, 5261],
    ["Matcha latte", 500, 17000, 6584], ["Matcha latte", 800, 22000, 9311], ["Matcha latte", 1000, 26000, 12959],
    ["Matcha latte", 500, 19000, 1722], ["Matcha latte", 800, 24000, 1776], ["Matcha latte", 1000, 28000, 2041],
    ["Trà tắc", 500, 8000, 3809], ["Trà tắc", 800, 10000, 4535], ["Trà tắc", 1000, 15000, 6072],
    ["Trà đường", 500, 6000, 2189], ["Trà đường", 800, 9000, 2435], ["Trà đường", 1000, 10000, 2892]
]
menu_df = pd.DataFrame(data, columns=["Loại nước", "Size", "Giá bán", "Chi phí"])
menu_df["Lợi nhuận"] = menu_df["Giá bán"] - menu_df["Chi phí"]

# === SESSION DATA ===
if "records" not in st.session_state:
    st.session_state.records = []

# === INPUT FORM ===
st.subheader("Nhập thông tin đơn hàng")
with st.form("order_form"):
    col1, col2 = st.columns(2)
    with col1:
        customer_name = st.text_input("Tên khách hàng")
        date = st.date_input("Ngày mua", format="DD/MM/YYYY")
        time = st.time_input("Giờ mua")
    with col2:
        drink = st.selectbox("Loại nước", menu_df["Loại nước"].unique())
        size = st.selectbox("Size (ml)", sorted(menu_df[menu_df["Loại nước"]==drink]["Size"].unique()))
        quantity = st.number_input("Số lượng", min_value=1, value=1)

    submit = st.form_submit_button("Thêm đơn hàng")

    if submit:
        row = menu_df[(menu_df["Loại nước"]==drink) & (menu_df["Size"]==size)].iloc[0]
        total_price = row["Giá bán"] * quantity
        total_cost = row["Chi phí"] * quantity
        total_profit = row["Lợi nhuận"] * quantity
        st.session_state.records.append({
            "Khách hàng": customer_name,
            "Ngày": date,
            "Giờ": time.strftime("%H:%M"),
            "Loại nước": drink,
            "Size": size,
            "Số lượng": quantity,
            "Doanh thu": total_price,
            "Chi phí": total_cost,
            "Lợi nhuận": total_profit
        })
        st.success("✔️ Đã thêm đơn hàng")

# === TABLE & CHART ===
st.subheader("Tổng hợp doanh thu")

if st.session_state.records:
    df = pd.DataFrame(st.session_state.records)
    st.dataframe(df, use_container_width=True)

    # Tổng theo ngày
    df_grouped = df.groupby("Ngày")[["Doanh thu", "Chi phí", "Lợi nhuận"]].sum().reset_index()

    st.subheader("Biểu đồ theo ngày")
    chart = px.bar(df_grouped, x="Ngày", y=["Doanh thu", "Chi phí", "Lợi nhuận"], barmode="group")
    st.plotly_chart(chart, use_container_width=True)
else:
    st.info("Chưa có đơn hàng nào.")
