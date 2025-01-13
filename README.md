# SMATH

Dự án SMATH là một ứng dụng hỗ trợ người dùng nhập vào các hàm số, thực hiện tính toán, vẽ đồ thị và hiển thị kết quả dưới dạng đồ họa hoặc văn bản. Người dùng có thể dễ dàng tương tác với ứng dụng thông qua giao diện đồ họa, nhập các hàm toán học và xem các biểu đồ 3D của chúng.

Ứng dụng hỗ trợ các phép toán như cộng, trừ, nhân, chia, căn bậc hai, hàm lượng giác, lũy thừa, v.v... với khả năng vẽ đồ thị hàm số một cách trực quan và dễ dàng. Ngoài ra, người dùng cũng có thể thêm, xóa các hàm số vào danh sách để theo dõi và vẽ.

### Các tính năng chính:

- Quy đổi nhiều đại lượng
- Nhập và tính toán hàm số với hỗ trợ LaTeX.
- Vẽ đồ thị 2D và 3D cho các hàm số.
- Hỗ trợ bàn phím ảo để nhập các ký hiệu toán học.
- Hiển thị thông tin nhật ký (log) với thông báo lỗi và kết quả tính toán.
- Danh sách các hàm số đã thêm, có thể xóa khi cần thiết.

## Cài đặt và chạy dự án

### Yêu cầu hệ thống:
- Python 3.6 trở lên
- Các thư viện cần thiết đã được liệt kê trong file `requirements.txt`

### Các bước cài đặt:

1. **Tạo môi trường ảo**:
   - Mở terminal và di chuyển vào thư mục `SMATH`.
   - Chạy lệnh sau để tạo môi trường ảo:

     ```bash
     python -m venv venv
     ```

2. **Kích hoạt môi trường ảo**:
   - Trên Windows:

     ```bash
     .\venv\Scripts\activate
     ```

   - Trên macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

3. **Cài đặt các thư viện phụ thuộc**:
   - Sau khi môi trường ảo đã được kích hoạt, chạy lệnh sau để cài đặt tất cả các thư viện cần thiết từ `requirements.txt`:

     ```bash
     pip install -r requirements.txt
     ```

4. **Chạy ứng dụng**:
   - Sau khi cài đặt xong, bạn có thể chạy ứng dụng bằng lệnh:

     ```bash
     python main.py
     ```

   - Đã hoàn thành... <33

### Cấu trúc thư mục:
SMATH
├── main.py  
├── Funcs
│   └── ***.py 
├── requirements.txt 
├── Styles
│   └── index.py 
├── Images
├── Layouts
│   └── layout.py
├── Themes
│   └── theme.py
└── README.md 


