import pandas as pd
import matplotlib.pyplot as plt

# 1. Đọc dữ liệu (Giả sử file student-mat.csv cùng thư mục)
# Sử dụng sep=';' vì dữ liệu này dùng dấu chấm phẩy phân cách
df = pd.read_csv('student-mat.csv', sep=';')

# 2. Tính toán các giá trị cơ bản (Yêu cầu số 3)
trung_binh_g3 = df['G3'].mean()
print(f"Điểm trung bình cuối kỳ (G3): {trung_binh_g3:.2f}")

# 3. Phân tích tác động của việc đi chơi (Go out) đến kết quả
# Nhóm theo mức độ đi chơi và tính trung bình điểm
goout_impact = df.groupby('goout')['G3'].mean()

# 4. Vẽ biểu đồ đánh giá (Yêu cầu số 2)
goout_impact.plot(kind='line', marker='o', color='red')
plt.title('Mối liên hệ giữa đi chơi và điểm số')
plt.xlabel('Mức độ đi chơi (1: Rất ít - 5: Rất nhiều)')
plt.ylabel('Điểm trung bình G3')
plt.grid(True)
plt.show() 