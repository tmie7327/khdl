import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- CHƯƠNG 2: LÀM SẠCH DỮ LIỆU ---
def clean_stock_data(file_path):
    # Đọc dữ liệu từ dòng thứ 6 (header thực sự của file)
    df = pd.read_csv(file_path, skiprows=5)
    
    # 1. Chuyển đổi cột NGÀY sang định dạng datetime
    df['NGÀY'] = pd.to_datetime(df['NGÀY'], dayfirst=True, errors='coerce')
    
    # 2. Loại bỏ các dòng bị lỗi hoặc dòng trống (như ngày 12/05/2026 có giá trị bằng 0)
    df = df.dropna(subset=['NGÀY'])
    df = df[df['GIÁ ĐÓNG CỬA'] > 0]
    
    # 3. Sắp xếp dữ liệu theo thứ tự thời gian tăng dần
    df = df.sort_values('NGÀY')
    
    # 4. Tính toán thêm các chỉ báo kỹ thuật (Chương 4)
    # Đường trung bình động 20 phiên (MA20) và 50 phiên (MA50)
    df['MA20'] = df['GIÁ ĐÓNG CỬA'].rolling(window=20).mean()
    df['MA50'] = df['GIÁ ĐÓNG CỬA'].rolling(window=50).mean()
    
    return df

# --- CHƯƠNG 4: HÌNH DUNG DỮ LIỆU (VISUALIZATION) ---
def plot_stock_chart(df):
    # Tạo biểu đồ có 2 phần: Biểu đồ giá và Biểu đồ khối lượng
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                       vertical_spacing=0.1, subplot_titles=('Biểu đồ Nến & MA', 'Khối lượng giao dịch'), 
                       row_width=[0.3, 0.7])

    # 1. Thêm biểu đồ nến (Candlestick)
    fig.add_trace(go.Candlestick(
        x=df['NGÀY'],
        open=df['GIÁ MỞ CỬA'],
        high=df['GIÁ CAO NHẤT'],
        low=df['GIÁ THẤP NHẤT'],
        close=df['GIÁ ĐÓNG CỬA'],
        name='Giá STK'
    ), row=1, col=1)

    # 2. Thêm đường MA20 và MA50
    fig.add_trace(go.Scatter(x=df['NGÀY'], y=df['MA20'], name='MA20', line=dict(color='blue', width=1)), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['NGÀY'], y=df['MA50'], name='MA50', line=dict(color='orange', width=1)), row=1, col=1)

    # 3. Thêm biểu đồ khối lượng (Bar chart)
    fig.add_trace(go.Bar(x=df['NGÀY'], y=df['KHỐI LƯỢNG'], name='Khối lượng', marker_color='gray'), row=2, col=1)

    # Tùy chỉnh giao diện
    fig.update_layout(
        title='PHÂN TÍCH KỸ THUẬT CỔ PHIẾU STK (SỢI THẾ KỶ)',
        yaxis_title='Giá (VND)',
        xaxis_rangeslider_visible=False,
        height=800,
        template='plotly_white'
    )
    
    fig.show()

# Thực thi
file_name = 'Simplize_STK_PriceHistory_20260512.xlsx - Sheet 1.csv'
data_cleaned = clean_stock_data(file_name)
plot_stock_chart(data_cleaned)