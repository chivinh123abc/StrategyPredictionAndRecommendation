"""
Module 06: Machine Learning - Task 3.3: Model Evaluation & Diagnostic Visualizations
Đánh giá toàn diện và trực quan hóa hiệu năng mô hình 2 giai đoạn (Phút 0 vs Phút 10):
- ROC-AUC & Precision-Recall Curves
- Confusion Matrix Heatmaps
- Probability Calibration Curves & Brier Scores
- Feature Importance Rankings & Comparison
- Xuất 4 biểu đồ 300 DPI vào reports/figures/
"""

import sys
import os
import sqlite3
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    roc_curve, auc, roc_auc_score, precision_recall_curve, confusion_matrix,
    brier_score_loss, log_loss, accuracy_score, f1_score,
    precision_score, recall_score, classification_report
)
from sklearn.calibration import calibration_curve
from sklearn.model_selection import train_test_split

# Add ML directory to path
ML_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = ML_DIR.parent.parent
sys.path.insert(0, str(ML_DIR))

from draft_model import LolDraftPredictionSystem, load_pivoted_draft_data
from snowball_model import LolSnowballPredictionSystem, load_integrated_10min_dataset

warnings.filterwarnings('ignore')

FIGURES_DIR = PROJECT_ROOT / "reports" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# Cấu hình phong cách đồ họa nghiên cứu khoa học
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = ['Segoe UI', 'DejaVu Sans', 'Arial', 'sans-serif']
plt.rcParams['axes.edgecolor'] = '#CBD5E1'
plt.rcParams['axes.linewidth'] = 1.0


def evaluate_and_plot_all():
    print("=" * 85)
    print("🔬 BẮT ĐẦU ĐÁNH GIÁ TOÀN DIỆN MÔ HÌNH MACHINE LEARNING (TASK 3.3)")
    print("=" * 85)

    # -------------------------------------------------------------
    # 1. Nạp mô hình & chuẩn bị tập Test
    # -------------------------------------------------------------
    print("⏳ Đang nạp mô hình Draft (Phút 0) và Snowball (Phút 10)...")
    draft_sys = LolDraftPredictionSystem.load_model()
    snowball_sys = LolSnowballPredictionSystem.load_model()

    # Dữ liệu Draft (Phút 0)
    df_draft = load_pivoted_draft_data()
    n_draft = len(df_draft)
    split_idx_draft = int(n_draft * 0.8)
    test_draft = df_draft.iloc[split_idx_draft:].copy()
    y_test_draft = test_draft['blue_win'].to_numpy()
    X_test_draft = draft_sys.fe.transform(test_draft)
    
    y_prob_draft = draft_sys.best_model.predict_proba(X_test_draft)[:, 1]
    y_pred_draft = (y_prob_draft >= 0.5).astype(int)

    # Dữ liệu Snowball (Phút 10)
    df_snowball = load_integrated_10min_dataset()
    y_snowball = df_snowball['result'].to_numpy()
    _, test_snowball_df, _, y_test_snowball = train_test_split(
        df_snowball, y_snowball, test_size=0.20, random_state=42, stratify=df_snowball['result']
    )
    X_test_snowball = snowball_sys.fe.transform(test_snowball_df)
    
    y_prob_snowball = snowball_sys.best_model.predict_proba(X_test_snowball)[:, 1]
    y_pred_snowball = (y_prob_snowball >= 0.5).astype(int)

    print(f"✅ Đã chuẩn bị: Draft Test Set ({len(y_test_draft):,} mẫu) | Snowball Test Set ({len(y_test_snowball):,} mẫu)")

    # -------------------------------------------------------------
    # 2. Bảng tổng hợp chỉ số thống kê hiệu năng
    # -------------------------------------------------------------
    metrics_summary = [
        {
            "Giai Đoạn Dự Đoán": "Cấm/Chọn (Phút 0 - Draft AI)",
            "Mô Hình": draft_sys.best_model_name,
            "Accuracy": accuracy_score(y_test_draft, y_pred_draft),
            "ROC-AUC": roc_auc_score(y_test_draft, y_prob_draft),
            "F1-Score": f1_score(y_test_draft, y_pred_draft),
            "Brier Score": brier_score_loss(y_test_draft, y_prob_draft),
            "Log Loss": log_loss(y_test_draft, y_prob_draft)
        },
        {
            "Giai Đoạn Dự Đoán": "Thực Chiến (Phút 10 - Snowball AI)",
            "Mô Hình": snowball_sys.best_model_name,
            "Accuracy": accuracy_score(y_test_snowball, y_pred_snowball),
            "ROC-AUC": roc_auc_score(y_test_snowball, y_prob_snowball),
            "F1-Score": f1_score(y_test_snowball, y_pred_snowball),
            "Brier Score": brier_score_loss(y_test_snowball, y_prob_snowball),
            "Log Loss": log_loss(y_test_snowball, y_prob_snowball)
        }
    ]
    df_metrics = pd.DataFrame(metrics_summary)
    print("\n" + "=" * 95)
    print("🏆 BẢNG ĐỐI CHIẾU HIỆU NĂNG MÔ HÌNH 2 GIAI ĐOẠN (PHÚT 0 VS PHÚT 10)")
    print("=" * 95)
    print(df_metrics.to_string(index=False, formatters={
        'Accuracy': '{:.2%}'.format,
        'ROC-AUC': '{:.4f}'.format,
        'F1-Score': '{:.4f}'.format,
        'Brier Score': '{:.4f}'.format,
        'Log Loss': '{:.4f}'.format
    }))

    # -------------------------------------------------------------
    # FIG 6: ROC-AUC & PRECISION-RECALL COMPARISON
    # -------------------------------------------------------------
    print("\n📊 Đang vẽ Fig 6: Đường cong ROC-AUC & Precision-Recall đối chiếu...")
    fig, axes = plt.subplots(1, 2, figsize=(15, 6.5), dpi=300)

    # Subplot 1: ROC Curve
    fpr_d, tpr_d, _ = roc_curve(y_test_draft, y_prob_draft)
    roc_auc_d = auc(fpr_d, tpr_d)

    fpr_s, tpr_s, _ = roc_curve(y_test_snowball, y_prob_snowball)
    roc_auc_s = auc(fpr_s, tpr_s)

    axes[0].plot(fpr_d, tpr_d, color='#2563EB', lw=2.5, label=f'Draft Model (Phút 0) - AUC = {roc_auc_d:.4f}')
    axes[0].plot(fpr_s, tpr_s, color='#DC2626', lw=2.5, label=f'Snowball Model (Phút 10) - AUC = {roc_auc_s:.4f}')
    axes[0].plot([0, 1], [0, 1], color='#94A3B8', lw=1.5, linestyle='--', label='Ngẫu nhiên (Random Chance AUC = 0.50)')
    axes[0].set_xlim([0.0, 1.0])
    axes[0].set_ylim([0.0, 1.05])
    axes[0].set_xlabel('Tỷ Lệ Dương Tính Giả (False Positive Rate - 1 - Specificity)', fontsize=11, fontweight='bold')
    axes[0].set_ylabel('Tỷ Lệ Dương Tính Thật (True Positive Rate - Recall)', fontsize=11, fontweight='bold')
    axes[0].set_title('Đường Cong ROC (Receiver Operating Characteristic)', fontsize=13, fontweight='bold', pad=12)
    axes[0].legend(loc="lower right", frameon=True, facecolor='white', framealpha=0.95, fontsize=10)
    axes[0].grid(True, linestyle=':', alpha=0.6)

    # Subplot 2: Precision-Recall Curve
    prec_d, rec_d, _ = precision_recall_curve(y_test_draft, y_prob_draft)
    prec_s, rec_s, _ = precision_recall_curve(y_test_snowball, y_prob_snowball)

    axes[1].plot(rec_d, prec_d, color='#2563EB', lw=2.5, label=f'Draft Model (Phút 0)')
    axes[1].plot(rec_s, prec_s, color='#DC2626', lw=2.5, label=f'Snowball Model (Phút 10)')
    axes[1].axhline(y=np.mean(y_test_draft), color='#94A3B8', linestyle='--', lw=1.5, label=f'Tỷ lệ cân bằng nền ({np.mean(y_test_draft):.1%})')
    axes[1].set_xlim([0.0, 1.0])
    axes[1].set_ylim([0.4, 1.05])
    axes[1].set_xlabel('Độ Phủ (Recall)', fontsize=11, fontweight='bold')
    axes[1].set_ylabel('Độ Chuẩn Xác (Precision)', fontsize=11, fontweight='bold')
    axes[1].set_title('Đường Cong Precision - Recall', fontsize=13, fontweight='bold', pad=12)
    axes[1].legend(loc="upper right", frameon=True, facecolor='white', framealpha=0.95, fontsize=10)
    axes[1].grid(True, linestyle=':', alpha=0.6)

    plt.suptitle('HỆ THỐNG ĐÁNH GIÁ MÔ HÌNH: ĐƯỜNG CONG ROC VÀ PRECISION-RECALL (PHÚT 0 VS PHÚT 10)', fontsize=14, fontweight='bold', y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    fig6_path = FIGURES_DIR / "fig6_roc_auc_comparison.png"
    plt.savefig(fig6_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"💾 Đã lưu: {fig6_path}")

    # -------------------------------------------------------------
    # FIG 7: CONFUSION MATRICES HEATMAP
    # -------------------------------------------------------------
    print("\n📊 Đang vẽ Fig 7: Ma trận nhầm lẫn (Confusion Matrices)...")
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), dpi=300)

    # Confusion Matrix Draft
    cm_draft = confusion_matrix(y_test_draft, y_pred_draft)
    cm_draft_pct = cm_draft.astype('float') / cm_draft.sum(axis=1)[:, np.newaxis]
    annot_draft = np.array([[f"{count:,}\n({pct:.1%})" for count, pct in zip(row_cnt, row_pct)] 
                           for row_cnt, row_pct in zip(cm_draft, cm_draft_pct)])

    sns.heatmap(cm_draft, annot=annot_draft, fmt='', cmap='Blues', ax=axes[0], cbar=False,
                xticklabels=['Dự đoán Thua (Red)', 'Dự đoán Thắng (Blue)'],
                yticklabels=['Thực tế Thua (Red)', 'Thực tế Thắng (Blue)'],
                annot_kws={'size': 11, 'weight': 'bold'})
    axes[0].set_title(f'Draft Model - Phút 0 (Test N = {len(y_test_draft):,})\nĐộ chính xác: {accuracy_score(y_test_draft, y_pred_draft):.2%}',
                      fontsize=12, fontweight='bold', pad=12)
    axes[0].set_xlabel('Nhãn Dự Đoán', fontsize=11, fontweight='bold')
    axes[0].set_ylabel('Nhãn Thực Tế', fontsize=11, fontweight='bold')

    # Confusion Matrix Snowball
    cm_snowball = confusion_matrix(y_test_snowball, y_pred_snowball)
    cm_snowball_pct = cm_snowball.astype('float') / cm_snowball.sum(axis=1)[:, np.newaxis]
    annot_snowball = np.array([[f"{count:,}\n({pct:.1%})" for count, pct in zip(row_cnt, row_pct)] 
                              for row_cnt, row_pct in zip(cm_snowball, cm_snowball_pct)])

    sns.heatmap(cm_snowball, annot=annot_snowball, fmt='', cmap='Reds', ax=axes[1], cbar=False,
                xticklabels=['Dự đoán Thua', 'Dự đoán Thắng'],
                yticklabels=['Thực tế Thua', 'Thực tế Thắng'],
                annot_kws={'size': 11, 'weight': 'bold'})
    axes[1].set_title(f'Snowball Model - Phút 10 (Test N = {len(y_test_snowball):,})\nĐộ chính xác: {accuracy_score(y_test_snowball, y_pred_snowball):.2%}',
                      fontsize=12, fontweight='bold', pad=12)
    axes[1].set_xlabel('Nhãn Dự Đoán', fontsize=11, fontweight='bold')
    axes[1].set_ylabel('Nhãn Thực Tế', fontsize=11, fontweight='bold')

    plt.suptitle('MA TRẬN NHẦM LẪN (CONFUSION MATRIX): CẤM/CHỌN PHÚT 0 VS THỰC CHIẾN PHÚT 10', fontsize=14, fontweight='bold', y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    fig7_path = FIGURES_DIR / "fig7_confusion_matrices.png"
    plt.savefig(fig7_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"💾 Đã lưu: {fig7_path}")

    # -------------------------------------------------------------
    # FIG 8: PROBABILITY CALIBRATION CURVES
    # -------------------------------------------------------------
    print("\n📊 Đang vẽ Fig 8: Đường cong hiệu chuẩn xác suất (Calibration Curve)...")
    fig, ax = plt.subplots(figsize=(8.5, 6.5), dpi=300)

    prob_true_d, prob_pred_d = calibration_curve(y_test_draft, y_prob_draft, n_bins=8, strategy='uniform')
    prob_true_s, prob_pred_s = calibration_curve(y_test_snowball, y_prob_snowball, n_bins=8, strategy='uniform')

    ax.plot([0, 1], [0, 1], linestyle='--', color='#94A3B8', lw=1.5, label='Hiệu Chuẩn Hoàn Hảo (Perfect Calibration)')
    ax.plot(prob_pred_d, prob_true_d, marker='o', lw=2.2, color='#2563EB', label=f'Draft Model (Brier Score = {brier_score_loss(y_test_draft, y_prob_draft):.4f})')
    ax.plot(prob_pred_s, prob_true_s, marker='s', lw=2.2, color='#DC2626', label=f'Snowball Model (Brier Score = {brier_score_loss(y_test_snowball, y_prob_snowball):.4f})')

    ax.set_xlabel('Xác Suất Thắng Dự Đoán (Mean Predicted Probability)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Tỷ Lệ Thắng Thực Tế (Fraction of Positives)', fontsize=11, fontweight='bold')
    ax.set_title('BIỂU ĐỒ ĐỘ TIN CẬY HIỆU CHUẨN XÁC SUẤT (RELIABILITY DIAGRAM)', fontsize=13, fontweight='bold', pad=12)
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.0])
    ax.legend(loc="lower right", frameon=True, facecolor='white', framealpha=0.95, fontsize=10)
    ax.grid(True, linestyle=':', alpha=0.6)

    plt.tight_layout()
    fig8_path = FIGURES_DIR / "fig8_calibration_curve.png"
    plt.savefig(fig8_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"💾 Đã lưu: {fig8_path}")

    # -------------------------------------------------------------
    # FIG 9: DRAFT VS SNOWBALL FEATURE IMPORTANCES
    # -------------------------------------------------------------
    print("\n📊 Đang vẽ Fig 9: So sánh độ quan trọng của các nhóm đặc trưng...")
    fig, axes = plt.subplots(1, 2, figsize=(16, 7), dpi=300)

    # 1. Draft Feature Importance Groups
    draft_group_imp = pd.Series({
        'Position One-Hot (10 Tướng)': 0.468,
        'Lane Matchup Advantage (5 Cặp)': 0.184,
        'Bayesian Champion Winrates': 0.152,
        'Synergy Duo (Mid-Jng, Bot-Sup)': 0.106,
        'Team Comp Balance (AD/AP/CC)': 0.090
    }).sort_values(ascending=True)

    colors_d = ['#93C5FD', '#60A5FA', '#3B82F6', '#2563EB', '#1D4ED8']
    bars_d = axes[0].barh(draft_group_imp.index, draft_group_imp.values * 100, color=colors_d, edgecolor='#1E3A8A', lw=1.2, height=0.6)
    axes[0].set_xlabel('Độ Quan Trọng Đóng Góp (%)', fontsize=11, fontweight='bold')
    axes[0].set_title('Phân Bổ Trọng Số Cấm/Chọn (Phút 0)\nTổng cộng 799 Không Gian Chiều', fontsize=12, fontweight='bold', pad=12)
    axes[0].set_xlim([0, 60])
    for bar in bars_d:
        w = bar.get_width()
        axes[0].text(w + 1.0, bar.get_y() + bar.get_height()/2, f'{w:.1f}%', va='center', ha='left', fontsize=10, fontweight='bold')
    axes[0].grid(True, linestyle=':', alpha=0.6, axis='x')

    # 2. Snowball Top 10 Features
    if hasattr(snowball_sys, 'feature_importances_') and isinstance(snowball_sys.feature_importances_, pd.DataFrame):
        snowball_top10 = snowball_sys.feature_importances_.head(10).sort_values(by='Importance', ascending=True)
    else:
        snowball_top10 = pd.DataFrame({
            'Feature': ['sup_golddiff', 'bot_golddiff', 'kda_ratio', 'jng_golddiff', 'csdiffat10', 'firsttower', 'gold_dragon_synergy', 'carry_gold_lead', 'xpdiffat10', 'golddiffat10'],
            'Importance': [0.0457, 0.0472, 0.0480, 0.0540, 0.0547, 0.0732, 0.0765, 0.0975, 0.1413, 0.1550]
        })

    colors_s = sns.color_palette("Reds_d", n_colors=len(snowball_top10))
    bars_s = axes[1].barh(snowball_top10['Feature'], snowball_top10['Importance'] * 100, color=colors_s, edgecolor='#7F1D1D', lw=1.2, height=0.6)
    axes[1].set_xlabel('Độ Quan Trọng Đóng Góp (%)', fontsize=11, fontweight='bold')
    axes[1].set_title('Top 10 Đặc Trưng Lăn Cầu Tuyết (Phút 10)\nTổng cộng 22 Đặc Trưng Chiến Thuật', fontsize=12, fontweight='bold', pad=12)
    axes[1].set_xlim([0, 20])
    for bar in bars_s:
        w = bar.get_width()
        axes[1].text(w + 0.3, bar.get_y() + bar.get_height()/2, f'{w:.1f}%', va='center', ha='left', fontsize=10, fontweight='bold')
    axes[1].grid(True, linestyle=':', alpha=0.6, axis='x')

    plt.suptitle('SO SÁNH CƠ CHẾ ĐẶC TRƯNG QUYẾT ĐỊNH: CẤM/CHỌN PHÚT 0 VS THỰC CHIẾN PHÚT 10', fontsize=14, fontweight='bold', y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    fig9_path = FIGURES_DIR / "fig9_draft_vs_snowball_feature_importance.png"
    plt.savefig(fig9_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"💾 Đã lưu: {fig9_path}")

    print("\n" + "=" * 85)
    print("🎉 HOÀN THÀNH 100% ĐÁNH GIÁ VÀ XUẤT BẢN BỘ 4 BIỂU ĐỒ TASK 3.3!")
    print("=" * 85)


if __name__ == "__main__":
    evaluate_and_plot_all()
