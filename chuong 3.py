import matplotlib.pyplot as plt

# Tính toán các chỉ số thống kê cơ bản
stats = df[['Dong_cua', 'Khoi_luong']].describe()
print(stats)

# Vẽ biểu đồ biến động giá Close
plt.figure(figsize=(12, 5))
plt.plot(df['Ngay'], df['Dong_cua'], label='Giá đóng cửa STK', color='#1f77b4')
plt.title('DIỄN BIẾN GIÁ CỔ PHIẾU STK', fontsize=14, fontweight='bold')
plt.xlabel('Thời gian')
plt.ylabel('Giá (VNĐ)')
plt.grid(True, alpha=0.3)
plt.legend()
plt.show()