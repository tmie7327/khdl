import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# 1. Khởi tạo dữ liệu từ đề bài
data = {
    'Chiều cao (cm)': [160, 170, 180, 175, 165],
    'Cân nặng (kg)': [55, 65, 80, 70, 60],
    'BMI': [21.5, 22.5, 24.7, 22.9, 22.0]
}
df = pd.DataFrame(data, index=['A', 'B', 'C', 'D', 'E'])

print("--- 1. DỮ LIỆU GỐC (3 CHIỀU) ---")
print(df)

# 2. Chuẩn hóa dữ liệu (Z-score Normalization)
scaler = StandardScaler()
scaled_data = scaler.fit_transform(df)

print("\n--- 2. DỮ LIỆU ĐÃ CHUẨN HÓA ---")
scaled_df = pd.DataFrame(scaled_data, columns=df.columns, index=df.index)
print(scaled_df)

# 3. Chạy thuật toán PCA giảm về 2 chiều
pca = PCA(n_components=2)
components = pca.fit_transform(scaled_data)

# 4. Hiển thị kết quả dữ liệu 2 chiều
pca_df = pd.DataFrame(data=components, 
                      columns=['PC1 (Trục chính 1)', 'PC2 (Trục chính 2)'], 
                      index=df.index)

print("\n--- 3. KẾT QUẢ DỮ LIỆU ĐÃ GIẢM CÒN 2 CHIỀU BẰNG PCA ---")
print(pca_df)

# Hiển thị độ mất mát thông tin
variance = pca.explained_variance_ratio_
print("\n--- 4. MỨC ĐỘ BẢO TOÀN THÔNG TIN ---")
print(f"Lượng thông tin PC1 giữ được: {variance[0]*100:.2f}%")
print(f"Lượng thông tin PC2 giữ được: {variance[1]*100:.2f}%")
print(f"=> Tổng cộng 2 chiều mới giữ được {sum(variance)*100:.2f}% (Gần như toàn bộ thông tin gốc)")

# 5. Vẽ biểu đồ minh họa
plt.figure(figsize=(12, 5))

# Đồ thị 1: Biểu đồ phân tán (Scatter plot) kết quả PCA
plt.subplot(1, 2, 1)
plt.scatter(components[:, 0], components[:, 1], color='dodgerblue', s=100, edgecolor='k', zorder=3)

# Gắn tên A, B, C, D, E vào độ thị
for i, txt in enumerate(pca_df.index):
    plt.annotate(txt, (components[i, 0], components[i, 1]), 
                 textcoords="offset points", xytext=(0, 10), ha='center', 
                 fontsize=12, fontweight='bold')

plt.title('Dữ liệu trên không gian 2D (PC1 vs PC2)', fontsize=13)
plt.xlabel(f'Thành phần chính 1 (PC1): {variance[0]*100:.1f}%')
plt.ylabel(f'Thành phần chính 2 (PC2): {variance[1]*100:.1f}%')
plt.axhline(0, color='gray', linestyle='--', linewidth=1, zorder=1)
plt.axvline(0, color='gray', linestyle='--', linewidth=1, zorder=1)
plt.grid(alpha=0.4, zorder=0)

# Đồ thị 2: Cột phần trăm thể hiện mức độ bảo toàn thông tin của các Trục
plt.subplot(1, 2, 2)
bars = plt.bar(['PC1', 'PC2'], variance * 100, color=['skyblue', 'lightgreen'], edgecolor='k', width=0.5, zorder=3)
plt.title('Tỷ lệ thông tin được bảo toàn', fontsize=13)
plt.ylabel('Phần trăm (%)')
plt.ylim(0, 110)

# Viết % lên đầu cột
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 2, f'{yval:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=11)

plt.grid(axis='y', alpha=0.4, zorder=0)
plt.tight_layout()
plt.show()
