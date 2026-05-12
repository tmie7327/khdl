# Tính đường trung bình động 20 phiên (ngắn hạn) và 50 phiên (trung hạn)
df['MA20'] = df['Dong_cua'].rolling(window=20).mean()
df['MA50'] = df['Dong_cua'].rolling(window=50).mean()

# Vẽ biểu đồ phân tích kỹ thuật
plt.figure(figsize=(12, 6))
plt.plot(df['Ngay'], df['Dong_cua'], label='Giá thực tế', alpha=0.3)
plt.plot(df['Ngay'], df['MA20'], label='MA20 - Xu hướng ngắn hạn', color='orange')
plt.plot(df['Ngay'], df['MA50'], label='MA50 - Xu hướng trung hạn', color='red')
plt.title('PHÂN TÍCH XU HƯỚNG CỦA STK QUA ĐƯỜNG TRUNG BÌNH ĐỘNG', fontsize=14)
plt.legend()
plt.show()