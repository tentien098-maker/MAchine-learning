# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 18:01:05 2026

@author: ASUS
"""

import pandas as pd
import sys
import joblib
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay
from micromlgen import port

# ==========================================
# PHẦN 1: TIỀN XỬ LÝ DỮ LIỆU
# ==========================================

# 1. Đọc dữ liệu từ 3 file CSV
try:
    df_gach = pd.read_csv('gach.csv')
    df_tham = pd.read_csv('tham.csv')
    df_goghe = pd.read_csv('goghe.csv')
    print("✅ Đọc 3 file dữ liệu thành công!")
except FileNotFoundError:
    print("❌ LỖI: Không tìm thấy file CSV! Vui lòng kiểm tra lại thư mục làm việc của Spyder.")
    sys.exit()

# 2. Gán nhãn cho từng loại bề mặt sàn
# 0: Sàn gạch/cứng, 1: Thảm, 2: Gồ ghề
df_gach['Nhan_Mat_San'] = 0
df_tham['Nhan_Mat_San'] = 1
df_goghe['Nhan_Mat_San'] = 2

# 3. Gộp dữ liệu và làm sạch
df_tong = pd.concat([df_gach, df_tham, df_goghe], ignore_index=True)
df_tong = df_tong.dropna() # Xóa dòng có giá trị rỗng

print(f"📊 Tổng số mẫu dữ liệu thu thập được: {len(df_tong)} dòng")

# 4. Tách Đặc trưng (X - Dữ liệu cảm biến) và Nhãn (y - Loại sàn)
X = df_tong.drop('Nhan_Mat_San', axis=1) 
y = df_tong['Nhan_Mat_San']               

# ==========================================
# PHẦN 2: HUẤN LUYỆN & ĐÁNH GIÁ MÔ HÌNH
# ==========================================

# 5. Chia tập dữ liệu (80% để học, 20% để kiểm tra)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 6. Huấn luyện mô hình Decision Tree
print("⚙️ Đang huấn luyện mô hình Machine Learning...")
model = DecisionTreeClassifier(random_state=42)
model.fit(X_train, y_train)

# 7. Đánh giá độ chính xác
y_pred = model.predict(X_test)
do_chinh_xac = accuracy_score(y_test, y_pred)

print("==========================================")
print(f"🎯 Độ chính xác của mô hình: {do_chinh_xac * 100:.2f}%")
print("==========================================")

# 8. Vẽ Ma trận nhầm lẫn (Confusion Matrix)
print("📊 Đang xuất biểu đồ...")
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Gạch (0)', 'Thảm (1)', 'Gồ ghề (2)'])
disp.plot(cmap=plt.cm.Blues)
plt.title("Ma Trận Nhầm Lẫn (Confusion Matrix)")
plt.show() # Ảnh sẽ hiện bên tab 'Plots' của Spyder

# ==========================================
# PHẦN 3: LƯU TRỮ VÀ XUẤT MÔ HÌNH
# ==========================================

# 9. Lưu file mô hình (.pkl) để nộp báo cáo
ten_file_model = 'model_phan_loai_san_A5.pkl'
joblib.dump(model, ten_file_model)
print(f"💾 Đã lưu thành công mô hình vào file: {ten_file_model}")

# 10. Xuất mô hình thành dạng code C++ (.h) để nạp vào ESP32
c_code = port(model)
ten_file_cpp = "model_DecisionTree.h"
with open(ten_file_cpp, "w") as f:
    f.write(c_code)
print(f"✅ Đã xuất thành công code C++ ra file: {ten_file_cpp}")