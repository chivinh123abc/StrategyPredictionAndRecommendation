"""
================================================================================
MODULE 05: TRỰC QUAN HÓA DỮ LIỆU EDA (EXPLORATORY DATA ANALYSIS)
Task 2.4: Bộ 5 Biểu Đồ EDA Chuẩn Khoa Học 300 DPI (Chương 3 - Trực quan hóa dữ liệu)
Giáo trình: Nhập môn Khoa học Dữ liệu - TS. Thái Tuyết Hải (PTIT)
================================================================================
"""

import sys
import argparse
import sqlite3
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Thêm thư mục gốc vào sys.path để nạp src.config
current_file = Path(__file__).resolve()
base_dir = current_file.parent.parent.parent
if str(base_dir) not in sys.path:
    sys.path.insert(0, str(base_dir))

from src.config.settings import OUTPUT_DB, BASE_DIR

FIGURES_DIR = Path(BASE_DIR) / "reports" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)


class EDAPlotter:
    """
    Class thực hiện Trực quan hóa Khám phá Dữ liệu (EDA) chuẩn khoa học:
    Sinh bộ 5 biểu đồ chất lượng cao (300 DPI) phân tích dữ liệu LMHT mốc 10 phút.
    
    Danh mục 5 biểu đồ:
      1. Fig 1: Heatmap Ma Trận Tương Quan Pearson giữa các chỉ số 10 phút & Kết quả thắng.
      2. Fig 2: Phân Phối Chênh Lệch Vàng lúc 10 phút (Histogram + KDE) Đấu Giải vs Rank.
      3. Fig 3: Boxplot Phân Bố Kinh Tế & Chỉ Số Lính (CS) theo 5 Vị Trí Thi Đấu.
      4. Fig 4: Scatter Plot & Đường Hồi Quy: Chênh Lệch Vàng 10p vs Thời Lượng Trận Đấu.
      5. Fig 5: Grouped Bar Chart So Sánh Tỷ Lệ Thắng 4 Kịch Bản Mục Tiêu Lớn (3 Sâu vs Rồng 1).
    """

    def __init__(self, db_path: Path = OUTPUT_DB, output_dir: Path = FIGURES_DIR, dpi: int = 300):
        self.db_path = Path(db_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.dpi = dpi
        
        # Thiết lập style thẩm mỹ thống nhất cho toàn bộ biểu đồ
        self._setup_plot_style()

    @staticmethod
    def _setup_plot_style():
        """Cấu hình typography, palette màu và lưới đồ họa cho Matplotlib & Seaborn"""
        plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Segoe UI', 'Helvetica']
        plt.rcParams['axes.unicode_minus'] = False
        sns.set_theme(style="whitegrid", palette="deep")

    def load_data(self) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Trích xuất 3 tập dữ liệu từ CSDL SQLite: Pro Matches, Rank Matches, Pro Players"""
        conn = sqlite3.connect(self.db_path)

        # 1. Đấu Giải Cấp Đội (Pro Matches)
        q_pro = """
        SELECT gameid, side, teamname, league, result,
               gamelength / 60.0 AS duration_min,
               golddiffat10, xpdiffat10, csdiffat10,
               killsat10, deathsat10,
               towers, firstdragon,
               void_grubs, dragons
        FROM tournament_matches
        WHERE datacompleteness = 'complete'
        """
        df_pro = pd.read_sql_query(q_pro, conn)

        # 2. Solo Rank Cấp Đội (Rank Matches 10 phút)
        q_rank = """
        SELECT gameId, server, blueWins,
               gameDuration / 60.0 AS duration_min,
               blueGoldDiff, blueExperienceDiff,
               ((blueTotalMinionsKilled + blueTotalJungleMinionsKilled) - (redTotalMinionsKilled + redTotalJungleMinionsKilled)) AS blueCSDiff,
               blueKills, blueDeaths,
               blueDragons, blueVoidgrubs,
               redDragons, redVoidgrubs,
               blueTowersDestroyed, redTowersDestroyed
        FROM matches_10min
        """
        df_rank = pd.read_sql_query(q_rank, conn)

        # 3. Tuyển Thủ 1v1 Đấu Giải (Pro Players 10 phút)
        q_players = """
        SELECT p.gameid, p.side, p.position, p.playername, p.champion, p.result,
               p.totalgold, p.damagetochampions,
               p.killsat10, p.deathsat10, p.assistsat10,
               p.golddiffat10, p.xpdiffat10, p.csdiffat10
        FROM tournament_players p
        JOIN tournament_matches m ON p.gameid = m.gameid AND p.side = m.side
        WHERE m.datacompleteness = 'complete'
        """
        df_players = pd.read_sql_query(q_players, conn)

        conn.close()
        return df_pro, df_rank, df_players

    def plot_fig1_correlation_heatmap(self) -> Path:
        """
        Fig 1: Bản Đồ Nhiệt Ma Trận Tương Quan Pearson (Correlation Heatmap)
        Đo mức độ tương quan giữa các chỉ số mốc 10 phút với Kết quả thắng trận (Result).
        """
        df_pro, df_rank, _ = self.load_data()

        # Chọn các đặc trưng kinh tế & mục tiêu lúc 10 phút của Đấu Giải
        feature_cols = [
            'result', 'golddiffat10', 'xpdiffat10', 'csdiffat10',
            'killsat10', 'deathsat10', 'firstdragon', 'void_grubs', 'duration_min'
        ]
        feature_labels = [
            'Thắng Trận\n(Result)', 'Chênh Vàng\n(Gold Diff 10)', 'Chênh XP\n(XP Diff 10)', 
            'Chênh Lính\n(CS Diff 10)', 'Số Mạng Ăn\n(Kills 10)', 'Số Mạng Chết\n(Deaths 10)', 
            'Ăn Rồng 1\n(First Dragon)', 'Sâu Hư Không\n(Voidgrubs)', 'Thời Lượng\n(Duration)'
        ]
        
        corr_matrix = df_pro[feature_cols].corr()

        with sns.axes_style("white"):
            fig, ax = plt.subplots(figsize=(11, 9), dpi=self.dpi)
            
            # Mask nửa tam giác trên để tránh trùng lặp
            mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)
            
            cmap = sns.diverging_palette(220, 20, as_cmap=True)

            from mpl_toolkits.axes_grid1 import make_axes_locatable
            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size="3.5%", pad=0.25)
            
            sns.heatmap(
                corr_matrix, mask=mask, cmap=cmap, vmin=-1.0, vmax=1.0, center=0,
                annot=True, fmt=".2f", annot_kws={"size": 10, "weight": "bold"},
                square=True, linewidths=1.5, linecolor='white',
                cbar_ax=cax,
                cbar_kws={
                    "ticks": [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
                },
                xticklabels=feature_labels, yticklabels=feature_labels, ax=ax
            )

            ax.set_title("FIG 1: MA TRẬN TƯƠNG QUAN PEARSON CÁC CHỈ SỐ MỐC 10 PHÚT (ĐẤU GIẢI CHUYÊN NGHIỆP)", 
                         fontsize=12, fontweight='bold', pad=18, color='#1A365D')
            
            ax.set_xticklabels(feature_labels, rotation=0, fontsize=8.5, ha='center')
            ax.set_yticklabels(feature_labels, rotation=0, fontsize=8.5, va='center')
            ax.tick_params(left=False, bottom=False, top=False, right=False)
            ax.grid(False)
            for spine in ax.spines.values():
                spine.set_visible(False)

            cax.tick_params(labelsize=9)
            
            plt.tight_layout()
            out_path = self.output_dir / "fig1_correlation_heatmap.png"
            fig.savefig(out_path, dpi=self.dpi, bbox_inches='tight')
            plt.close(fig)
        return out_path

    def plot_fig2_gold_diff_distribution(self) -> Path:
        """
        Fig 2: Phân Phối Chênh Lệch Vàng lúc 10 phút (Histogram + KDE)
        So sánh hình dáng phân phối giữa Đội Thắng vs Đội Thua ở cả 2 môi trường Pro Play vs Solo Rank.
        """
        df_pro, df_rank, _ = self.load_data()

        fig, axes = plt.subplots(1, 2, figsize=(14, 6), dpi=self.dpi, sharey=True)

        # 1. Pro Play Subplot
        sns.histplot(
            data=df_pro, x='golddiffat10', hue='result', kde=True,
            palette={1: '#2B6CB0', 0: '#C53030'}, bins=40, alpha=0.45,
            ax=axes[0], legend=False
        )
        axes[0].axvline(0, color='gray', linestyle='--', linewidth=1.2, label='Cân bằng (0g)')
        axes[0].axvline(df_pro[df_pro['result']==1]['golddiffat10'].mean(), color='#2B6CB0', linestyle='-', linewidth=2, label=f"Mean Thắng: +{df_pro[df_pro['result']==1]['golddiffat10'].mean():.0f}g")
        axes[0].axvline(df_pro[df_pro['result']==0]['golddiffat10'].mean(), color='#C53030', linestyle='-', linewidth=2, label=f"Mean Thua: {df_pro[df_pro['result']==0]['golddiffat10'].mean():.0f}g")
        
        axes[0].set_title("Đấu Giải Chuyên Nghiệp (Pro Play - 4,752 quan sát)", fontsize=11, fontweight='bold', color='#2D3748')
        axes[0].set_xlabel("Chênh Lệch Vàng Lúc 10 Phút (Gold Diff @ 10)", fontsize=10)
        axes[0].set_ylabel("Mật Độ / Số Lượng Trận Đấu", fontsize=10)
        axes[0].legend(loc='upper right', frameon=True, fontsize=9)
        axes[0].set_xlim(-6000, 6000)

        # 2. Solo Rank Subplot (Ghép Blue + Red)
        df_rank_blue = pd.DataFrame({
            'golddiff': df_rank['blueGoldDiff'],
            'result': df_rank['blueWins']
        })
        df_rank_red = pd.DataFrame({
            'golddiff': -df_rank['blueGoldDiff'],
            'result': 1 - df_rank['blueWins']
        })
        df_rank_all = pd.concat([df_rank_blue, df_rank_red], ignore_index=True)

        sns.histplot(
            data=df_rank_all, x='golddiff', hue='result', kde=True,
            palette={1: '#2B6CB0', 0: '#C53030'}, bins=40, alpha=0.45,
            ax=axes[1], legend=False
        )
        axes[1].axvline(0, color='gray', linestyle='--', linewidth=1.2, label='Cân bằng (0g)')
        axes[1].axvline(df_rank_all[df_rank_all['result']==1]['golddiff'].mean(), color='#2B6CB0', linestyle='-', linewidth=2, label=f"Mean Thắng: +{df_rank_all[df_rank_all['result']==1]['golddiff'].mean():.0f}g")
        axes[1].axvline(df_rank_all[df_rank_all['result']==0]['golddiff'].mean(), color='#C53030', linestyle='-', linewidth=2, label=f"Mean Thua: {df_rank_all[df_rank_all['result']==0]['golddiff'].mean():.0f}g")
        
        axes[1].set_title("Solo Rank Thách Đấu (2,018 quan sát)", fontsize=11, fontweight='bold', color='#2D3748')
        axes[1].set_xlabel("Chênh Lệch Vàng Lúc 10 Phút (Gold Diff @ 10)", fontsize=10)
        axes[1].legend(loc='upper right', frameon=True, fontsize=9)
        axes[1].set_xlim(-6000, 6000)

        fig.suptitle("FIG 2: PHÂN PHỐI CHÊNH LỆCH VÀNG LÚC 10 PHÚT (HISTOGRAM + KDE DENSITY)", 
                     fontsize=13, fontweight='bold', y=0.98, color='#1A365D')

        plt.tight_layout()
        out_path = self.output_dir / "fig2_gold_diff_distribution_kde.png"
        fig.savefig(out_path, dpi=self.dpi)
        plt.close(fig)
        return out_path

    def plot_fig3_lane_economy_boxplot(self) -> Path:
        """
        Fig 3: Biểu Đồ Hộp (Boxplot & Outliers) Kinh Tế 5 Vị Trí Lúc 10 Phút
        So sánh mức độ chênh lệch vàng (Gold Diff @ 10) giữa Top, Jgl, Mid, Bot, Sup.
        """
        _, _, df_players = self.load_data()

        # Chuẩn hóa thứ tự 5 vị trí
        pos_order = ['top', 'jng', 'mid', 'bot', 'sup']
        pos_labels = ['Đường Trên\n(Top)', 'Đi Rừng\n(Jungle)', 'Đường Giữa\n(Mid)', 'Xạ Thủ\n(Bot / ADC)', 'Hỗ Trợ\n(Support)']
        
        df_plot = df_players[df_players['position'].isin(pos_order)].copy()

        fig, ax = plt.subplots(figsize=(11, 6), dpi=self.dpi)

        colors = ['#E53E3E', '#38A169', '#3182CE', '#D69E2E', '#805AD5']
        
        sns.boxplot(
            data=df_plot, x='position', y='golddiffat10', order=pos_order,
            hue='position', palette=colors, legend=False, width=0.5, fliersize=3.5,
            flierprops={'marker': 'o', 'markerfacecolor': 'gray', 'alpha': 0.5},
            ax=ax
        )

        # Thêm đường mốc 0g cân bằng
        ax.axhline(0, color='red', linestyle='--', linewidth=1.2, alpha=0.7)

        # Tính median hiển thị trên từng box
        medians = df_plot.groupby('position')['golddiffat10'].median()[pos_order]
        iqrs = df_plot.groupby('position')['golddiffat10'].apply(lambda x: x.quantile(0.75) - x.quantile(0.25))[pos_order]

        for i, (med, iqr_val) in enumerate(zip(medians, iqrs)):
            ax.text(i, med + 150, f"Med: {med:.0f}\nIQR: {iqr_val:.0f}", 
                    horizontalalignment='center', fontsize=8.5, fontweight='bold', color='#2D3748',
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8, edgecolor='none'))

        ax.set_title("FIG 3: PHÂN BỐ CHÊNH LỆCH VÀNG 10 PHÚT THEO 5 VỊ TRÍ THI ĐẤU (PRO PLAY)", 
                     fontsize=12, fontweight='bold', pad=15, color='#1A365D')
        ax.set_xlabel("Vị Trí Thi Đấu Trên Bản Đồ (Lane Positions)", fontsize=10, fontweight='bold')
        ax.set_ylabel("Chênh Lệch Vàng Đối Đầu 1v1 Lúc 10 Phút", fontsize=10, fontweight='bold')
        ax.set_xticks(range(len(pos_labels)))
        ax.set_xticklabels(pos_labels, fontsize=9.5)
        ax.set_ylim(-3500, 3500)

        plt.tight_layout()
        out_path = self.output_dir / "fig3_lane_economy_boxplot.png"
        fig.savefig(out_path, dpi=self.dpi)
        plt.close(fig)
        return out_path

    def plot_fig4_gold_lead_vs_duration_scatter(self) -> Path:
        """
        Fig 4: Biểu Đồ Phân Tán & Đường Hồi Quy (Scatter Plot + Regression Trendline)
        Mối quan hệ giữa Chênh lệch vàng lúc 10 phút và Thời lượng kết thúc trận đấu.
        """
        df_pro, df_rank, _ = self.load_data()

        # Chuẩn bị dữ liệu đội dẫn vàng
        df_pro_lead = df_pro[df_pro['golddiffat10'] >= 0].copy()
        
        df_rank_blue_lead = df_rank[df_rank['blueGoldDiff'] >= 0].copy()
        df_rank_blue_lead['lead_gold'] = df_rank_blue_lead['blueGoldDiff']
        
        df_rank_red_lead = df_rank[df_rank['blueGoldDiff'] < 0].copy()
        df_rank_red_lead['lead_gold'] = -df_rank_red_lead['blueGoldDiff']
        
        df_rank_lead = pd.concat([df_rank_blue_lead, df_rank_red_lead], ignore_index=True)

        fig, axes = plt.subplots(1, 2, figsize=(14, 6), dpi=self.dpi, sharey=True)

        # 1. Đấu Giải
        sns.regplot(
            data=df_pro_lead, x='golddiffat10', y='duration_min',
            scatter_kws={'alpha': 0.25, 'color': '#3182CE', 's': 20},
            line_kws={'color': '#C53030', 'linewidth': 2.5, 'label': 'Đường Hồi Quy Xu Hướng'},
            ax=axes[0]
        )
        axes[0].axhline(20, color='orange', linestyle=':', label='Mốc Baron (20 phút)')
        axes[0].set_title("Đấu Giải Chuyên Nghiệp (Pro Play)", fontsize=11, fontweight='bold', color='#2D3748')
        axes[0].set_xlabel("Vàng Dẫn Trước Lúc 10 Phút (Gold Lead @ 10)", fontsize=10)
        axes[0].set_ylabel("Thời Lượng Trận Đấu (Phút)", fontsize=10)
        axes[0].legend(loc='upper right', frameon=True, fontsize=9)
        axes[0].set_xlim(0, 5000)

        # 2. Solo Rank
        sns.regplot(
            data=df_rank_lead, x='lead_gold', y='duration_min',
            scatter_kws={'alpha': 0.35, 'color': '#38A169', 's': 25},
            line_kws={'color': '#C53030', 'linewidth': 2.5, 'label': 'Đường Hồi Quy Xu Hướng'},
            ax=axes[1]
        )
        axes[1].axhline(15, color='red', linestyle='--', label='Mốc Đầu Hàng Sớm FF15')
        axes[1].axhline(20, color='orange', linestyle=':', label='Mốc Baron (20 phút)')
        axes[1].set_title("Solo Rank Thách Đấu", fontsize=11, fontweight='bold', color='#2D3748')
        axes[1].set_xlabel("Vàng Dẫn Trước Lúc 10 Phút (Gold Lead @ 10)", fontsize=10)
        axes[1].legend(loc='upper right', frameon=True, fontsize=9)
        axes[1].set_xlim(0, 5000)

        fig.suptitle("FIG 4: MỐI QUAN HỆ GIỮA VÀNG DẪN TRƯỚC VÀ THỜI LƯỢNG TRẬN ĐẤU (SCATTER + REGRESSION)", 
                     fontsize=13, fontweight='bold', y=0.98, color='#1A365D')

        plt.tight_layout()
        out_path = self.output_dir / "fig4_gold_lead_vs_duration_scatter.png"
        fig.savefig(out_path, dpi=self.dpi)
        plt.close(fig)
        return out_path

    def plot_fig5_neutral_objectives_scenarios(self) -> Path:
        """
        Fig 5: Biểu Đồ Cột Nhóm Toàn Diện 8 Tổ Hợp Mục Tiêu Lớn (Rồng 1 x 0, 1, 2, 3 Sâu)
        So sánh chi tiết Tỷ lệ thắng giữa Đấu Giải (Pro Play) và Solo Rank (Task 2.3).
        """
        df_pro, df_rank, _ = self.load_data()

        # 1. Tính số liệu 8 tổ hợp cho Đấu Giải (Pro Play)
        df_pro_work = df_pro[df_pro['void_grubs'].isin([0, 1, 2, 3])].copy()
        df_pro_work['has_drag'] = df_pro_work['firstdragon'].fillna(0).astype(int)
        pro_stats = df_pro_work.groupby(['has_drag', 'void_grubs'])['result'].mean() * 100.0

        # 2. Tính số liệu 8 tổ hợp cho Solo Rank
        df_rank_blue = pd.DataFrame({
            'has_drag': (df_rank['blueDragons'] > 0).astype(int),
            'void_grubs': df_rank['blueVoidgrubs'].clip(0, 3),
            'result': df_rank['blueWins']
        })
        df_rank_red = pd.DataFrame({
            'has_drag': (df_rank['redDragons'] > 0).astype(int),
            'void_grubs': df_rank['redVoidgrubs'].clip(0, 3),
            'result': 1 - df_rank['blueWins']
        })
        df_rank_all = pd.concat([df_rank_blue, df_rank_red], ignore_index=True)
        rank_stats = df_rank_all.groupby(['has_drag', 'void_grubs'])['result'].mean() * 100.0

        grub_labels = ['0 Sâu\n(0 Grubs)', '1 Sâu\n(1 Grub)', '2 Sâu\n(2 Grubs)', '3 Sâu\n(3 Grubs)']
        x = np.arange(len(grub_labels))
        width = 0.36

        fig, axes = plt.subplots(1, 2, figsize=(14, 6), dpi=self.dpi, sharey=True)

        # Function helper vẽ từng subplot
        def draw_subplot(ax, stats, title, subtitle):
            no_drag = [stats.get((0, g), 0.0) for g in range(4)]
            has_drag = [stats.get((1, g), 0.0) for g in range(4)]

            rects_no = ax.bar(x - width/2, no_drag, width, label='Mất Rồng 1 (0 Dragons)', color='#C53030', alpha=0.9, edgecolor='black', linewidth=0.8)
            rects_has = ax.bar(x + width/2, has_drag, width, label='Có Rồng 1 (First Dragon)', color='#2B6CB0', alpha=0.9, edgecolor='black', linewidth=0.8)

            ax.axhline(50, color='gray', linestyle='--', linewidth=1.2, alpha=0.8, label='Mốc Cân Bằng (50%)')

            for rect in rects_no:
                h = rect.get_height()
                ax.annotate(f'{h:.1f}%',
                            xy=(rect.get_x() + rect.get_width() / 2, h),
                            xytext=(0, 3), textcoords="offset points",
                            ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#742A2A')

            for rect in rects_has:
                h = rect.get_height()
                ax.annotate(f'{h:.1f}%',
                            xy=(rect.get_x() + rect.get_width() / 2, h),
                            xytext=(0, 3), textcoords="offset points",
                            ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#1A365D')

            ax.set_title(f"{title}\n({subtitle})", fontsize=11, fontweight='bold', color='#1A365D', pad=10)
            ax.set_xlabel("Số Lượng Sâu Hư Không Ăn Được Lúc 10 Phút", fontsize=10, fontweight='bold')
            ax.set_xticks(x)
            ax.set_xticklabels(grub_labels, fontsize=9.5)
            ax.set_ylim(0, 90)
            ax.legend(loc='upper left', frameon=True, fontsize=8.5)

        draw_subplot(axes[0], pro_stats, "Đấu Giải Chuyên Nghiệp (Pro Play)", "4,752 quan sát đội")
        draw_subplot(axes[1], rank_stats, "Solo Rank Thách Đấu (VN & KR)", "2,018 quan sát đội")

        axes[0].set_ylabel("Tỷ Lệ Thắng Cuối Trận (%)", fontsize=10, fontweight='bold')

        fig.suptitle("FIG 5: MA TRẬN 8 TỔ HỢP MỤC TIÊU LỚN 10 PHÚT (RỒNG 1 x 0, 1, 2, 3 SÂU HƯ KHÔNG)", 
                     fontsize=12.5, fontweight='bold', y=0.98, color='#1A365D')

        plt.tight_layout()
        out_path = self.output_dir / "fig5_neutral_objectives_scenarios_bar.png"
        fig.savefig(out_path, dpi=self.dpi)
        plt.close(fig)
        return out_path

    def plot_all(self) -> dict[str, Path]:
        """Tạo toàn bộ bộ 5 biểu đồ EDA chất lượng cao 300 DPI"""
        print("=" * 80)
        print("🎨 BẮT ĐẦU XUẤT BỘ 5 BIỂU ĐỒ TRỰC QUAN HÓA EDA (CHƯƠNG 3 - CHUẨN 300 DPI)")
        print("=" * 80)

        figs = {}
        print("⏳ [1/5] Đang vẽ Fig 1: Bản đồ nhiệt ma trận tương quan Pearson...")
        figs["fig1"] = self.plot_fig1_correlation_heatmap()
        print(f"   --> Đã lưu: {figs['fig1']}")

        print("⏳ [2/5] Đang vẽ Fig 2: Phân phối chênh lệch vàng (Histogram + KDE)...")
        figs["fig2"] = self.plot_fig2_gold_diff_distribution()
        print(f"   --> Đã lưu: {figs['fig2']}")

        print("⏳ [3/5] Đang vẽ Fig 3: Phân bố kinh tế 5 vị trí (Boxplot & Outliers)...")
        figs["fig3"] = self.plot_fig3_lane_economy_boxplot()
        print(f"   --> Đã lưu: {figs['fig3']}")

        print("⏳ [4/5] Đang vẽ Fig 4: Quan hệ vàng dẫn trước vs thời lượng (Scatter + Regression)...")
        figs["fig4"] = self.plot_fig4_gold_lead_vs_duration_scatter()
        print(f"   --> Đã lưu: {figs['fig4']}")

        print("⏳ [5/5] Đang vẽ Fig 5: Ma trận 4 kịch bản mục tiêu lớn (Grouped Bar Chart)...")
        figs["fig5"] = self.plot_fig5_neutral_objectives_scenarios()
        print(f"   --> Đã lưu: {figs['fig5']}")

        print("=" * 80)
        print(f"✅ HOÀN THÀNH XUẤT 5 BIỂU ĐỒ EDA THÀNH CÔNG VÀO THƯ MỤC: {self.output_dir}")
        print("=" * 80)
        return figs


def main():
    parser = argparse.ArgumentParser(description="Task 2.4: Xuất bộ 5 biểu đồ EDA 300 DPI (Chương 3)")
    parser.add_argument("--db", type=str, default=str(OUTPUT_DB), help="Đường dẫn CSDL SQLite")
    parser.add_argument("--out", type=str, default=str(FIGURES_DIR), help="Thư mục xuất ảnh")
    parser.add_argument("--dpi", type=int, default=300, help="Độ phân giải hình ảnh (mặc định: 300 DPI)")
    parser.add_argument("--fig", type=int, choices=[1, 2, 3, 4, 5], default=None, help="Vẽ riêng 1 biểu đồ cụ thể (1..5)")
    args = parser.parse_args()

    plotter = EDAPlotter(db_path=Path(args.db), output_dir=Path(args.out), dpi=args.dpi)

    if args.fig == 1:
        plotter.plot_fig1_correlation_heatmap()
    elif args.fig == 2:
        plotter.plot_fig2_gold_diff_distribution()
    elif args.fig == 3:
        plotter.plot_fig3_lane_economy_boxplot()
    elif args.fig == 4:
        plotter.plot_fig4_gold_lead_vs_duration_scatter()
    elif args.fig == 5:
        plotter.plot_fig5_neutral_objectives_scenarios()
    else:
        plotter.plot_all()


if __name__ == "__main__":
    main()
