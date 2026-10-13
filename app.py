import streamlit as st
import pandas as pd
import numpy as np

# ---------------------------------------------------------
# 1. Khởi tạo dữ liệu giả lập cho 10 sinh viên
# ---------------------------------------------------------
np.random.seed(42) # Cố định dữ liệu mẫu

data = {
    "Họ tên": [
        "Nguyễn Văn A", "Trần Thị B", "Lê Văn C", "Phạm Thị D", "Hoàng Văn E",
        "Vũ Thị F", "Đặng Văn G", "Bùi Thị H", "Đỗ Văn I", "Hồ Thị K"
    ],
    "Chuyên cần": np.random.randint(7, 11, size=10),
    "Giữa kỳ": np.random.uniform(5.0, 10.0, size=10).round(1),
    "Cuối kỳ": np.random.uniform(4.0, 10.0, size=10).round(1)
}

df = pd.DataFrame(data)

# Tính Điểm tổng kết: 10% Chuyên cần + 30% Giữa kỳ + 60% Cuối kỳ
df["Tổng kết"] = (df["Chuyên cần"] * 0.1 + df["Giữa kỳ"] * 0.3 + df["Cuối kỳ"] * 0.6).round(1)

# Xếp loại dựa trên Điểm tổng kết
def xep_loai(score):
    if score >= 8.5:
        return "Xuất sắc"
    elif score >= 7.0:
        return "Giỏi"
    elif score >= 5.5:
        return "Khá"
    elif score >= 4.0:
        return "Trung bình"
    else:
        return "Yếu"

df["Xếp loại"] = df["Tổng kết"].apply(xep_loai)

# ---------------------------------------------------------
# 2. Xây dựng giao diện Web App bằng Streamlit
# ---------------------------------------------------------

# Hiển thị tiêu đề
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")

# Hiển thị bảng điểm của 10 sinh viên
st.subheader("📋 Bảng điểm sinh viên")
st.dataframe(df, use_container_width=True)

# Hiển thị các chỉ số thống kê
st.subheader("📊 Thống kê chung của lớp")

col1, col2, col3, col4 = st.columns(4)

# Điểm trung bình lớp
dtb_lop = df["Tổng kết"].mean().round(2)
col1.metric("Điểm TB lớp", dtb_lop)

# Sinh viên cao điểm nhất
sv_max = df.loc[df["Tổng kết"].idxmax()]
col2.metric("Cao nhất", f"{sv_max['Tổng kết']} điểm", help=f"Sinh viên: {sv_max['Họ tên']}")

# Sinh viên thấp điểm nhất
sv_min = df.loc[df["Tổng kết"].idxmin()]
col3.metric("Thấp nhất", f"{sv_min['Tổng kết']} điểm", help=f"Sinh viên: {sv_min['Họ tên']}")

# Số sinh viên đạt (Tổng kết >= 4.0)
so_sv_dat = (df["Tổng kết"] >= 4.0).sum()
col4.metric("Số SV đạt", f"{so_sv_dat} / 10")

st.markdown("---")

# Danh sách xổ xuống (Selectbox) để tra cứu thông tin chi tiết
st.subheader("🔍 Tra cứu điểm sinh viên")
selected_student = st.selectbox("Chọn một sinh viên:", df["Họ tên"])

if selected_student:
    student_info = df[df["Họ tên"] == selected_student].iloc[0]
    
    col_a, col_b, col_c, col_d, col_e = st.columns(5)
    col_a.write(f"**Chuyên cần:** {student_info['Chuyên cần']}")
    col_b.write(f"**Giữa kỳ:** {student_info['Giữa kỳ']}")
 col_c.write(f"**Cuối kỳ:** {student_info['Cuối kỳ']}")
    col_d.write(f"**Tổng kết:** {student_info['Tổng kết']}")
    col_e.write(f"**Xếp loại:** {student_info['Xếp loại']}")

st.markdown("---")

# Hiển thị biểu đồ cột điểm tổng kết
st.subheader("📈 Biểu đồ điểm tổng kết")
chart_data = df.set_index("Họ tên")[["Tổng kết"]]
st.bar_chart(chart_data)

st.markdown("---")

# Hiển thị Họ tên và MSSV ở cuối trang với kích thước chữ nhỏ
st.markdown(
    "<p style='text-align: center; color: gray; font-size: 13px;'>"
    "Người tạo ứng dụng: <b>TRANNGOCANH</b> - MSSV: <b>034208004115</b>"
    "</p>", 
    unsafe_allow_html=False   