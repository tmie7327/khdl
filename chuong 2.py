import pandas as pd
import numpy as np

# 1. Đọc dữ liệu (Bỏ qua 5 dòng tiêu đề rác trong file Simplize)
df = pd.read_csv('Simplize_STK_PriceHistory_20260512.xlsx - Sheet 1.csv', skiprows=5)

# 2. Đổi tên cột để dễ làm việc
df.columns = ['Ngay', 'Mo_cua', 'Cao_nhat', 'Thap_nhat', 'Dong_cua', 'Thay_doi', 'Pct_Thay_doi', 'Khoi_luong']

# 3. Xử lý định dạng ngày tháng
df['Ngay'] = pd.to_datetime(df['Ngay'], format='%d/%m/%Y', errors='coerce')

# 4. Xử lý định dạng số (Loại bỏ dấu phẩy và chuyển sang float)
num_cols = ['Mo_cua', 'Cao_nhat', 'Thap_nhat', 'Dong_cua', 'Khoi_luong']
for col in num_cols:
    df[col] = df[col].astype(str).str.replace(',', '').astype(float)

# 5. XỬ LÝ GIÁ TRỊ TRỐNG (Dòng 12/05/2026 bị trống)
# Ta xóa dòng này vì dữ liệu chưa hoàn thiện của phiên hiện tại
df = df.dropna(subset=['Dong_cua']).reset_index(drop=True)

# 6. Sắp xếp lại dữ liệu từ cũ nhất đến mới nhất
df = df.sort_values('Ngay')

print("Dữ liệu đã làm sạch thành công!")