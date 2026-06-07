#  Edge AI Robot: Real-time Surface Classification 
![ESP32](https://img.shields.io/badge/Microcontroller-ESP32-blue)
![Machine Learning](https://img.shields.io/badge/AI-TinyML%20%2F%20Edge%20AI-orange)
![Sensor](https://img.shields.io/badge/Sensor-MPU6050-lightgrey)
![Status](https://img.shields.io/badge/Status-Completed-success)

##  Giới thiệu dự án (Overview)
Dự án này ứng dụng công nghệ **Edge AI (Trí tuệ nhân tạo tại biên)** lên vi điều khiển giới hạn tài nguyên (ESP32) để giúp Robot tự hành nhận biết bề mặt nó đang di chuyển theo thời gian thực. 

Bằng cách phân tích tín hiệu rung lắc từ cảm biến gia tốc MPU6050 thông qua mô hình Machine Learning (Decision Tree / Random Forest), robot có thể phân loại chính xác 3 loại địa hình:
1. **Sàn Gạch (Tile)** - Bằng phẳng, ít ma sát.
2. **Thảm (Carpet)** - Ma sát cao, bám bánh.
3. **Gồ Ghề (Rough/Obstacles)** - Rung lắc mạnh.

Dự án là nền tảng tuyệt vời để phát triển hệ thống tự động điều chỉnh lực kéo, tốc độ động cơ (Traction Control) cho robot dựa trên địa hình thực tế.

![Demo Robot](link_anh_robot_cua_ban_o_day.jpg)
*(Chèn hình ảnh chiếc xe robot của bạn vào đây)*

---

##  Tính năng nổi bật (Key Features)
*  Machine Learning on Edge:** Mô hình AI được huấn luyện trên Python và nạp trực tiếp vào ESP32 bằng C++ (thư viện `micromlgen`), không cần kết nối Cloud để xử lý.
*  Lọc nhiễu kỹ thuật số (DSP):** Sử dụng thuật toán Trung bình động hàm mũ (EMA - Exponential Moving Average) để làm mượt sóng rung của động cơ DC, giúp AI nhận diện rõ ràng hơn.
*  Thuật toán "Majority Voting":** Hệ thống lấy mẫu 10 lần/giây và "bầu cử" để chốt kết quả cuối cùng, giúp loại bỏ các sai số tức thời và đẩy độ chính xác thực tế lên **> 95%**.
*  Giao diện giám sát WiFi (TCP/IP):** Kết quả phân tích được stream không dây từ ESP32 về phần mềm Python (PC) theo thời gian thực.

---

##  Cấu trúc Phần cứng & Phần mềm (Hardware & Tech Stack)

### Phần cứng (Hardware)
* Vi điều khiển: ESP32 DOIT DevKit V1
* Cảm biến quán tính (IMU): MPU6050
* Điều khiển động cơ: Module L298N
* Khung gầm: Robot 4 bánh (4WD)
* Nguồn cấp: Pin 18650

### Phần mềm & Thư viện (Software)
* **Python:** `pandas`, `scikit-learn` (Huấn luyện AI), `micromlgen` (Xuất mô hình sang C++), `socket` (Giao tiếp TCP/IP).
* **Arduino IDE (C++):** `Adafruit_MPU6050`, `WiFi`.

---

##  Sơ đồ hoạt động (How it works)

1. **Thu thập dữ liệu (Data Collection):** Cảm biến MPU6050 đọc gia tốc 3 trục (X, Y, Z) khi xe chạy trên các bề mặt và gửi về máy tính.
2. **Huấn luyện (Training):** Dữ liệu được đưa qua bộ lọc EMA, sau đó huấn luyện bằng thuật toán Machine Learning.
3. **Triển khai (Deployment):** Mô hình AI được xuất thành file Header `.h` (Mảng logic if-else) và nạp thẳng vào bộ nhớ Flash của ESP32.
4. **Suy luận thời gian thực (Inference):** Khi chạy thực tế, ESP32 thu thập dữ liệu rung, lọc EMA, đưa vào hàm `predict()` của mô hình và dùng thuật toán bầu cử để đưa ra kết luận.
5. **Giám sát (Monitoring):** ESP32 đóng vai trò là WiFi Server, liên tục gửi chuỗi text kết quả về Client (Python) hiển thị.

---

##  Hướng dẫn sử dụng (Quick Start)

### 1. Nạp code cho ESP32
* Tải toàn bộ mã nguồn trong thư mục `ESP32_Code`.
* Mở file `.ino` bằng Arduino IDE. Đảm bảo file `model_DecisionTree.h` nằm cùng thư mục.
* Cài đặt thông số WiFi mạng nội bộ của bạn trong code.
* Bấm **Upload** xuống ESP32.

### 2. Khởi chạy Dashboard hiển thị trên PC
* Kết nối máy tính vào cùng mạng WiFi với ESP32.
* Cập nhật địa chỉ `ESP_IP` trong file `PC_Dashboard.py` cho đúng với IP của xe.
* Chạy script Python:
```bash
python PC_Dashboard.py
