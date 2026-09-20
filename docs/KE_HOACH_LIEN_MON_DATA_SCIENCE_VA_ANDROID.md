# KẾ HOẠCH & CHECKLIST LIÊN MÔN: KHOA HỌC DỮ LIỆU & LẬP TRÌNH ANDROID
**Chiến lược tối ưu:** "1 Sản phẩm lõi — Điểm 10 cả 2 môn học"  
**Học viện:** Học viện Công nghệ Bưu chính Viễn thông (PTIT)  
* **Môn 1:** Nhập môn Khoa học Dữ liệu (TS. Thái Tuyết Hải) — Trọng tâm: *Data Pipeline, SQL 1NF/3NF, Thống kê A/B, ML 2 giai đoạn, Ban/Pick AI*.
* **Môn 2:** Lập trình trên Thiết bị Di động (ThS. Nguyễn Trung Hiếu) — Trọng tâm: *Android Studio, Activity Lifecycle, Intent, UI Layout/RecyclerView, SQLite/Room, Retrofit REST API*.
* **Tên ứng dụng:** **LoL Hextech AI Assistant (Trợ lý Phân tích Cấm/Chọn & Dự đoán Esports Liên Minh Huyền Thoại)**

---

## 🏛️ SƠ ĐỒ KIẾN TRÚC TÍCH HỢP LIÊN MÔN (SYSTEM ARCHITECTURE)

```
       ┌─────────────────────────────────────────────────────────────┐
       │   🧠 BACKEND & DATA SCIENCE ENGINE (Môn Khoa học Dữ liệu)   │
       │   - CSDL SQLite: lol_live_data.db (Chuẩn 1NF & 3NF)          │
       │   - 2-Stage Machine Learning: Draft (Phút 0) & Snowball (10p)│
       │   - Recommender System: Cosine Similarity & Apriori Rules   │
       │   - REST API Service: FastAPI (Chạy cổng :8000)             │
       └──────────────────────────────┬──────────────────────────────┘
                                      │ HTTP / JSON API
       ┌──────────────────────────────┴──────────────────────────────┐
       │     📱 CLIENT: ANDROID NATIVE APP (Môn Lập trình Di động)   │
       │     - Ngôn ngữ: Java / Kotlin (Android Studio)               │
       │     - 4 Trụ cột Android: Activity, Intent, Broadcast, SQLite │
       │     - Thư viện: Retrofit 2 (Gọi API), Glide (Tải ảnh CDN)    │
       │     - Giao diện: RecyclerView, CardView, Animated ProgressBar│
       └─────────────────────────────────────────────────────────────┘
```

---

## 📋 MA TRẬN ĐỐI CHIẾU NỘI DUNG VỚI 2 GIẢNG VIÊN

| Yêu cầu của Môn học | Triển khai trong Dự án | Áp dụng vào Môn Data Science (Cô Hải) | Áp dụng vào Môn Android (Thầy Hiếu) |
| :--- | :--- | :--- | :--- |
| **Nguồn dữ liệu & CSDL** | Riot API + Oracle's Elixir $\rightarrow$ SQLite | Đạt chuẩn 1NF & 3NF, lọc Outlier/Remake, 5 câu truy vấn SQL nâng cao. | Tích hợp Room Database / SQLite lưu các trận đấu yêu thích offline trên máy. |
| **Giao diện & Thành phần** | Android Activity & Layouts | Báo cáo sản phẩm thực tế có giao diện người dùng hoàn chỉnh. | Cấu trúc Project chuẩn (Chương 1), Vòng đời Activity & Intent truyền dữ liệu (Chương 2). |
| **Trực quan hóa & CDN** | Data Dragon CDN (173 Tướng) | Lấy Base stats làm đặc trưng phân cụm K-Means. | Tải ảnh avatar tướng bất đồng bộ bằng Glide vào `RecyclerView`. |
| **Dự đoán Trí tuệ Nhân tạo** | 2-Stage ML (Draft & Snowball) | Đánh giá ROC/AUC, Confusion Matrix, Feature Importance (Chương 4). | Gửi thông số trận đấu sang Backend, nhận xác suất thắng cập nhật lên ProgressBar. |
| **Hệ thống Gợi ý** | Recommender Ban/Pick AI | Thuật toán Khắc chế & Cặp đôi ăn ý (Chương 6). | Màn hình Trợ lý Cấm/Chọn gợi ý trực tiếp cho game thủ lúc đang ban/pick. |

---

## 📅 LỘ TRÌNH THỰC HIỆN CHI TIẾT THEO TỪNG TUẦN

### 🟢 TUẦN 1: NỀN TẢNG DỮ LIỆU & KHỞI TẠO DỰ ÁN ANDROID
> **Mục tiêu:** CSDL SQLite môn Data Science xong khâu cào thô; Project Android Studio được cấu hình chuẩn.

- [ ] **Môn Data Science [Thành viên 1, 2]:**
  - Chạy `crawl_riot_matches.py` cào tối thiểu $1,000$ trận rank Việt Nam (`VN2`) và Hàn Quốc (`KR`).
  - Đảm bảo bảng `matches_10min` đạt chuẩn **1NF & 3NF** (không cột chuỗi gộp, chỉ giữ `server`).
  - Nạp 8,740 trận đấu giải từ `2026_LoL_esports_match_data_from_OraclesElixir.csv` vào CSDL.
- [ ] **Môn Android (Chương 1 Thầy Hiếu) [Thành viên 1]:**
  - Khởi tạo project mới trên **Android Studio** (Package: `vn.ptit.lolaiassistant`, Min SDK: 26 - Android 8.0).
  - Cấu hình file `AndroidManifest.xml`: Cấp quyền `<uses-permission android:name="android.permission.INTERNET" />`.
  - Cấu hình file `build.gradle` (Module: app): Thêm các thư viện thiết yếu:
    ```groovy
    implementation 'com.squareup.retrofit2:retrofit:2.9.0'
    implementation 'com.squareup.retrofit2:converter-gson:2.9.0'
    implementation 'com.github.bumptech.glide:glide:4.16.0'
    implementation 'androidx.recyclerview:recyclerview:1.3.2'
    implementation 'androidx.cardview:cardview:1.0.0'
    ```
  - Thiết kế bảng màu Hextech Dark Theme trong `res/values/colors.xml` (Xanh Hextech `#0AC8B9`, Vàng Kim `#C8AA6E`, Xanh Đậm `#091428`).

---

### 🔵 TUẦN 2: THÀNH PHẦN CƠ BẢN ANDROID & TRỰC QUAN HÓA DATA SCIENCE
> **Mục tiêu:** Xây dựng các Activity cốt lõi và hoàn thành phân tích EDA thống kê.

- [ ] **Môn Data Science [Thành viên 2]:**
  - Viết 5 câu truy vấn SQL nâng cao theo Chương 5 (Kèo đối đầu 1v1, Cặp đôi đường dưới, Subquery).
  - Chạy kiểm định giả thuyết A/B ($Z$-test Phe Xanh, Two-sample $t$-test Snowball $2,000$ vàng).
  - Vẽ bộ 5 biểu đồ EDA 300 DPI xuất bản vào `reports/figures/`.
- [ ] **Môn Android (Chương 2 Thầy Hiếu) [Thành viên 1]:**
  - Xây dựng **Vòng đời Activity (Activity Lifecycle)** chuẩn: Quản lý trạng thái trong `onCreate()`, `onStart()`, `onResume()`, `onPause()`.
  - Thiết kế màn hình chính `MainActivity.java` với thanh điều hướng (BottomNavigationView):
    1. **Tab 1: Danh sách tướng (Champions):** `ChampionListActivity`.
    2. **Tab 2: Phòng Cấm/Chọn (Draft AI):** `DraftPredictActivity`.
    3. **Tab 3: Trợ lý Khắc chế (Counter Pick):** `CounterRecommenderActivity`.
  - **Sử dụng Intent (Explicit Intent):** Bấm vào 1 tướng trong danh sách $\rightarrow$ Chuyển sang `ChampionDetailActivity` truyền dữ liệu tướng qua `intent.putExtra("CHAMPION_NAME", name)`.
  - **BroadcastReceiver:** Tạo `NetworkChangeReceiver` để lắng nghe trạng thái mạng, thông báo Toast khi mất kết nối.

---

### 🟠 TUẦN 3: HUẤN LUYỆN MACHINE LEARNING & DỰNG GIAO DIỆN NÂNG CAO
> **Mục tiêu:** Mô hình AI sẵn sàng; Màn hình Android hiển thị danh sách tướng mượt mà.

- [ ] **Môn Data Science [Thành viên 3]:**
  - Tiền xử lý dữ liệu và huấn luyện **Mô hình Tầng 1 (Draft Prediction lúc 0 phút)**: Logistic Regression / XGBoost (Kỳ vọng: $58 - 62\%$).
  - Huấn luyện **Mô hình Tầng 2 (Snowball Prediction lúc 10 phút)**: Random Forest / Gradient Boosting (Kỳ vọng: $80 - 85\%$).
  - Xây dựng thuật toán Recommender System (Cosine Similarity & Apriori rules).
  - Lưu các mô hình thành file `.pkl`.
- [ ] **Môn Android (Chương 3 & 4) [Thành viên 1]:**
  - Tạo `ChampionAdapter` kế thừa `RecyclerView.Adapter`:
    - Hiển thị danh sách 173 vị tướng dạng lưới (`GridLayoutManager(context, 4)`).
    - Tải ảnh đại diện tướng trực tiếp từ Riot CDN qua URL:
      `https://ddragon.leagueoflegends.com/cdn/16.18.1/img/champion/{name}.png` bằng **Glide**.
  - Thiết kế giao diện phòng Cấm/Chọn `activity_draft_predict.xml`:
    - 5 ô chọn tướng Đội Xanh (bên trái) và 5 ô chọn tướng Đội Đỏ (bên phải).
    - Nút bấm *"DỰ ĐOÁN KẾT QUẢ CẤM/CHỌN"*.
    - Thanh `ProgressBar` tỷ lệ thắng với hiệu ứng đổi màu (Xanh thắng $>50\%$ hiện xanh dương, $<50\%$ hiện đỏ).

---

### 🟣 TUẦN 4: VIẾT FASTAPI KẾT NỐI ANDROID VỚI MACHINE LEARNING
> **Mục tiêu:** Ứng dụng Android gọi API dự đoán thời gian thực từ mô hình Python.

- [ ] **Môn Data Science & Backend [Thành viên 1 + 3]:**
  - Viết file `src/api/app.py` sử dụng **FastAPI**:
    ```python
    @app.post("/api/predict/draft")
    def predict_draft(data: DraftRequest):
        # Nhận 10 tướng từ Android -> chạy mô hình -> trả về % thắng
        prob = draft_model.predict_proba([vector])[0][1]
        return {"blue_win_prob": round(float(prob), 4)}

    @app.get("/api/recommend/counter")
    def recommend_counter(enemy_mid: str):
        # Gợi ý top 3 tướng khắc chế
        return {"counters": recommender.get_counters(enemy_mid)}
    ```
  - Dựng Web Dashboard **Streamlit** (`src/web_dashboard/app.py`) để chiếu slide thuyết trình bảo vệ trước lớp.
- [ ] **Môn Android [Thành viên 1]:**
  - Khởi tạo `ApiService` interface bằng **Retrofit 2**:
    ```java
    public interface ApiService {
        @POST("api/predict/draft")
        Call<PredictResponse> predictDraft(@Body DraftRequest request);

        @GET("api/recommend/counter")
        Call<CounterResponse> getCounters(@Query("enemy_mid") String enemyMid);
    }
    ```
  - Khi người dùng bấm nút *"Dự đoán"* trên điện thoại:
    - Hiển thị `ProgressDialog` đang phân tích.
    - Gọi API bất đồng bộ (Enqueue Callback).
    - Cập nhật số liệu tỷ lệ thắng lên màn hình điện thoại mượt mà không bị đơ UI.

---

### 🔴 TUẦN 5: TỔNG DUYỆT, BÁO CÁO & BẢO VỆ CẢ 2 MÔN HỌC
> **Mục tiêu:** Nộp sản phẩm đạt điểm tối đa ở cả 2 hội đồng thi.

- [ ] **Môn 1: Nhập môn Khoa học Dữ liệu (TS. Thái Tuyết Hải):**
  - Hoàn thiện file Báo cáo tổng thể Word/PDF 6 chương giáo trình.
  - Slide PowerPoint 20–25 trang tập trung vào: *Pipeline cào Riot API, CSDL chuẩn 1NF/3NF, Biểu đồ EDA, Kiểm định A/B, Kết quả Machine Learning*.
  - Kịch bản Demo: Chiếu Web Streamlit trên máy tính $\rightarrow$ Mời thầy cô chọn 10 tướng để xem AI dự đoán.
- [ ] **Môn 2: Lập trình Thiết bị Di động (ThS. Nguyễn Trung Hiếu):**
  - Đóng gói file `.apk` cài đặt trực tiếp lên điện thoại hoặc chạy trên Android Emulator.
  - Viết Báo cáo thiết kế ứng dụng Android: Cấu trúc Project (Chương 1), Vòng đời Activity & Intent (Chương 2), Xử lý luồng mạng với Retrofit (Chương 6).
  - Trình chiếu demo: Cầm điện thoại thao tác chọn tướng trực tiếp trước mặt thầy, giao diện mượt mà, phản hồi API trong 0.2 giây!

---

## 🏆 KỊCH BẢN THUYẾT TRÌNH DEMO "ĐIỂM 10 TUYỆT ĐỐI"

Khi bảo vệ trước hội đồng, nhóm bạn thực hiện kịch bản sau:
1. **Bước 1:** Trưởng nhóm chiếu Slide và mở **Web Streamlit** trên máy tính giảng đường để trình bày các biểu đồ EDA và công thức toán học Machine Learning (Thỏa mãn tiêu chí học thuật của môn Data Science).
2. **Bước 2:** Cầm chiếc điện thoại Android lên và nói:
   > *"Thưa thầy cô, nhóm em không chỉ dừng lại ở lý thuyết trên máy tính, mà nhóm đã đóng gói toàn bộ mô hình AI này thành một Ứng dụng Di động hoàn chỉnh mang tên **LoL Hextech AI Assistant** để các tuyển thủ và game thủ có thể sử dụng ngay trên điện thoại khi thi đấu!"*
3. **Bước 3:** Bấm nút trên điện thoại $\rightarrow$ Cả ứng dụng di động và hệ thống máy chủ cùng phản hồi kết quả trực quan!
   $\rightarrow$ **Kết quả: Cả 2 giảng viên của 2 môn đều sẽ cho điểm tối đa vì sản phẩm quá hoàn thiện và mang tính thực tế vượt trội!**
