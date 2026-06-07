#include <WiFi.h>
#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

// Nhúng "Bộ não AI" vào ESP32
#include "model_DecisionTree.h"
Eloquent::ML::Port::RandomForest thuat_toan_AI;

// --- THÔNG SỐ WIFI ---
const char* ssid = "Tro so 7";
const char* password = "12345678";
WiFiServer server(8080);

Adafruit_MPU6050 mpu;

// --- KHAI BÁO CHÂN ĐỘNG CƠ ---
const int ENA = 14; 
const int IN1 = 27; 
const int IN2 = 26; 
const int IN3 = 25; 
const int IN4 = 33; 
const int ENB = 32; 

// Biến cho Bộ lọc nhiễu EMA (Giống hệt trên Python)
float ema_x = 0, ema_y = 0, ema_z = 0;
const float ALPHA = 0.2;
bool is_first_reading = true;

void setup() {
  Serial.begin(115200);

  // 1. Cài đặt chân động cơ & Tốc độ tối đa
  pinMode(ENA, OUTPUT); pinMode(IN1, OUTPUT); pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT); pinMode(IN4, OUTPUT); pinMode(ENB, OUTPUT);
  analogWrite(ENA, 255); 
  analogWrite(ENB, 255); 

  // 2. Khởi tạo MPU6050
  if (!mpu.begin()) {
    Serial.println("Loi: Khong tim thay MPU6050!");
    while (1) delay(10);
  }

  // 3. Kết nối WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
  server.begin();
}

void loop() {
  WiFiClient client = server.available(); 

  if (client) {
    // KHI SPYDER KẾT NỐI -> CHO XE CHẠY
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    digitalWrite(IN3, LOW); 
    digitalWrite(IN4, HIGH);

    client.println("=== BAT DAU NHAN DIEN MAT SAN ===");
    
    while (client.connected()) {
      int phieu_bau[3] = {0, 0, 0}; // Đếm số phiếu cho 3 loại sàn: 0(Gạch), 1(Thảm), 2(Gồ ghề)
      
      // CHIẾN THUẬT BẦU CỬ: Lấy 10 mẫu trong 1 giây để chốt kết quả
      for(int i = 0; i < 10; i++) {
        sensors_event_t a, g, temp;
        mpu.getEvent(&a, &g, &temp);

        // Lọc nhiễu EMA
        if (is_first_reading) {
          ema_x = a.acceleration.x; ema_y = a.acceleration.y; ema_z = a.acceleration.z;
          is_first_reading = false;
        } else {
          ema_x = (ALPHA * a.acceleration.x) + ((1.0 - ALPHA) * ema_x);
          ema_y = (ALPHA * a.acceleration.y) + ((1.0 - ALPHA) * ema_y);
          ema_z = (ALPHA * a.acceleration.z) + ((1.0 - ALPHA) * ema_z);
        }

        // Đưa cho AI dự đoán tức thời
        float dac_trung[3] = {ema_x, ema_y, ema_z};
        int du_doan = thuat_toan_AI.predict(dac_trung);
        
        phieu_bau[du_doan]++; // Cộng 1 phiếu cho kết quả AI vừa đoán
        delay(100); // 0.1s lấy 1 mẫu
      }

      // CHỐT KẾT QUẢ CUỐI CÙNG SAU 1 GIÂY
      int ket_qua_chot = 0;
      int max_phieu = phieu_bau[0];
      
      if (phieu_bau[1] > max_phieu) { ket_qua_chot = 1; max_phieu = phieu_bau[1]; }
      if (phieu_bau[2] > max_phieu) { ket_qua_chot = 2; }

      // Bắn thẳng kết quả dạng chữ lên màn hình máy tính
      if (ket_qua_chot == 0)      client.println(">> Phat hien: SAN GACH");
      else if (ket_qua_chot == 1) client.println(">> Phat hien: THAM");
      else if (ket_qua_chot == 2) client.println(">> Phat hien: GO GHE");
    }
    
    // KHI BẤM STOP TRÊN SPYDER -> DỪNG XE
    client.stop();
    digitalWrite(IN1, LOW); digitalWrite(IN2, LOW);
    digitalWrite(IN3, LOW); digitalWrite(IN4, LOW);
    
  } else {
    // CHƯA KẾT NỐI -> XE ĐỨNG IM CHỜ LỆNH
    digitalWrite(IN1, LOW); digitalWrite(IN2, LOW);
    digitalWrite(IN3, LOW); digitalWrite(IN4, LOW);
  }
}