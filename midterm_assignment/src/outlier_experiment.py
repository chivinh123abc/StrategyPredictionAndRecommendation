import os
import sys
from pathlib import Path
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.ensemble import IsolationForest

# Cấu hình font và độ phân giải biểu đồ
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 300

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
EXP_DIR = PROJECT_ROOT / "midterm_assignment"
DATA_DIR = EXP_DIR / "data"
FIG_DIR = EXP_DIR / "figures"
REPORT_DIR = EXP_DIR / "report"
SLIDES_DIR = EXP_DIR / "slides"

for d in [DATA_DIR, FIG_DIR, REPORT_DIR, SLIDES_DIR]:
    d.mkdir(parents=True, exist_ok=True)

def run_outlier_experiment():
    print("=" * 80)
    print("THÍ NGHIỆM GIỮA KỲ: PHÁT HIỆN & XỬ LÝ NGOẠI LAI (TOPIC 2 - OUTLIER DETECTION)")
    print("Dữ liệu: Chênh lệch Vàng & Kinh nghiệm Phút 10 trong Đấu Giải Chuyên Nghiệp LMHT 2026")
    print("=" * 80)

    # 1. Trích xuất dữ liệu thực tế từ CSDL
    db_path = PROJECT_ROOT / "data" / "database" / "lol_live_data.db"
    clean_tour_csv = PROJECT_ROOT / "data" / "processed" / "clean_tournament_10min.csv"
    if clean_tour_csv.exists():
        df_full = pd.read_csv(clean_tour_csv)
        # Lấy quan sát bên Blue để đảm bảo mỗi trận là 1 quan sát độc lập (không bị duplicate lật dấu -Red)
        if 'side' in df_full.columns:
            df = df_full[df_full['side'] == 'Blue'].copy()
        else:
            df = df_full.copy()
        data_source_name = f"Đấu Giải Chuyên Nghiệp LMHT 2026 (Pro Play - LCK, LPL, LCP, EWC, MSI - {len(df):,} ván)"
    else:
        # Fallback query từ SQLite nếu cần
        conn = sqlite3.connect(db_path)
        query = "SELECT * FROM matches_10min LIMIT 1000"
        df = pd.read_sql(query, conn)
        conn.close()
        data_source_name = f"Dữ liệu mẫu LMHT ({len(df):,} ván)"

    # Đảm bảo các cột cần thiết có tồn tại
    if 'killsat10' in df.columns and 'opp_killsat10' in df.columns and 'killdiffat10' not in df.columns:
        df['killdiffat10'] = df['killsat10'] - df['opp_killsat10']

    # Lọc bỏ missing values trên các biến trọng tâm để đồng bộ cỡ mẫu
    df = df.dropna(subset=['golddiffat10', 'xpdiffat10']).copy()

    # Lưu tập dữ liệu phục vụ riêng cho bài tập giữa kỳ
    dataset_csv_path = DATA_DIR / "outlier_experiment_data.csv"
    df.to_csv(dataset_csv_path, index=False)
    print(f"✅ Đã trích xuất {len(df):,} bản ghi từ {data_source_name} -> {dataset_csv_path.name}")

    # Biến số trọng tâm nghiên cứu: golddiffat10
    col = 'golddiffat10'
    data_raw = df[col].values

    # 2. Thống kê mô tả ban đầu (Descriptive Statistics)
    n_total = len(data_raw)
    mean_raw = float(np.mean(data_raw))
    median_raw = float(np.median(data_raw))
    std_raw = float(np.std(data_raw, ddof=1))
    skew_raw = float(stats.skew(data_raw))
    kurt_raw = float(stats.kurtosis(data_raw))
    min_raw = float(np.min(data_raw))
    max_raw = float(np.max(data_raw))

    print("\n--- 1. THỐNG KÊ MÔ TẢ TẬP DỮ LIỆU GỐC ---")
    print(f"Số lượng mẫu (N): {n_total:,}")
    print(f"Mean (Trung bình): {mean_raw:+.2f} vàng")
    print(f"Median (Trung vị): {median_raw:+.2f} vàng")
    print(f"Std Dev (Độ lệch chuẩn): {std_raw:.2f} vàng")
    print(f"Khoảng giá trị: [{min_raw:+.0f}, {max_raw:+.0f}] vàng")
    print(f"Skewness (Độ lệch): {skew_raw:.4f}")
    print(f"Kurtosis (Độ nhọn): {kurt_raw:.4f}")

    # 3. Phương pháp 1: Interquartile Range (IQR)
    q1 = float(np.percentile(data_raw, 25))
    q3 = float(np.percentile(data_raw, 75))
    iqr_val = q3 - q1
    iqr_lower = q1 - 1.5 * iqr_val
    iqr_upper = q3 + 1.5 * iqr_val

    iqr_outliers_mask = (data_raw < iqr_lower) | (data_raw > iqr_upper)
    iqr_outliers_count = int(np.sum(iqr_outliers_mask))
    iqr_outliers_pct = (iqr_outliers_count / n_total) * 100

    print("\n--- 2. KẾT QUẢ PHÁT HIỆN THEO IQR (1.5 x IQR) ---")
    print(f"Q1 (25th): {q1:+.1f} | Q3 (75th): {q3:+.1f} | IQR: {iqr_val:.1f}")
    print(f"Ngưỡng an toàn: [{iqr_lower:+.1f}, {iqr_upper:+.1f}]")
    print(f"Số điểm ngoại lai phát hiện: {iqr_outliers_count:,} ({iqr_outliers_pct:.2f}%)")

    # 4. Phương pháp 2: Z-Score (|Z| > 3.0)
    z_scores = np.abs(stats.zscore(data_raw))
    z_threshold = 3.0
    z_outliers_mask = z_scores > z_threshold
    z_outliers_count = int(np.sum(z_outliers_mask))
    z_outliers_pct = (z_outliers_count / n_total) * 100
    z_lower = mean_raw - 3.0 * std_raw
    z_upper = mean_raw + 3.0 * std_raw

    print("\n--- 3. KẾT QUẢ PHÁT HIỆN THEO Z-SCORE (|Z| > 3.0) ---")
    print(f"Ngưỡng Z-Score (|Z| <= 3.0): [{z_lower:+.1f}, {z_upper:+.1f}]")
    print(f"Số điểm ngoại lai phát hiện: {z_outliers_count:,} ({z_outliers_pct:.2f}%)")

    # 5. Phương pháp 3 (Nâng cao): Isolation Forest
    iso_forest = IsolationForest(contamination=0.03, random_state=42)
    iso_preds = iso_forest.fit_predict(data_raw.reshape(-1, 1))
    iso_outliers_mask = (iso_preds == -1)
    iso_outliers_count = int(np.sum(iso_outliers_mask))
    iso_outliers_pct = (iso_outliers_count / n_total) * 100

    print("\n--- 4. KẾT QUẢ PHÁT HIỆN THEO ISOLATION FOREST ---")
    print(f"Số điểm ngoại lai phát hiện: {iso_outliers_count:,} ({iso_outliers_pct:.2f}%)")

    # Giao thoa giữa IQR và Z-Score
    overlap_both = np.sum(iqr_outliers_mask & z_outliers_mask)
    iqr_only = np.sum(iqr_outliers_mask & (~z_outliers_mask))
    z_only = np.sum((~iqr_outliers_mask) & z_outliers_mask)

    print("\n--- 5. SO SÁNH ĐỐI CHIẾU SỰ KHÁC BIỆT ---")
    print(f"Số điểm cả 2 phương pháp cùng gắn cờ: {overlap_both:,}")
    print(f"Số điểm chỉ IQR gắn cờ (Z-Score bỏ sót): {iqr_only:,}")
    print(f"Số điểm chỉ Z-Score gắn cờ: {z_only:,}")

    # 6. Khảo sát các Chiến lược Xử lý (Handling Strategies)
    # A. Trimming (Xóa bỏ ngoại lai theo IQR)
    data_trimmed_iqr = data_raw[~iqr_outliers_mask]
    mean_trimmed_iqr = float(np.mean(data_trimmed_iqr))
    std_trimmed_iqr = float(np.std(data_trimmed_iqr, ddof=1))
    skew_trimmed_iqr = float(stats.skew(data_trimmed_iqr))

    # B. Trimming (Xóa bỏ ngoại lai theo Z-Score)
    data_trimmed_z = data_raw[~z_outliers_mask]
    mean_trimmed_z = float(np.mean(data_trimmed_z))
    std_trimmed_z = float(np.std(data_trimmed_z, ddof=1))
    skew_trimmed_z = float(stats.skew(data_trimmed_z))

    # C. Winsorization (Cắt ngọn / Capping tại ngưỡng 1% và 99%)
    p01 = float(np.percentile(data_raw, 1))
    p99 = float(np.percentile(data_raw, 99))
    data_winsorized = np.clip(data_raw, p01, p99)
    mean_winsorized = float(np.mean(data_winsorized))
    std_winsorized = float(np.std(data_winsorized, ddof=1))
    skew_winsorized = float(stats.skew(data_winsorized))

    # Bảng tổng hợp so sánh tác động thống kê
    summary_metrics = pd.DataFrame([
        {
            'Chiến lược': 'Gốc (Raw Data / Retaining)',
            'Cỡ mẫu (N)': len(data_raw),
            'Tỷ lệ giữ lại (%)': 100.0,
            'Mean (Trung bình)': round(mean_raw, 2),
            'Std (Độ lệch chuẩn)': round(std_raw, 2),
            'Δ Std so với gốc (%)': 0.0,
            'Skewness': round(skew_raw, 4),
            'Min': round(min_raw, 0),
            'Max': round(max_raw, 0)
        },
        {
            'Chiến lược': 'Loại bỏ (Trimming theo IQR)',
            'Cỡ mẫu (N)': len(data_trimmed_iqr),
            'Tỷ lệ giữ lại (%)': round(len(data_trimmed_iqr) / n_total * 100, 2),
            'Mean (Trung bình)': round(mean_trimmed_iqr, 2),
            'Std (Độ lệch chuẩn)': round(std_trimmed_iqr, 2),
            'Δ Std so với gốc (%)': round((std_trimmed_iqr - std_raw) / std_raw * 100, 2),
            'Skewness': round(skew_trimmed_iqr, 4),
            'Min': round(float(np.min(data_trimmed_iqr)), 0),
            'Max': round(float(np.max(data_trimmed_iqr)), 0)
        },
        {
            'Chiến lược': 'Loại bỏ (Trimming theo Z-Score)',
            'Cỡ mẫu (N)': len(data_trimmed_z),
            'Tỷ lệ giữ lại (%)': round(len(data_trimmed_z) / n_total * 100, 2),
            'Mean (Trung bình)': round(mean_trimmed_z, 2),
            'Std (Độ lệch chuẩn)': round(std_trimmed_z, 2),
            'Δ Std so với gốc (%)': round((std_trimmed_z - std_raw) / std_raw * 100, 2),
            'Skewness': round(skew_trimmed_z, 4),
            'Min': round(float(np.min(data_trimmed_z)), 0),
            'Max': round(float(np.max(data_trimmed_z)), 0)
        },
        {
            'Chiến lược': 'Cắt ngọn (Winsorization 1%-99%)',
            'Cỡ mẫu (N)': len(data_winsorized),
            'Tỷ lệ giữ lại (%)': 100.0,
            'Mean (Trung bình)': round(mean_winsorized, 2),
            'Std (Độ lệch chuẩn)': round(std_winsorized, 2),
            'Δ Std so với gốc (%)': round((std_winsorized - std_raw) / std_raw * 100, 2),
            'Skewness': round(skew_winsorized, 4),
            'Min': round(p01, 0),
            'Max': round(p99, 0)
        }
    ])

    summary_metrics_path = DATA_DIR / "outlier_comparison_summary.csv"
    summary_metrics.to_csv(summary_metrics_path, index=False)
    print("\n--- 6. BẢNG TỔNG HỢP TÁC ĐỘNG LÊN THƯỚC ĐO THỐNG KÊ ---")
    print(summary_metrics.to_string(index=False))

    # 7. VẼ BỘ 4 BIỂU ĐỒ MINH HỌA HỌC THUẬT (300 DPI)
    print("\n--- 7. XUẤT BẢN BỘ BIỂU ĐỒ 300 DPI ---")

    # FIG 1: Boxplot & Phát hiện Ngoại lai của IQR và Z-Score
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Subplot 1: Boxplot với ngưỡng IQR
    sns.boxplot(y=data_raw, ax=ax1, color='#6baed6', width=0.35, flierprops={'marker': 'o', 'markersize': 5, 'markerfacecolor': '#de2d26', 'alpha': 0.6})
    ax1.axhline(iqr_upper, color='#e6550d', linestyle='--', linewidth=1.5, label=f'Upper Fence ({iqr_upper:+.0f}g)')
    ax1.axhline(iqr_lower, color='#e6550d', linestyle='--', linewidth=1.5, label=f'Lower Fence ({iqr_lower:+.0f}g)')
    ax1.set_title("A. Phương pháp IQR (1.5 x IQR Rule)", fontsize=13, fontweight='bold')
    ax1.set_ylabel("Chênh lệch Vàng Phút 10 (golddiffat10)", fontsize=11)
    ax1.legend(loc='upper right')
    ax1.grid(axis='y', linestyle=':', alpha=0.6)

    # Subplot 2: Z-Score Plot
    sorted_idx = np.argsort(data_raw)
    sorted_data = data_raw[sorted_idx]
    sorted_z = z_scores[sorted_idx]
    outlier_colors = ['#de2d26' if z > 3.0 else '#3182bd' for z in sorted_z]
    
    ax2.scatter(range(len(sorted_data)), sorted_data, c=outlier_colors, alpha=0.6, s=15)
    ax2.axhline(z_upper, color='#de2d26', linestyle='--', linewidth=1.5, label=f'Z = +3.0 ({z_upper:+.0f}g)')
    ax2.axhline(z_lower, color='#de2d26', linestyle='--', linewidth=1.5, label=f'Z = -3.0 ({z_lower:+.0f}g)')
    ax2.axhline(mean_raw, color='black', linestyle='-', linewidth=1.2, label=f'Mean ({mean_raw:+.0f}g)')
    ax2.set_title("B. Phương pháp Z-Score (|Z| > 3.0 Rule)", fontsize=13, fontweight='bold')
    ax2.set_xlabel("Thứ tự Mẫu sắp xếp theo Giá trị", fontsize=11)
    ax2.legend(loc='upper left')
    ax2.grid(axis='y', linestyle=':', alpha=0.6)

    plt.tight_layout()
    fig1_path = FIG_DIR / "fig1_outlier_detection_iqr_zscore.png"
    plt.savefig(fig1_path, dpi=300)
    plt.close()
    print(f"📸 Đã lưu: {fig1_path.name}")

    # FIG 2: Histogram & Phân phối trước vs sau xử lý
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    # Gốc
    sns.histplot(data_raw, kde=True, ax=axes[0], color='#3182bd', bins=40)
    axes[0].set_title(f"A. Dữ liệu Gốc (N={len(data_raw):,})\nStd = {std_raw:.1f} | Skew = {skew_raw:.2f}", fontsize=12, fontweight='bold')
    axes[0].set_xlabel("golddiffat10")
    axes[0].grid(axis='y', linestyle=':', alpha=0.6)

    # Trimming IQR
    sns.histplot(data_trimmed_iqr, kde=True, ax=axes[1], color='#e6550d', bins=40)
    axes[1].set_title(f"B. Sau khi Trimming IQR (N={len(data_trimmed_iqr):,})\nStd = {std_trimmed_iqr:.1f} (Giảm {abs((std_trimmed_iqr-std_raw)/std_raw*100):.1f}%)", fontsize=12, fontweight='bold')
    axes[1].set_xlabel("golddiffat10")
    axes[1].grid(axis='y', linestyle=':', alpha=0.6)

    # Winsorization
    sns.histplot(data_winsorized, kde=True, ax=axes[2], color='#31a354', bins=40)
    axes[2].set_title(f"C. Sau khi Winsorization 1%-99% (N={len(data_winsorized):,})\nStd = {std_winsorized:.1f} (Bảo tồn 100% mẫu)", fontsize=12, fontweight='bold')
    axes[2].set_xlabel("golddiffat10")
    axes[2].grid(axis='y', linestyle=':', alpha=0.6)

    plt.tight_layout()
    fig2_path = FIG_DIR / "fig2_distribution_before_after.png"
    plt.savefig(fig2_path, dpi=300)
    plt.close()
    print(f"📸 Đã lưu: {fig2_path.name}")

    # FIG 3: Scatter Plot 2D (Gold Diff vs XP Diff) và Sự Đồng Thuận Của Các Phương Pháp
    fig, ax = plt.subplots(figsize=(10, 7))
    xp_data = df['xpdiffat10'].values

    # Phân loại trạng thái nhãn
    category = []
    for i in range(len(data_raw)):
        is_iqr = iqr_outliers_mask[i]
        is_z = z_outliers_mask[i]
        is_iso = iso_outliers_mask[i]
        if is_iqr and is_z:
            category.append('Both IQR & Z-Score')
        elif is_iqr:
            category.append('Only IQR')
        elif is_z:
            category.append('Only Z-Score')
        elif is_iso:
            category.append('Only Isolation Forest')
        else:
            category.append('Inlier (Bình thường)')
    
    color_map = {
        'Inlier (Bình thường)': '#9ecae1',
        'Both IQR & Z-Score': '#de2d26',
        'Only IQR': '#f16913',
        'Only Z-Score': '#756bb1',
        'Only Isolation Forest': '#31a354'
    }

    for cat_name, c_color in color_map.items():
        cat_mask = [c == cat_name for c in category]
        ax.scatter(data_raw[cat_mask], xp_data[cat_mask], label=f"{cat_name} ({np.sum(cat_mask):,})", color=c_color, alpha=0.7 if cat_name != 'Inlier (Bình thường)' else 0.25, s=25 if cat_name != 'Inlier (Bình thường)' else 12)

    ax.set_title("Tương quan 2D: Chênh lệch Vàng vs Kinh nghiệm và Nhãn Ngoại lai", fontsize=13, fontweight='bold')
    ax.set_xlabel("Chênh lệch Vàng Phút 10 (golddiffat10)", fontsize=11)
    ax.set_ylabel("Chênh lệch Kinh nghiệm Phút 10 (xpdiffat10)", fontsize=11)
    ax.axvline(0, color='grey', linestyle=':', alpha=0.7)
    ax.axhline(0, color='grey', linestyle=':', alpha=0.7)
    ax.legend(loc='lower right', frameon=True)
    ax.grid(linestyle=':', alpha=0.6)

    plt.tight_layout()
    fig3_path = FIG_DIR / "fig3_scatter_multivariate_outliers.png"
    plt.savefig(fig3_path, dpi=300)
    plt.close()
    print(f"📸 Đã lưu: {fig3_path.name}")

    # FIG 4: Biểu đồ cột Tác động lên Độ lệch chuẩn và Thước đo Thống kê
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    strategies = ['Gốc', 'Trimming IQR', 'Trimming Z-Score', 'Winsorization']
    stds = [std_raw, std_trimmed_iqr, std_trimmed_z, std_winsorized]
    skews = [skew_raw, skew_trimmed_iqr, skew_trimmed_z, skew_winsorized]

    bars1 = ax1.bar(strategies, stds, color=['#3182bd', '#e6550d', '#756bb1', '#31a354'], alpha=0.85, width=0.5)
    ax1.set_title("Tác động lên Độ lệch chuẩn (Standard Deviation)", fontsize=12, fontweight='bold')
    ax1.set_ylabel("Giá trị Độ lệch chuẩn (Vàng)", fontsize=11)
    for bar in bars1:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2.0, yval + 15, f"{yval:.1f}", ha='center', va='bottom', fontweight='bold')
    ax1.set_ylim(0, max(stds) * 1.15)
    ax1.grid(axis='y', linestyle=':', alpha=0.6)

    bars2 = ax2.bar(strategies, skews, color=['#3182bd', '#e6550d', '#756bb1', '#31a354'], alpha=0.85, width=0.5)
    ax2.set_title("Tác động lên Độ lệch (Skewness)", fontsize=12, fontweight='bold')
    ax2.set_ylabel("Hệ số Skewness", fontsize=11)
    for bar in bars2:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2.0, yval + (0.01 if yval >= 0 else -0.03), f"{yval:.3f}", ha='center', va='bottom', fontweight='bold')
    ax2.grid(axis='y', linestyle=':', alpha=0.6)

    plt.tight_layout()
    fig4_path = FIG_DIR / "fig4_statistical_impact_comparison.png"
    plt.savefig(fig4_path, dpi=300)
    plt.close()
    print(f"📸 Đã lưu: {fig4_path.name}")

    print("\n🎉 HOÀN TẤT THÍ NGHIỆM OUTLIER DETECTION!")
    return summary_metrics

if __name__ == '__main__':
    run_outlier_experiment()
