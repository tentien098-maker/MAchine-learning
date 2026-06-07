import socket

ESP_IP = "192.168.1.55"  # IP của xe 
PORT = 8080

print(f" Đang tìm xe robot tại IP {ESP_IP}...")

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ESP_IP, PORT))
        print(" Đã kết nối! Xe đang phóng đi và phân tích bề mặt...")
        print(" Bấm nút VUÔNG MÀU ĐỎ (Stop) để phanh xe lại.\n")

        while True:
            # Liên tục nhận kết quả AI từ xe bắn về qua WiFi
            data = s.recv(1024).decode('utf-8')
            if data:
                print(data, end="")
                
except KeyboardInterrupt:
    print("\n dừng khẩn cấp. Đã ngắt kết nối!")
except Exception as e:
    print(f"\n Lỗi kết nối: {e}")