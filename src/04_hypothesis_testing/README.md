# Module 04: Thống Kê Suy Diễn & Kiểm Định Giả Thuyết (Hypothesis Testing - Chương 1)

> **Môn học:** Nhập môn Khoa học Dữ liệu (Introduction to Data Science) - PTIT  
> **Giảng viên hướng dẫn:** TS. Thái Tuyết Hải  
> **Trách nhiệm:** Thành viên 2 (Data Analyst & Statistician)  
> **Môi trường thực thi:** Python 3.13 (`.venv`)

---

## 🎯 Mục Tiêu & Phương Pháp Thống Kê
Module áp dụng các phương pháp toán học và thống kê suy diễn theo chuẩn giáo trình **Chương 1** để kiểm chứng các giả thuyết khoa học về trò chơi với mức ý nghĩa $\alpha = 0.05$:

1. **Kiểm định 1 ($Z$-test Tỷ lệ 2 phía - Task 2.1):** Kiểm định xem Phe Xanh (Blue Side) có lợi thế thắng vượt trội so với Phe Đỏ (Red Side) hay không.
2. **Kiểm định 2 (Two-sample Independent $t$-test - Task 2.2):** So sánh hiệu quả lăn cầu tuyết (Snowball Lead $\ge 2,000\text{g}$ lúc 10 phút) giữa Đấu Giải vs Solo Rank.
3. **Kiểm định 3 (Chi-square Test $\chi^2$ - Task 2.3):** So sánh tác động của việc ăn 3 Sâu Hư Không đầu vs Rồng Nguyên Tố đầu đến tỷ lệ thắng chung cuộc.

---

## 🚀 Hướng Dẫn Vận Hành (CLI Usage)

### 1. Chạy Kiểm Định Task 2.1 (Lợi Thế Phe Xanh)
```powershell
# Chạy kiểm định với mức ý nghĩa mặc định alpha = 0.05 và tự động xuất CSV
.\.venv\Scripts\python.exe src/04_hypothesis_testing/test_blue_side_advantage.py

# Chạy với mức ý nghĩa tùy chỉnh (ví dụ: alpha = 0.01)
.\.venv\Scripts\python.exe src/04_hypothesis_testing/test_blue_side_advantage.py --alpha 0.01
```

---

## 📊 Kết Quả Kiểm Định Task 2.1 Thực Tế (Dữ Liệu Dự Án)

| Tập Dữ Liệu | Cỡ Mẫu ($n$) | Blue Thắng | Tỷ Lệ Thắng ($\hat{p}$) | $Z$-Score | $p$-value | Khoảng Tin Cậy 95% | Kết Luận Thống Kê ($\alpha = 0.05$) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Đấu Giải (Pro Play)** | **3,000** | 1,605 | **53.50%** | **+3.8341** | **$0.000126^{***}$** | $[51.72\%, 55.28\%]$ | ✅ **Bác bỏ $H_0$** (Phe Xanh có lợi thế vượt trội rõ rệt). |
| **Solo Rank (VN2 & KR)** | **1,009** | 459 | **45.49%** | **-2.8648** | **$0.004173^{**}$** | $[42.42\%, 48.56\%]$ | ✅ **Bác bỏ $H_0$** (Phe Đỏ thắng $54.51\%$ cao hơn). |
| *Solo Rank VN2* | 550 | 259 | 47.09% | -1.3645 | 0.1724 | $[42.92\%, 51.26\%]$ | ❌ Chưa đủ bằng chứng bác bỏ $H_0$. |
| *Solo Rank KR* | 459 | 200 | 43.57% | -2.7539 | $0.0059^{**}$ | $[39.04\%, 48.11\%]$ | ✅ **Bác bỏ $H_0$** (Phe Đỏ áp đảo tại Rank Hàn). |
| *Giải Đấu LCP* | 466 | 257 | 55.15% | +2.2236 | $0.0262^{*}$ | $[50.63\%, 59.67\%]$ | ✅ **Bác bỏ $H_0$** (Lợi thế Phe Xanh rõ rệt). |
| *Giải Đấu MSI* | 151 | 89 | 58.94% | +2.1972 | $0.0280^{*}$ | $[51.09\%, 66.79\%]$ | ✅ **Bác bỏ $H_0$** (First Pick đem lại lợi thế lớn). |

---

## 💾 Tệp Dữ Liệu Kết Quả Đầu Ra
* `data/processed/hypothesis_test_1_blue_side.csv`: Bảng tổng hợp đầy đủ các chỉ số thống kê, $Z$-score, $p$-value và khoảng tin cậy 95%.
