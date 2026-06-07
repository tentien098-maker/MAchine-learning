import socket

# ==========================================
# CÀI ĐẶT THÔNG SỐ (Chỉ cần sửa dòng số 7 cho các lần sau)
# ==========================================
ESP_IP = "192.168.1.55"   # Đã đổi sang IP mới mạng "Tro so 7"
TEN_FILE_LUU = "gach.csv" # Sửa tên file ở đây: gach.csv / tham.csv / goghe.csv

PORT = 8080

# ==========================================
# BẮT ĐẦU THU THẬP DỮ LIỆU
# ==========================================
print(f"🔄 Đang tìm xe robot tại IP {ESP_IP}...")

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ESP_IP, PORT))
        print(f"Đã kết nối WiFi với xe! Đang lưu data vào {TEN_FILE_LUU}...")
        print("Bấm nút VUÔNG MÀU ĐỎ (Stop) trên Spyder để dừng đo khi chạy đủ 1 phút.\n")

        # Mở file để ghi dữ liệu
        with open(TEN_FILE_LUU, "w", encoding="utf-8") as f:
            while True:
                # Nhận dữ liệu từ ESP32 qua WiFi
                data = s.recv(1024).decode('utf-8')
                if data:
                    print(data, end="") # Hiển thị số đang nhảy trên màn hình
                    f.write(data)       # Ghi thẳng vào file CSV
                    
except KeyboardInterrupt:
    print(f"\nLƯU THÀNH CÔNG: Dữ liệu đã nằm gọn trong file {TEN_FILE_LUU}!")
except Exception as e:
    print(f"\nLỗi kết nối: {e}")
    print("Hãy chắc chắn xe đang bật nguồn và máy tính dùng chung WiFi 'Tro so 7'.")