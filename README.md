# Stock Pricing App

Ứng dụng này đọc dữ liệu lịch sử giá từ file Excel `Simplize_STK_PriceHistory_20260512.xlsx` và cung cấp:

- tổng quan dữ liệu giá đóng cửa 2022-2026
- thống kê giá theo năm 2023-2026
- dự báo giá đóng cửa cuối năm theo mô hình tuyến tính

## Cài đặt

```powershell
cd d:\KHDL\.github\khdl
python -m pip install -r requirements.txt
```

## Chạy app

```powershell
streamlit run app.py
```

## Lưu ý

- Nếu cần dùng file Excel khác, hãy tải file lên giao diện hoặc đổi `DEFAULT_FILE` trong `stock_pricing.py`.
- Mô hình dự báo chỉ mang tính tham khảo.
