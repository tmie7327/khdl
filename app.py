from pathlib import Path

import pandas as pd
import streamlit as st

from stock_pricing import (
    DEFAULT_FILE,
    build_linear_model,
    extract_company_info,
    evaluate_model,
    forecast_close,
    get_default_file_path,
    get_year_summary,
    load_price_history,
    split_train_test,
)


def main() -> None:
    st.set_page_config(
        page_title="Stock Pricing App",
        page_icon="📈",
        layout="wide",
    )

    st.title("Định giá cổ phiếu - CTCP Sợi Thế Kỷ")
    st.caption("Ứng dụng này tải dữ liệu lịch sử giá từ Excel và dự báo giá đóng cửa cho giai đoạn 2023-2026.")

    default_path = get_default_file_path()
    uploaded_file = st.file_uploader(
        "Tải file Excel lịch sử giá (nếu không, app sẽ dùng file mặc định)",
        type=["xlsx"],
    )

    data_source = uploaded_file if uploaded_file is not None else default_path
    if uploaded_file is None and not Path(default_path).exists():
        st.error(
            f"File mặc định không tồn tại: {default_path}\nVui lòng tải file Excel hoặc đặt file vào đường dẫn đó."
        )
        return

    try:
        company_info = extract_company_info(data_source)
        df = load_price_history(data_source)
    except Exception as exc:
        st.error(f"Không thể đọc dữ liệu: {exc}")
        return

    st.markdown(
        f"**Công ty:** {company_info['company']}  \n"
        f"**Báo cáo:** {company_info['report']}"
    )

    if df.empty:
        st.warning("Dữ liệu trống sau khi lọc. Kiểm tra lại file Excel.")
        return

    st.subheader("Tổng quan dữ liệu")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Bắt đầu từ", df["NGÀY"].min().date().isoformat())
    with col2:
        st.metric("Kết thúc đến", df["NGÀY"].max().date().isoformat())
    with col3:
        st.metric("Số ngày giao dịch", len(df))

    st.line_chart(df.rename(columns={"NGÀY": "index"}).set_index("index")["GIÁ ĐÓNG CỬA"])

    st.subheader("Thống kê theo năm")
    year_summary = get_year_summary(df)
    st.dataframe(year_summary)

    st.subheader("Quy trình học máy và đánh giá")
    st.markdown(
        "1. Thu thập dữ liệu từ file Excel.  \n"
        "2. Tiền xử lý: chuyển đổi ngày, làm sạch giá đóng cửa và loại bỏ giá trị không hợp lệ.  \n"
        "3. Tách tập train và test theo thứ tự thời gian (train là dữ liệu cũ, test là dữ liệu mới).  \n"
        "4. Huấn luyện mô hình hồi quy tuyến tính trên tập train.  \n"
        "5. Đánh giá mô hình trên tập test bằng MSE, MAE và R²."
    )

    try:
        train_df, test_df = split_train_test(df, test_ratio=0.2)
        model_eval = build_linear_model(train_df)
        eval_metrics = evaluate_model(model_eval, test_df)
        final_model = build_linear_model(df)
    except Exception as exc:
        st.error(f"Lỗi khi tách hoặc huấn luyện mô hình: {exc}")
        return

    st.markdown(
        f"- Tập train: **{len(train_df)}** dòng, từ {train_df['NGÀY'].min().date()} đến {train_df['NGÀY'].max().date()}  \n"
        f"- Tập test: **{len(test_df)}** dòng, từ {test_df['NGÀY'].min().date()} đến {test_df['NGÀY'].max().date()}"
    )

    st.markdown(
        f"- MSE (trung bình bình phương lỗi): **{eval_metrics['mse']:.2f}**  \n"
        f"- MAE (trung bình sai số tuyệt đối): **{eval_metrics['mae']:.2f}**  \n"
        f"- R² (độ phù hợp): **{eval_metrics['r2']:.4f}**"
    )
    st.markdown(
        "Đây là cách cơ bản để đánh giá mô hình trên dữ liệu chưa từng thấy trước đó. "
        "Mô hình được huấn luyện trên train và đánh giá trên test để tránh rò rỉ dữ liệu."
    )

    st.subheader("Dự báo giá đóng cửa tương lai")
    max_date = df["NGÀY"].max().date()
    forecast_date = st.date_input(
        "Chọn ngày muốn dự báo trong tương lai:",
        value=max_date + pd.Timedelta(days=30),
        min_value=max_date + pd.Timedelta(days=1),
    )

    try:
        prediction_price = forecast_close(final_model, pd.Timestamp(forecast_date))
    except Exception as exc:
        st.error(f"Lỗi khi dự báo giá tương lai: {exc}")
        return

    st.markdown(
        f"- Ngày dự báo: **{forecast_date}**  \n"
        f"- Giá đóng cửa dự báo: **{prediction_price:,.0f} VND**  \n"
        f"- Độ chính xác trên tập kiểm tra (R²): **{eval_metrics['r2']:.4f}**"
    )

    st.markdown(
        "Mô hình dự báo ở đây dựa trên xu hướng tuyến tính của giá đóng cửa theo thời gian. "
        "Kết quả chỉ mang tính tham khảo và không thay thế phân tích tài chính chuyên sâu."
    )

    st.subheader("Dữ liệu lịch sử (10 dòng đầu và 10 dòng cuối)")
    st.dataframe(df.head(10))
    st.dataframe(df.tail(10))

    st.markdown("---")
    st.write(
        "**Hướng dẫn:** Khi đã cài xong, chạy `streamlit run app.py` và mở giao diện web để xem báo cáo và dự báo."
    )


if __name__ == "__main__":
    main()
