import streamlit as st

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

# =========================
# CSS GIAO DIỆN
# =========================
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #1565C0;
        margin-bottom: 5px;
    }

    .sub-title {
        text-align: center;
        color: #666;
        margin-bottom: 30px;
    }

    .result-box {
        background-color: #f5f9ff;
        border: 1px solid #d6e7ff;
        border-radius: 12px;
        padding: 20px;
        margin-top: 20px;
    }

    .result-item {
        font-size: 18px;
        margin: 10px 0;
    }

    .result-value {
        color: #1565C0;
        font-weight: bold;
    }

    .total-box {
        background-color: #e8f5e9;
        border: 1px solid #b7dfba;
        border-radius: 12px;
        padding: 20px;
        margin-top: 15px;
    }

    .note {
        color: #666;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)


# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================
def format_money(value):
    return f"{value:,.0f} VNĐ".replace(",", ".")


# =========================
# TIÊU ĐỀ
# =========================
st.markdown(
    '<h1 class="main-title">💰 TÍNH LÃI GỬI TIẾT KIỆM</h1>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="sub-title">Tính nhanh tiền lãi và tổng số tiền nhận được</p>',
    unsafe_allow_html=True
)


# =========================
# NHẬP THÔNG TIN
# =========================
st.subheader("📋 Thông tin khoản gửi")

col1, col2 = st.columns(2)

with col1:
    so_tien_gui = st.number_input(
        "Số tiền gửi (VNĐ)",
        min_value=0.0,
        value=100_000_000.0,
        step=1_000_000.0,
        format="%.0f"
    )

    ky_han = st.number_input(
        "Kỳ hạn (tháng)",
        min_value=1,
        max_value=120,
        value=12,
        step=1
    )

with col2:
    lai_suat = st.number_input(
        "Lãi suất (%/năm)",
        min_value=0.0,
        max_value=100.0,
        value=6.0,
        step=0.01,
        format="%.2f"
    )

    hinh_thuc = st.selectbox(
        "Hình thức nhận lãi",
        [
            "Cuối kỳ",
            "Hàng tháng",
            "Hàng quý"
        ]
    )


# =========================
# TÍNH TOÁN
# =========================
if st.button("🧮 TÍNH LÃI", type="primary", use_container_width=True):

    if so_tien_gui <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    if lai_suat < 0:
        st.error("Lãi suất không được nhỏ hơn 0.")
        st.stop()

    # Lãi suất theo năm chuyển sang số thập phân
    lai_suat_nam = lai_suat / 100

    # Tổng số tháng gửi
    tong_thang = ky_han

    # Tổng tiền lãi:
    # Tiền lãi = Tiền gốc × lãi suất năm × số tháng / 12
    tong_tien_lai = so_tien_gui * lai_suat_nam * tong_thang / 12

    # =========================
    # TÍNH LÃI ĐỊNH KỲ
    # =========================
    if hinh_thuc == "Cuối kỳ":
        so_ky_nhan_lai = 1
        lai_dinh_ky = tong_tien_lai
        mo_ta_dinh_ky = f"Tiền lãi nhận sau {ky_han} tháng"

    elif hinh_thuc == "Hàng tháng":
        so_ky_nhan_lai = tong_thang
        lai_dinh_ky = tong_tien_lai / so_ky_nhan_lai
        mo_ta_dinh_ky = "Tiền lãi nhận mỗi tháng"

    else:  # Hàng quý
        so_ky_nhan_lai = tong_thang // 3

        # Nếu kỳ hạn không chia hết cho 3,
        # phần tháng lẻ vẫn được tính vào tổng lãi.
        if so_ky_nhan_lai > 0:
            lai_dinh_ky = tong_tien_lai / so_ky_nhan_lai
        else:
            lai_dinh_ky = tong_tien_lai

        mo_ta_dinh_ky = "Tiền lãi nhận mỗi quý"

    # Tổng số tiền cuối cùng
    tong_tien_nhan = so_tien_gui + tong_tien_lai

    # =========================
    # HIỂN THỊ KẾT QUẢ
    # =========================
    st.success("✅ Đã tính toán thành công!")

    st.markdown(
        f"""
        <div class="result-box">
            <h3>📊 Kết quả</h3>

            <div class="result-item">
                💵 Tiền gốc:
                <span class="result-value">
                    {format_money(so_tien_gui)}
                </span>
            </div>

            <div class="result-item">
                📈 Lãi suất:
                <span class="result-value">
                    {lai_suat:.2f}%/năm
                </span>
            </div>

            <div class="result-item">
                ⏱️ Kỳ hạn:
                <span class="result-value">
                    {ky_han} tháng
                </span>
            </div>

            <div class="result-item">
                🏦 Hình thức nhận lãi:
                <span class="result-value">
                    {hinh_thuc}
                </span>
            </div>

            <hr>

            <div class="result-item">
                💸 {mo_ta_dinh_ky}:
                <span class="result-value">
                    {format_money(lai_dinh_ky)}
                </span>
            </div>

            <div class="result-item">
                💰 Tổng tiền lãi:
                <span class="result-value">
                    {format_money(tong_tien_lai)}
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="total-box">
            <h3>💰 TỔNG TIỀN NHẬN ĐƯỢC</h3>
            <div style="font-size: 28px; color: #2E7D32; font-weight: bold;">
                {format_money(tong_tien_nhan)}
            </div>
            <p class="note">
                = Tiền gốc + Tổng tiền lãi
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================
# GHI CHÚ
# =========================
st.markdown("---")

st.info(
    """
    **Lưu ý:** Công thức trên tính lãi đơn theo lãi suất năm:
    
    Tiền lãi = Tiền gốc × Lãi suất năm × Số tháng / 12
    
    Kết quả mang tính tham khảo. Thực tế ngân hàng có thể áp dụng
    cách tính theo số ngày thực tế, cơ sở 365/360 ngày, quy định riêng
    về kỳ hạn và phương thức trả lãi.
    """
  )
