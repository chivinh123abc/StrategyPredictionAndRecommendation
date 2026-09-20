import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def create_full_specialized_project_document(output_path):
    doc = Document()

    # Cấu hình lề trang (Standard 1 inch / 2.54 cm)
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)
        section.different_first_page_header_footer = True
        
        # Header & Footer cho các trang sau
        header = section.header
        p_head = header.paragraphs[0]
        p_head.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r_head = p_head.add_run("ĐỒ ÁN NHẬP MÔN KHOA HỌC DỮ LIỆU - PTIT")
        r_head.font.name = "Calibri"
        r_head.font.size = Pt(8.5)
        r_head.font.color.rgb = RGBColor(120, 120, 120)

        footer = section.footer
        p_foot = footer.paragraphs[0]
        p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_foot = p_foot.add_run("Bản Đặc tả Kỹ thuật Chuyên sâu & Danh mục Tài nguyên Dữ liệu")
        r_foot.font.name = "Calibri"
        r_foot.font.size = Pt(8.5)
        r_foot.font.color.rgb = RGBColor(120, 120, 120)

    # Bảng màu chuyên nghiệp (Corporate Navy & Slate Blue)
    COLOR_PRIMARY = RGBColor(31, 78, 121)     # #1F4E79 (Deep Navy)
    COLOR_SECONDARY = RGBColor(46, 117, 182) # #2E75B6 (Steel Blue)
    COLOR_TEXT = RGBColor(40, 40, 40)         # #282828 (Charcoal)
    COLOR_MUTED = RGBColor(100, 100, 100)     # #646464 (Gray)
    HEX_HEADER_BG = "1F4E79"
    HEX_ALT_ROW = "F2F5F8"
    HEX_CALLOUT_BG = "EDF4FA"
    HEX_BORDER = "CCCCCC"

    # Định dạng style Normal
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Calibri'
    style_normal.font.size = Pt(11)
    style_normal.font.color.rgb = COLOR_TEXT
    style_normal.paragraph_format.line_spacing = 1.2
    style_normal.paragraph_format.space_after = Pt(5)

    def add_custom_heading(text, level, space_before=14, space_after=6):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Calibri'
        if level == 1:
            run.font.size = Pt(17)
            run.font.color.rgb = COLOR_PRIMARY
        elif level == 2:
            run.font.size = Pt(13.5)
            run.font.color.rgb = COLOR_SECONDARY
        elif level == 3:
            run.font.size = Pt(11.5)
            run.font.color.rgb = COLOR_PRIMARY
        return p

    def add_callout(text, bold_prefix=""):
        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = table.cell(0, 0)
        cell.width = Inches(6.5)
        
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(f'''
            <w:tcBorders {nsdecls("w")}>
                <w:top w:val="none" w:sz="0" w:space="0" w:color="auto"/>
                <w:left w:val="single" w:sz="24" w:space="0" w:color="1F4E79"/>
                <w:bottom w:val="none" w:sz="0" w:space="0" w:color="auto"/>
                <w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>
            </w:tcBorders>
        ''')
        tcPr.append(borders)
        shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{HEX_CALLOUT_BG}"/>')
        tcPr.append(shading)
        
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.left_indent = Inches(0.15)
        p.paragraph_format.right_indent = Inches(0.15)
        
        if bold_prefix:
            r_bold = p.add_run(bold_prefix + " ")
            r_bold.bold = True
            r_bold.font.color.rgb = COLOR_PRIMARY
        r_text = p.add_run(text)
        r_text.font.size = Pt(10)
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    def style_table(table, col_widths=None):
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        for i, row in enumerate(table.rows):
            trPr = row._tr.get_or_add_trPr()
            trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
            if i == 0:
                trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))

            for j, cell in enumerate(row.cells):
                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                if col_widths and j < len(col_widths):
                    cell.width = col_widths[j]
                
                tcPr = cell._tc.get_or_add_tcPr()
                tcMar = parse_xml(f'''
                    <w:tcMar {nsdecls("w")}>
                        <w:top w:w="120" w:type="dxa"/>
                        <w:bottom w:w="120" w:type="dxa"/>
                        <w:left w:w="160" w:type="dxa"/>
                        <w:right w:w="160" w:type="dxa"/>
                    </w:tcMar>
                ''')
                tcPr.append(tcMar)

                if i == 0:
                    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{HEX_HEADER_BG}"/>')
                    tcPr.append(shd)
                    for p in cell.paragraphs:
                        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                        for r in p.runs:
                            r.font.bold = True
                            r.font.color.rgb = RGBColor(255, 255, 255)
                            r.font.size = Pt(9.5)
                else:
                    if i % 2 == 0:
                        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{HEX_ALT_ROW}"/>')
                        tcPr.append(shd)
                    for p in cell.paragraphs:
                        for r in p.runs:
                            r.font.size = Pt(9)
                
                bdr = parse_xml(f'''
                    <w:tcBorders {nsdecls("w")}>
                        <w:top w:val="single" w:sz="4" w:space="0" w:color="{HEX_BORDER}"/>
                        <w:left w:val="none"/>
                        <w:bottom w:val="single" w:sz="4" w:space="0" w:color="{HEX_BORDER}"/>
                        <w:right w:val="none"/>
                    </w:tcBorders>
                ''')
                tcPr.append(bdr)

    # =========================================================================
    # TRANG TIÊU ĐỀ & TỔNG QUAN
    # =========================================================================
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG (PTIT HCM)\nKHOA CÔNG NGHỆ THÔNG TIN")
    r_inst.font.size = Pt(12)
    r_inst.font.bold = True
    r_inst.font.color.rgb = COLOR_SECONDARY
    p_inst.paragraph_format.space_after = Pt(28)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("BẢN ĐẶC TẢ KỸ THUẬT & KẾ HOẠCH TRIỂN KHAI\nĐỒ ÁN CUỐI KỲ MÔN KHOA HỌC DỮ LIỆU")
    r_title.font.size = Pt(21)
    r_title.font.bold = True
    r_title.font.color.rgb = COLOR_PRIMARY
    p_title.paragraph_format.space_after = Pt(10)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("Phân tích chuyên sâu 5 hướng đề tài đột phá:\nEsports LoL, Spotify Music, Pokémon VGC, Thẻ bài TCG & Bất động sản Đô thị VN\n(Bao quát 100% nội dung giáo trình Chương 0 đến Chương 6)")
    r_sub.font.size = Pt(12)
    r_sub.font.italic = True
    r_sub.font.color.rgb = COLOR_MUTED
    p_sub.paragraph_format.space_after = Pt(28)

    # Bảng thông tin học phần
    tbl_info = doc.add_table(rows=4, cols=2)
    tbl_info.alignment = WD_TABLE_ALIGNMENT.CENTER
    info_data = [
        ("Môn học:", "Nhập môn Khoa học Dữ liệu (Introduction to Data Science)"),
        ("Giảng viên phụ trách:", "TS. Thái Tuyết Hải (tuyethai@ptithcm.edu.vn)"),
        ("Tỷ trọng điểm đồ án:", "60% Tổng kết môn học (Đồ án nhóm tối đa 3 sinh viên)"),
        ("Phạm vi tài liệu:", "Đặc tả kỹ thuật 5 chủ đề, thiết kế thuật toán, danh mục link API và lộ trình 6 tuần")
    ]
    for idx, (label, val) in enumerate(info_data):
        c0 = tbl_info.cell(idx, 0)
        c1 = tbl_info.cell(idx, 1)
        c0.text = label
        c1.text = val
        c0.paragraphs[0].runs[0].font.bold = True
        c0.paragraphs[0].runs[0].font.color.rgb = COLOR_PRIMARY
        c0.width = Inches(2.2)
        c1.width = Inches(4.3)
    p_space = doc.add_paragraph()
    p_space.paragraph_format.space_after = Pt(20)

    add_callout(
        "Tài liệu này tổng hợp 5 hướng đề tài chọn lọc, từ Thể thao điện tử, Âm nhạc, Pokémon chiến thuật, "
        "Thị trường thẻ bài TCG cho đến đề tài Xã hội về Bất động sản & An cư Đô thị Việt Nam (xếp ở thứ tự ưu tiên cuối). "
        "Mỗi đề tài đều tích hợp trọn vẹn 100% các kiến thức trong giáo trình của TS. Thái Tuyết Hải.",
        bold_prefix="ĐỊNH HƯỚNG TỔNG QUAN:"
    )

    doc.add_page_break()

    # =========================================================================
    # PHẦN I: MA TRẬN ÁNH XẠ TOÀN BỘ GIÁO TRÌNH
    # =========================================================================
    add_custom_heading("PHẦN I: MA TRẬN ÁNH XẠ TOÀN BỘ GIÁO TRÌNH (CHAPTER 0 - 6)", 1)
    
    p_p1 = doc.add_paragraph(
        "Dù lựa chọn bất kỳ đề tài nào trong 5 chủ đề, nhóm sinh viên đều phải chứng minh việc ứng dụng đầy đủ "
        "từng module kiến thức theo chuẩn đề cương môn học:"
    )

    tbl_matrix = doc.add_table(rows=8, cols=4)
    matrix_headers = ["Chương học", "Chủ đề cốt lõi trong slide", "Công cụ & Thuật toán", "Yêu cầu thực thi bắt buộc"]
    for j, h in enumerate(matrix_headers):
        tbl_matrix.cell(0, j).paragraphs[0].text = h

    matrix_rows = [
        ("Chương 1:\nPreliminaries", 
         "Đại số tuyến tính, Xác suất thống kê, Định lý Bayes, Phân phối chuẩn, CLT, Thống kê mô tả (Mean, Variance, IQR), Kiểm định giả thuyết.",
         "Scipy.stats, Numpy, Math",
         "Thực hiện kiểm định giả thuyết thống kê (t-test / Z-test, p-value < 0.05) để kiểm tra các giả thuyết nghiên cứu (A/B testing)."),
        ("Chương 2:\nData Preparation", 
         "Data Collection (Web crawler, Scraping BeautifulSoup, API), Data Cleaning (Missing, Outliers), Normalization (Min-Max, Z-Score), Reduction (Sampling, PCA).",
         "BeautifulSoup, Requests, Scikit-learn (PCA, StandardScaler)",
         "Crawl trực tiếp từ web/API; xử lý triệt để missing/outlier; chuẩn hóa đặc trưng và lấy mẫu dữ liệu phân tầng."),
        ("Chương 3:\nData Visualization", 
         "Line plot (trend), Bar chart, Scatter plot (tương quan), Box plot (ngoại lai), Error bars, Density/KDE & Histogram, Subplots, 3D Plot, Annotations.",
         "Matplotlib, Seaborn",
         "Xây dựng hệ thống bảng điều khiển EDA trực quan hóa với đầy đủ 7 dạng biểu đồ cơ bản và nâng cao có chú thích (annotations)."),
        ("Chương 4:\nMachine Learning", 
         "Supervised: Naive Bayes (Laplace add-1), Linear Regression (Ridge/Lasso), SVM, Decision Tree, Random Forest, Ensemble (Bagging, Boosting).\nUnsupervised: K-Means, PCA.\nEvaluation: Holdout, CV, Bias-Variance.",
         "Scikit-learn (naive_bayes, linear_model, svm, ensemble, cluster, metrics)",
         "• Classification: Dự đoán nhãn / Sentiment Analysis.\n• Regression: Dự đoán chỉ số liên tục có điều chuẩn Ridge/Lasso.\n• Clustering: Phân cụm đối tượng bằng K-Means kết hợp PCA."),
        ("Chương 5:\nDatabases & SQL", 
         "DDL (Create Table, PK, FK, Constraints), DML (Insert, Update, Delete), Queries (SELECT, WHERE, JOIN, GROUP BY, HAVING, ORDER BY, Aggregation, Subqueries), NoSQL concept.",
         "SQLite3 / PostgreSQL, SQL Engine",
         "Khởi tạo Schema CSDL quan hệ 4-5 bảng; thực thi các truy vấn SQL nghiệp vụ phức tạp có JOIN nhiều bảng và lồng Subquery."),
        ("Chương 5x:\nPandas Manipulation", 
         "Series, DataFrame, Indexing (loc, iloc), Hierarchical Indexing (MultiIndex), Ufuncs, Missing data, Merge/Concat, GroupBy, Pivot Tables.",
         "Pandas",
         "Xây dựng data pipeline biến đổi ma trận tiện ích (Utility Matrix), tạo bảng tổng hợp Pivot và lập chỉ mục đa cấp."),
        ("Chương 6:\nRecommendation", 
         "Utility Matrix (Sparsity, Long Tail), Content-based Filtering (Item Profile TF-IDF, User Profile, Cosine Similarity), Collaborative Filtering (User-User, Item-Item), Hybrid, Đánh giá (RMSE, MAE).",
         "TfidfVectorizer, Cosine Similarity, Scikit-learn metrics",
         "Xây dựng bộ máy gợi ý đa phương thức (Content-based + Collaborative Filtering), xử lý bài toán Cold-Start và đo lường RMSE.")
    ]

    for i, row in enumerate(matrix_rows):
        for j, val in enumerate(row):
            tbl_matrix.cell(i+1, j).paragraphs[0].text = val

    style_table(tbl_matrix, [Inches(1.3), Inches(2.0), Inches(1.5), Inches(2.2)])

    # =========================================================================
    # PHẦN II: PHÂN TÍCH CHUYÊN SÂU 5 ĐỀ TÀI
    # =========================================================================
    add_custom_heading("PHẦN II: PHÂN TÍCH KỸ THUẬT CHUYÊN SÂU 5 ĐỀ TÀI ĐỘT PHÁ", 1)

    # -------------------------------------------------------------------------
    # ĐỀ TÀI 1: ESPORTS
    # -------------------------------------------------------------------------
    add_custom_heading("1. Đề tài 1: Esports LoL Analytics: Ban/Pick AI, Snowball Prediction & Pro Play vs Solo Queue Comparison", 2)
    p_es = doc.add_paragraph()
    p_es.add_run("Tên học thuật: ").bold = True
    p_es.add_run("Hệ Thống Trợ Lý Phân Tích Cấm/Chọn (Ban/Pick AI), Dự Đoán Thắng Thua Sớm 2 Giai Đoạn & Đối Chiếu Chiến Thuật Đấu Giải (Pro Play) vs Đấu Xếp Hạng (Solo Queue) trong Esports Liên Minh Huyền Thoại\n")
    p_es.add_run("Tổng quan: ").bold = True
    p_es.add_run(
        "Khai thác toàn diện hệ sinh thái Esports Liên Minh Huyền Thoại qua 3 nguồn dữ liệu lớn: "
        "(1) Hồ sơ 173 tướng từ Riot Data Dragon CDN; "
        "(2) Đường ống cào dữ liệu sống (Living Data Pipeline) thời gian thực từ Riot Match-v5 API (đầy đủ 10 lượt Cấm, 10 lượt Chọn theo 5 vị trí: Top, Jungle, Mid, ADC, Support mốc 10 phút); và "
        "(3) Tập dữ liệu Đấu Giải Chuyên Nghiệp (Pro Play) từ Oracle's Elixir và Leaguepedia Cargo API (các giải đấu VCS, LCK, LPL, CKTG với tên đội tuyển T1, Gen.G, GAM Esports và tuyển thủ Faker, Chovy, Levi). "
        "Hệ thống vừa đóng vai trò Trợ lý Cấm/Chọn AI, dự đoán kết quả trận đấu 2 tầng (Draft phút 0 & In-game phút 10), vừa nghiên cứu đối chiếu sự khác biệt chiến thuật sâu sắc giữa tuyển thủ chuyên nghiệp và người chơi xếp hạng rank cao."
    )
    
    bullets_es = [
        ("Chương 2 (Chuẩn bị dữ liệu & Kỹ thuật đặc trưng):", 
         "Tích hợp dữ liệu từ 2 nguồn: Đấu Rank (Riot API) và Đấu Giải (Oracle's Elixir / Leaguepedia). "
         "Làm sạch dữ liệu: Lọc bỏ 100% trận Remake (< 10 phút) và AFK qua chỉ số lính; loại bỏ ngoại lai phá game bằng thuật toán IQR và Z-Score. "
         "Trích xuất đặc trưng Đội hình Cấm/Chọn (Team Comp Engineering): Tỷ lệ AP/AD, điểm khống chế cứng (Hard CC score), độ chống chịu (Tankiness), tầm đánh; "
         "Bóc tách 5 vị trí thi đấu đối đầu trực diện: blueTop vs redTop, blueMid vs redMid, cặp đôi Bot 2v2 (ADC + Support)."),
        ("Chương 5 & 5x (SQL & Pandas):", 
         "Thiết kế CSDL quan hệ chuẩn hóa SQLite: Champions, Ranked_Matches (5 đường + bans), Tournament_Matches (Team1, Team2, Player, KDA). "
         "Truy vấn SQL nâng cao: Phân tích Kèo đấu Khắc chế 1v1 (Lane Matchup Query: Mid Katarina vs Lissandra, Top Akali vs Jax) bằng JOIN và GROUP BY; "
         "Phân tích Cặp đôi Ăn ý Đường Dưới (Bot Lane Synergy: Jinx+Pyke vs Caitlyn+Lux) có HAVING count >= 10; "
         "Subquery tìm các vị tướng có tỷ lệ Cấm/Chọn (Presence) cao nhất giải đấu VCS/LCK. Pandas: MultiIndex [Tournament, Role], Pivot Table so sánh tỷ lệ thắng theo tổ hợp tướng."),
        ("Chương 1 (Thống kê & Kiểm định giả thuyết A/B):", 
         "Kiểm định giả thuyết đối xứng bản đồ (Map Symmetry): 'Phe Xanh có tỷ lệ thắng cao hơn Phe Đỏ có ý nghĩa thống kê hay không?' (Z-test tỷ lệ 2 phía, alpha = 0.05, tính p-value). "
         "Kiểm định t-test độc lập: 'Hiệu quả Lăn Cầu Tuyết (Snowball Efficiency) ở Đấu Giải chuyên nghiệp (dẫn 2,000 vàng lúc 10p winrate 88%) có cao hơn có ý nghĩa thống kê so với Đấu Rank Kim Cương (75%) hay không?'. "
         "Kiểm định tác động của bùa Sâu Hư Không và Rồng đầu tiên."),
        ("Chương 3 (Trực quan hóa EDA):", 
         "Biểu đồ Mạng nhện (Radar Chart) so sánh 5 trục sức mạnh giữa 2 Đội hình (Giao tranh, Cấu rỉa, Bắt lẻ, Đẩy lẻ, Mở giao tranh). "
         "Biểu đồ Nhiệt Ma trận Khắc chế 1v1 từng đường (Counter-pick Lane Heatmap). "
         "Subplots so sánh trực quan Meta Đấu Giải vs Đấu Rank: Bar chart so sánh Top tướng ưu tiên (Pro chuộng Azir, K'Sante, Sejuani vs Rank chuộng Yasuo, Zed, Katarina). "
         "Box plot phân phối sát thương 5 vị trí. Line plot biến động chênh lệch vàng theo thời gian."),
        ("Chương 4 (Machine Learning 2 Giai đoạn & MLOps):", 
         "Mô hình Tầng 1 (Draft Prediction - Phút 0): Dùng Naive Bayes, Logistic Regression dự đoán xác suất thắng chỉ dựa vào chất tướng và kèo đấu 5 đường (~60% accuracy). "
         "Mô hình Tầng 2 (Snowball Prediction - Phút 10): Dùng Random Forest, AdaBoost, SVM kết hợp chất tướng + kinh tế phút 10 (vàng, rồng, sâu hư không, trụ) đẩy độ chính xác lên ~80% (Confusion Matrix, ROC-AUC). "
         "So sánh hiệu năng mô hình ML trên tập dữ liệu Đấu Giải (dữ liệu kỷ luật, ít nhiễu) vs tập dữ liệu Đấu Rank. "
         "Xây dựng Pipeline MLOps Tự động Học liên tục (Daily Retraining) cập nhật trọng số meta mới nhất. Phân cụm K-Means phân loại 4 trường phái chiến thuật đội hình (Poke, Dive, Teamfight, Split-push)."),
        ("Chương 6 (Hệ thống Gợi ý Cấm/Chọn Thông minh):", 
         "Hệ thống Ban/Pick AI Assistant toàn diện: "
         "(1) Gợi ý Kèo đấu Khắc chế từng đường (Lane Counter-Pick): Đối phương pick Mid Zed -> Gợi ý chọn Lissandra/Malzahar/Vex. "
         "(2) Gợi ý Kết hợp Ăn ý (Synergy Pick qua Association Rules): Đồng đội pick Yasuo Mid -> Gợi ý Rừng Diana/Malphite/Gragas; Xạ thủ Lucian -> Gợi ý Hỗ trợ Nami/Milio. "
         "(3) Gợi ý Phong cách Đội tuyển Vô địch (Championship Team Builder): Gợi ý xây dựng đội hình mô phỏng chiến thuật giao tranh của T1 hoặc Gen.G. "
         "(4) Gợi ý Mở rộng Bể Tướng (Content-based Cosine Similarity): Tìm tướng tương đồng thay thế khi tướng tủ bị Cấm. Đánh giá sai số RMSE, Precision@K.")
    ]
    for title, desc in bullets_es:
        p = doc.add_paragraph(style='List Bullet')
        r1 = p.add_run(title + " ")
        r1.bold = True
        r1.font.color.rgb = COLOR_PRIMARY
        p.add_run(desc)

    # -------------------------------------------------------------------------
    # ĐỀ TÀI 2: SPOTIFY MUSIC
    # -------------------------------------------------------------------------
    add_custom_heading("2. Đề tài 2: Spotify Audio Intelligence & Dynamic Playlist Recommender", 2)
    p_sp = doc.add_paragraph()
    p_sp.add_run("Tên học thuật: ").bold = True
    p_sp.add_run("Spotify Audio Intelligence, Track Popularity Forecasting & Personalized Playlist Recommendation Platform\n")
    p_sp.add_run("Tổng quan: ").bold = True
    p_sp.add_run(
        "Khai thác thuộc tính vật lý của sóng âm (Danceability, Energy, Acousticness, Valence, Tempo) qua Spotify Web API "
        "và tập dữ liệu 160,000+ bài hát trên Kaggle để xây dựng bộ máy gợi ý nhạc theo tâm trạng."
    )

    bullets_sp = [
        ("Chương 2 (Chuẩn bị dữ liệu):", "Trích xuất Audio Features từ Spotify API; dataset 160,000 bài hát. Loại bỏ track duplicate/remastered; lọc ngoại lai thời lượng bài hát; chuẩn hóa Min-Max Tempo và Z-score Popularity theo thập kỷ; PCA giảm chiều sóng âm."),
        ("Chương 5 & 5x (SQL & Pandas):", "CSDL Tracks, Artists, Albums, Audio_Features, Playlists. Truy vấn SQL: GROUP BY thể loại có năng lượng cao nhất (HAVING count >= 100); JOIN 4 bảng truy xuất lịch sử nghe; Subquery tìm bài hot hơn trung bình album. Pandas Pivot Table theo thập niên."),
        ("Chương 1 (Thống kê & Kiểm định):", "Kiểm định giả thuyết t-test độc lập: 'Độ ồn (Loudness) và năng lượng (Energy) của âm nhạc hiện đại (2020s) có tăng cao hơn có ý nghĩa thống kê so với thập niên 1980s hay không?' (Loudness War hypothesis, p-value < 0.05)."),
        ("Chương 3 (Trực quan hóa EDA):", "Line plot (tiến hóa xu hướng âm nhạc qua các năm), Bar chart (top nghệ sĩ), Scatter plot (Valence vs Energy 4 góc phần tư tâm trạng), Box plot (Tempo theo thể loại), 3D plot (Danceability-Energy-Valence), Subplots đa chiều."),
        ("Chương 4 (Machine Learning):", "Regression: Dự đoán điểm Popularity (0-100) bằng Linear Regression với điều chuẩn Ridge/Lasso. Classification: Phân loại thể loại / tâm trạng (Happy/Sad/Chill) bằng Naive Bayes và Random Forest. Clustering: K-Means phân cụm Gu âm nhạc kết hợp PCA."),
        ("Chương 6 (Hệ thống gợi ý):", "Content-based: Cosine Similarity trên vector sóng âm để tạo playlist đồng chất từ 1 bài mẫu (Seed Track). Collaborative Filtering: Item-Item CF trên ma trận Playlist x Track. Đánh giá RMSE, Precision@K.")
    ]
    for title, desc in bullets_sp:
        p = doc.add_paragraph(style='List Bullet')
        r1 = p.add_run(title + " ")
        r1.bold = True
        r1.font.color.rgb = COLOR_PRIMARY
        p.add_run(desc)

    # -------------------------------------------------------------------------
    # ĐỀ TÀI 3: POKEMON CHAMPIONS & OPTIMAL TEAM PICKER
    # -------------------------------------------------------------------------
    add_custom_heading("3. Đề tài 3: Competitive Pokémon VGC Analytics & Optimal Counter Team Picker", 2)
    p_pk = doc.add_paragraph()
    p_pk.add_run("Tên học thuật: ").bold = True
    p_pk.add_run("Competitive Pokémon Battle Analytics, Match Outcome Prediction & Optimal Counter-Team Recommendation Engine\n")
    p_pk.add_run("Ý nghĩa thực tiễn & Điểm nhấn: ").bold = True
    p_pk.add_run(
        "Đấu trường Pokémon cạnh tranh (VGC / Smogon) là đỉnh cao của tư duy chiến thuật theo lượt, "
        "nơi 18 hệ (Types), hàng trăm chiêu thức, đặc tính (Abilities) và tương quan chỉ số Base Stats đối đầu nhau. "
        "Điểm đột phá đặc biệt của đề tài này là xây dựng thuật toán Tối ưu hóa lựa chọn Pokémon (Optimal Counter Picker): "
        "tự động tính toán điểm yếu của đội đối phương và gợi ý con Pokémon tối ưu nhất để khắc chế toàn diện."
    )

    bullets_pk = [
        ("Chương 2 (Chuẩn bị dữ liệu):", 
         "Kéo thông số 1,025 Pokémon từ PokéAPI (HP, Atk, Def, SpA, SpD, Spe, Types, Abilities); tải logs thi đấu Smogon/Showdown. Làm sạch dữ liệu các trận đấu disconnect sớm; chuẩn hóa Min-Max cho Base Stat Total (BST); chuẩn hóa Z-Score cho điểm tốc độ Spe; dùng PCA giảm 6 chỉ số chiến đấu thành 2 trục: Sức mạnh tấn công (Offensive Power) và Sức chịu đựng (Bulkiness)."),
        ("Chương 5 & 5x (SQL & Pandas):", 
         "Thiết kế CSDL quan hệ: Pokemon (id, name, type1, type2, hp, atk, def, spa, spd, spe, bst), Moves (move_id, name, type, power, accuracy), Teams (team_id, format, winrate), Team_Members (team_id, pokemon_id). Truy vấn SQL: GROUP BY tìm hệ (Type) có chỉ số tấn công trung bình cao nhất có HAVING số lượng Pokémon >= 20; JOIN 3 bảng để liên kết đội hình và kết quả trận; Subquery lọc các Pokémon có Base Speed cao hơn trung bình của cả Tier. Pandas: Pivot Table ma trận tương khắc 18x18 giữa các Hệ."),
        ("Chương 1 (Thống kê & Kiểm định):", 
         "Kiểm định giả thuyết thống kê: 'Lợi thế khắc chế Hệ (Type Advantage) hay Tốc độ cơ bản (Base Speed) có tác động quyết định lớn hơn đến xác suất giành chiến thắng?' (Two-sample t-test và Logistic Correlation, đặt alpha = 0.05, tính p-value). Thống kê mô tả phân phối tổng chỉ số BST của các thế hệ Pokémon (Gen 1 đến Gen 9)."),
        ("Chương 3 (Trực quan hóa EDA):", 
         "Line plot (xu hướng tăng trưởng chỉ số BST qua các thế hệ game - Power Creep), Bar chart (Top 10 Pokémon có Usage Rate cao nhất meta), Scatter plot (Attack vs Special Attack phân loại sát thương), Box plot (phân phối Tốc độ theo từng Hệ), Histogram/KDE (phân phối điểm Bulkiness), 3D Plot [HP, Defense, Sp.Def] thể hiện không gian chống chịu, Subplots so sánh đội hình vô địch vs đội hình phổ thông."),
        ("Chương 4 (Machine Learning):", 
         "• Classification (Dự đoán thắng/thua trận đấu): Huấn luyện Random Forest, SVM và AdaBoost trên tương quan đội hình 6v6/4v4 (Độ phủ hệ, tổng chỉ số, lợi thế tốc độ) để dự đoán kết quả trận đấu.\n"
         "• Regression: Dự đoán điểm Elo của người chơi hoặc lượng sát thương gây ra bằng Linear Regression có điều chuẩn Ridge/Lasso.\n"
         "• Clustering: Dùng K-Means + PCA phân nhóm Pokémon thành các vai trò chiến thuật chuẩn giải đấu: Fast Physical Sweeper (Garchomp, Weavile), Special Wall (Blissey), Bulky Water Tank (Toxapex), Hazard Setter (Skarmory)."),
        ("Chương 6 (Hệ thống gợi ý & Chọn Pokémon Tối Ưu Khắc Chế):", 
         "• Thuật toán chọn con tối ưu (Optimal Counter Picker): Dựa trên ma trận tương khắc 18x18 Type Chart và chỉ số Speed. Khi đối thủ đưa ra đội hình, thuật toán quét kho Pokémon để chọn ra vị trí tối ưu vừa kháng được chiêu của đối thủ vừa có chiêu gây sát thương Siêu hiệu quả (Super Effective x2 / x4).\n"
         "• Team Builder Recommender: Áp dụng Collaborative Filtering (Item-Item CF trên ma trận Teammate Synergy của Smogon) để gợi ý các con Pokémon ăn ý nhất bổ sung vào 2 slot còn lại của đội hình người chơi.\n"
         "• Đánh giá: Đo lường độ chính xác gợi ý và tỷ lệ thắng mô phỏng.")
    ]
    for title, desc in bullets_pk:
        p = doc.add_paragraph(style='List Bullet')
        r1 = p.add_run(title + " ")
        r1.bold = True
        r1.font.color.rgb = COLOR_PRIMARY
        p.add_run(desc)

    # -------------------------------------------------------------------------
    # ĐỀ TÀI 4: THỊ TRƯỜNG TCG
    # -------------------------------------------------------------------------
    add_custom_heading("4. Đề tài 4: Thị trường Thẻ bài Chiến thuật TCG & Deck Synergy Optimization", 2)
    p_tcg = doc.add_paragraph()
    p_tcg.add_run("Tên học thuật: ").bold = True
    p_tcg.add_run("Trading Card Game Market Intelligence, Price Forecasting & Competitive Deck Synergy Recommender\n")
    p_tcg.add_run("Ý nghĩa thực tiễn & Điểm nhấn: ").bold = True
    p_tcg.add_run(
        "Thị trường thẻ bài sưu tầm và thi đấu (Yu-Gi-Oh!, Pokémon TCG, Magic: The Gathering) là một thị trường tài chính thu nhỏ "
        "với giá trị giao dịch hàng tỷ USD. Giá thẻ bài biến động cực mạnh theo độ hiếm, tình trạng cấm/hạn chế (Banlist) "
        "và sự thay đổi của meta giải đấu. Đề tài này kết hợp giữa bài toán Phân tích Tài chính/Định giá (Finance/Pricing) "
        "và bài toán Tối ưu hóa bộ bài thi đấu (Synergy Optimization)."
    )

    bullets_tcg = [
        ("Chương 2 (Chuẩn bị dữ liệu):", 
         "Kéo 13,000+ lá bài từ YGOPRODeck API (ID, name, type, race, attribute, atk, def, card_text, card_prices); tải dữ liệu bộ bài top giải đấu. Xử lý các thẻ bài promo thiếu giá; chuẩn hóa Min-Max cho chỉ số ATK/DEF; chuẩn hóa Z-Score cho giá bán theo từng Archetype; PCA giảm chiều ma trận thuộc tính lá bài."),
        ("Chương 5 & 5x (SQL & Pandas):", 
         "CSDL quan hệ chuẩn hóa: Cards (card_id, name, type, atk, def, price, text), Archetypes (archetype_id, name), Decks (deck_id, tournament_name, rank), Deck_Cards (deck_id, card_id, quantity - quan hệ nhiều-nhiều). Truy vấn SQL: GROUP BY tìm Archetype có giá trị bộ bài trung bình đắt nhất có HAVING số lá >= 10; Subquery tìm các lá bài 'Staple' xuất hiện trong > 50% các bộ bài lọt vào Top 8 giải đấu lớn. Pandas: Pivot Table ma trận tương hỗ giữa các cặp lá bài đi kèm."),
        ("Chương 1 (Thống kê & Kiểm định):", 
         "Kiểm định giả thuyết A/B Testing: 'Người giành quyền đi trước (Going 1st) có tỷ lệ thắng ván đấu cao hơn có ý nghĩa thống kê so với người đi sau (Going 2nd) hay không?' (Z-test tỷ lệ 2 phía, alpha = 0.05, p-value). Thống kê mô tả phân phối giá trị thẻ bài theo độ hiếm (Common, Ultra Rare, Secret Rare, Starlight Rare)."),
        ("Chương 3 (Trực quan hóa EDA):", 
         "Line plot (biến động giá của các lá bài meta theo từng mốc công bố Banlist), Bar chart (Top 10 lá bài đắt nhất thị trường), Scatter plot (Tương quan giữa Tỉ lệ sử dụng Usage Rate và Giá thị trường), Box plot (Phân phối giá tiền theo từng độ hiếm để phát hiện Outliers 'thẻ bài tiền triệu'), Histogram/KDE (phân phối độ dài văn bản hiệu ứng), Subplots so sánh cấu trúc bộ bài Aggro vs Control."),
        ("Chương 4 (Machine Learning):", 
         "• Regression (Dự báo giá thẻ bài): Sử dụng Linear Regression kết hợp điều chuẩn Ridge (L2) và Lasso (L1) để dự đoán giá bán của một lá bài dựa trên độ hiếm, chỉ số ATK/DEF, năm phát hành và tần suất xuất hiện trong các bộ bài thắng giải.\n"
         "• Text Classification: Dùng TF-IDF Vectorizer trên đoạn văn bản hiệu ứng (Card Text), áp dụng Multinomial Naive Bayes (với Laplace Add-1) và SVM để tự động phân loại vai trò lá bài: Starter (Kích hoạt combo), Extender (Mở rộng combo), Handtrap (Ngắt quãng đối thủ), Board Breaker (Phá bàn).\n"
         "• Clustering: Dùng K-Means gom cụm các bộ bài thi đấu thành các trường phái: Hyper-Combo, Pure Control, Midrange, Stun."),
        ("Chương 6 (Hệ thống gợi ý & Tối ưu hóa Bộ bài):", 
         "• Content-based Synergy Recommender: Trích xuất đặc trưng văn bản hiệu ứng bằng TF-IDF, tính Cosine Similarity để gợi ý các lá bài có từ khóa combo tương thích (ví dụ: người chơi chọn lá bài có hiệu ứng 'Send to GY', hệ thống gợi ý các lá bài có hiệu ứng 'When sent to GY').\n"
         "• Collaborative Filtering Deck Builder: Xây dựng ma trận Utility Matrix (Card x Deck). Áp dụng Item-Item CF để gợi ý: 'Những người chơi sử dụng lá bài A và B thường trang bị thêm lá bài C nào để tối ưu tỷ lệ rút bài?'.\n"
         "• Đánh giá: Đo lường RMSE và sai số gợi ý trên tập kiểm thử.")
    ]
    for title, desc in bullets_tcg:
        p = doc.add_paragraph(style='List Bullet')
        r1 = p.add_run(title + " ")
        r1.bold = True
        r1.font.color.rgb = COLOR_PRIMARY
        p.add_run(desc)

    # -------------------------------------------------------------------------
    # ĐỀ TÀI 5: BẤT ĐỘNG SẢN & AN CƯ XÃ HỘI (ƯU TIÊN CUỐI CÙNG)
    # -------------------------------------------------------------------------
    add_custom_heading("5. Đề tài 5 (Ưu tiên Cuối cùng - Đề tài Xã hội & Đô thị): Hệ thống Định giá Khách quan, Phát hiện Tin đăng Bất thường & Gợi ý Nơi An cư Phù hợp tại Đô thị Việt Nam", 2)
    p_re = doc.add_paragraph()
    p_re.add_run("Tên học thuật: ").bold = True
    p_re.add_run("Vietnam Urban Housing Intelligence, Anomaly Detection, Machine Learning Fair Valuation & Relocation Recommender\n")
    p_re.add_run("Ý nghĩa thực tiễn & Bối cảnh xã hội: ").bold = True
    p_re.add_run(
        "Thị trường bất động sản và thuê nhà đô thị tại Việt Nam (TP.HCM, Hà Nội) hiện tồn tại nhiều bất cập: "
        "tình trạng 'thổi giá' ảo, tin đăng cò mồi/lừa đảo (Bait listings) gây hoang mang cho người lao động và sinh viên. "
        "Các sàn thương mại như Chợ Tốt hay Batdongsan chỉ hoạt động như bảng tin quảng cáo thu tiền người đăng mà không bảo vệ người thuê. "
        "Đề tài này đóng vai trò một Hệ thống Kiểm định Độc lập: sử dụng Khoa học Dữ liệu để phát hiện tin bất thường, "
        "định giá khách quan bằng AI và gợi ý nơi ở tối ưu nhất theo ngân sách và nhu cầu đời sống."
    )

    add_callout(
        "Nguồn dữ liệu thực tế tại Việt Nam: (1) Chợ Tốt Gateway API (gateway.chotot.com - API mở cung cấp dữ liệu sạch dạng JSON gồm giá, diện tích, tọa độ GPS lat/lon, quận/huyện, mô tả chi tiết); "
        "(2) Alonhadat / Batdongsan.com.vn (cào dữ liệu bằng BeautifulSoup); (3) Kaggle Vietnam Housing Dataset (25,000+ tin rao bán/cho thuê đã chuẩn hóa sẵn).",
        bold_prefix="TÀI NGUYÊN DỮ LIỆU TẠI VIỆT NAM:"
    )

    bullets_re = [
        ("Chương 2 (Data Preparation):", 
         "• Thu thập dữ liệu: Gọi API Chợ Tốt Nhà hoặc cào Alonhadat lấy 5,000+ tin căn hộ/phòng trọ tại TP.HCM (hoặc Hà Nội).\n"
         "• Làm sạch dữ liệu: Xử lý missing values bằng cách điền Median cho số phòng tắm/số tầng; loại bỏ tin thiếu giá hoặc thiếu diện tích. Lọc bỏ các tin rác ngoại lai (nhà 100m² giá 100k VNĐ hoặc giá 10,000 tỷ) bằng phương pháp IQR và Z-score.\n"
         "• Chuẩn hóa: Tính đơn giá don_gia_m2 = price / size; chuẩn hóa Z-score cho đơn giá theo từng quận; chuẩn hóa Min-Max cho diện tích và khoảng cách về thang đo [0, 1].\n"
         "• Giảm chiều: Lấy mẫu phân tầng (Stratified Sampling) theo quận; dùng PCA nén các đặc trưng phụ thành 1 chỉ số 'Quy mô căn nhà'."),
        ("Chương 5 & 5x (Databases, SQL & Pandas):", 
         "• Thiết kế CSDL SQLite/PostgreSQL: Bảng Properties (id, title, body, price, size, price_per_m2, lat, lon, district_id, user_id), Districts (id, name, region), Posters (user_id, phone, account_name, total_posts).\n"
         "• Truy vấn SQL nghiệp vụ: Lệnh DDL tạo bảng khóa chính/ngoại; DML nạp dữ liệu. Viết truy vấn: GROUP BY tính đơn giá trung bình/m² theo từng quận có HAVING COUNT(*) >= 50; JOIN 3 bảng kết nối nhà, quận và người đăng; Subquery tìm các căn nhà rẻ hơn mức trung bình quận nhưng diện tích lớn hơn trung bình; Truy vấn phát hiện Spam tìm số điện thoại đăng trên 30 tin ở 5 quận khác nhau trong ngày.\n"
         "• Xử lý Pandas: Hierarchical Indexing (MultiIndex) theo [Quận, Phường], pivot_table tính ma trận đơn giá giữa các Loại hình nhà (Chung cư, Nhà phố, Phòng trọ) đối chiếu theo từng Quận."),
        ("Chương 1 (Toán cơ sở, Thống kê & Kiểm định giả thuyết):", 
         "• Toán cơ sở & Hình học: Dùng công thức Haversine (tính toán dựa trên vector tọa độ kinh độ/vĩ độ) tính khoảng cách chính xác từ từng căn nhà đến trung tâm (Chợ Bến Thành) hoặc nhà ga Metro số 1 gần nhất.\n"
         "• Thống kê mô tả: Tính Mean, Median, Mode, Variance, Độ lệch chuẩn của giá thuê và diện tích; kiểm tra tính phân phối chuẩn.\n"
         "• Kiểm định giả thuyết thống kê A/B (Tác động của hạ tầng Metro): Đặt giả thuyết khoa học: 'Các căn hộ nằm trong bán kính 1.5 km quanh tuyến Metro số 1 Bến Thành - Suối Tiên có đơn giá thuê cao hơn có ý nghĩa thống kê so với các căn hộ ngoài bán kính này hay không?'. Thiết lập H0: mu_near = mu_far vs H1: mu_near > mu_far, kiểm định Two-sample t-test với alpha = 0.05 và tính p-value."),
        ("Chương 3 (Trực quan hóa EDA với Matplotlib & Seaborn):", 
         "• Line plot: Xu hướng biến động đơn giá thuê (triệu/m²) theo khoảng cách di chuyển từ trung tâm ra ngoại ô.\n"
         "• Bar chart: Top 10 quận có mức giá thuê nhà trọ sinh viên đắt đỏ nhất TP.HCM.\n"
         "• Scatter plot: Mối tương quan tuyến tính giữa Diện tích (m²) và Tổng giá tiền để nhận diện các điểm bất thường.\n"
         "• Box plot: Phân phối đơn giá theo từng quận nhằm phát hiện trực quan các điểm ngoại lai (Outliers - các căn bị thổi giá ảo).\n"
         "• Histogram & Density (KDE): Phân phối tần suất diện tích phòng trọ của sinh viên tại TP.HCM.\n"
         "• 3D Plot: Không gian 3 chiều [Diện tích, Khoảng cách trung tâm, Giá thuê].\n"
         "• Subplots & Annotations: Bảng ghép 4 góc phân tích đa chiều giữa các phân khúc có mũi tên chú thích chỉ vào các điểm dữ liệu bất thường."),
        ("Chương 4 (Machine Learning - Hồi quy định giá, Phân loại tin rác & Phân cụm):", 
         "• Supervised Regression (Định giá khách quan): Dự đoán mức giá thực tế hợp lý bằng Linear Regression có điều chuẩn Ridge (L2) và Lasso (L1) dựa trên diện tích, số phòng, vị trí, khoảng cách Metro. Phân tích phần dư sai số (|y - y_hat|): nếu giá thực tế cao hơn giá AI dự đoán vượt quá 30% -> Cảnh báo căn nhà đang bị thổi giá (Overpriced).\n"
         "• Supervised Classification (Phát hiện tin rác / cò mồi): Dùng TF-IDF Vectorizer trên văn bản bài viết, áp dụng Multinomial Naive Bayes (với Laplace Add-1 smoothing) và Random Forest phân loại tin thành: Tin chính chủ đáng tin cậy vs Tin cò mồi/văn mẫu giật tít lừa đảo.\n"
         "• Unsupervised Clustering (Phân cụm khu vực): Dùng K-Means + PCA gom cụm các khu vực BĐS thành 3 nhóm: Lõi đô thị đắt đỏ, Đô thị mới năng động, Ngoại ô giá rẻ."),
        ("Chương 6 (Hệ thống gợi ý Nơi An cư Tối ưu):", 
         "• Content-based Filtering: Xây dựng Item Profile cho từng căn nhà từ các từ khóa tiện ích (máy lạnh, ban công, an ninh, gác lửng, giờ tự do) bằng TF-IDF. Tính Cosine Similarity với nhu cầu người thuê để xếp hạng gợi ý.\n"
         "• Collaborative Filtering: Item-Item CF trên ma trận tương tác để gợi ý các căn phòng tương tự ở các phường lân cận mà những người có cùng nhu cầu thường lưu lại.\n"
         "• Hybrid Recommender: Kết hợp lọc bán kính khoảng cách tới trường học/công ty (<= 5 km) và ngân sách để đưa ra Top 5 căn nhà an cư lý tưởng nhất. Đánh giá bằng RMSE và MAE.")
    ]
    for title, desc in bullets_re:
        p = doc.add_paragraph(style='List Bullet')
        r1 = p.add_run(title + " ")
        r1.bold = True
        r1.font.color.rgb = COLOR_PRIMARY
        p.add_run(desc)

    # =========================================================================
    # PHẦN III: SO SÁNH & ĐÁNH GIÁ 5 ĐỀ TÀI
    # =========================================================================
    add_custom_heading("PHẦN III: BẢNG SO SÁNH VÀ ĐÁNH GIÁ TRỰC DIỆN 5 ĐỀ TÀI", 1)

    tbl_cmp = doc.add_table(rows=6, cols=6)
    cmp_headers = ["Đề tài", "Độ mới lạ & Cuốn hút", "Độ sẵn có của dữ liệu", "Độ khó kỹ thuật", "Tính năng nổi bật", "Đánh giá chung"]
    for j, h in enumerate(cmp_headers):
        tbl_cmp.cell(0, j).paragraphs[0].text = h

    cmp_rows = [
        ("1. Esports LoL Analytics", "5.0 / 5.0 (Cực hấp dẫn)", "5.0 / 5.0 (Riot Live API + Timeline)", "Vừa sức, số liệu thời gian thực", "Trợ lý Cấm/Chọn AI, Dự đoán Draft + Phút 10, Gợi ý Synergy", "★★★★★ (Ưu tiên 1)"),
        ("2. Spotify Music Playlist", "4.8 / 5.0 (Rất nghệ thuật)", "4.5 / 5.0 (Spotify API + 160k bài)", "Trung bình", "Gợi ý nhạc theo sóng âm & tâm trạng", "★★★★★ (Ưu tiên 2)"),
        ("3. Pokémon Champions VGC", "5.0 / 5.0 (Đậm chất chiến thuật)", "5.0 / 5.0 (PokéAPI + Smogon logs)", "Vừa sức, logic hệ rõ ràng", "Chọn con tối ưu khắc chế & Team Builder", "★★★★★ (Ưu tiên 3)"),
        ("4. Thị trường Thẻ bài TCG", "5.0 / 5.0 (Tài chính & Sưu tầm)", "5.0 / 5.0 (YGOPRODeck API mở 100%)", "Vừa sức, dữ liệu thẻ phong phú", "Dự báo giá thẻ & Tối ưu combo bộ bài", "★★★★★ (Ưu tiên 4)"),
        ("5. BĐS & An cư Đô thị VN", "4.6 / 5.0 (Rất thực tế đời sống)", "5.0 / 5.0 (Chợ Tốt API + Alonhadat)", "Trung bình, cần xử lý tiếng Việt", "AI định giá công bằng, lọc tin ảo", "★★★★★ (Ưu tiên cuối)")
    ]

    for i, row in enumerate(cmp_rows):
        for j, val in enumerate(row):
            tbl_cmp.cell(i+1, j).paragraphs[0].text = val

    style_table(tbl_cmp, [Inches(1.7), Inches(1.1), Inches(1.1), Inches(1.0), Inches(1.6), Inches(1.0)])

    # =========================================================================
    # PHẦN IV: KẾ HOẠCH PHÂN CÔNG & LỘ TRÌNH 6 TUẦN
    # =========================================================================
    add_custom_heading("PHẦN IV: KẾ HOẠCH PHÂN CÔNG CÔNG VIỆC CHO NHÓM 3 THÀNH VIÊN", 1)

    tbl_team = doc.add_table(rows=4, cols=3)
    team_headers = ["Thành viên & Vai trò", "Chương phụ trách", "Nhiệm vụ cụ thể bắt buộc bàn giao"]
    for j, h in enumerate(team_headers):
        tbl_team.cell(0, j).paragraphs[0].text = h

    team_rows = [
        ("Thành viên 1:\nData Engineer & DBA\n(Nhóm trưởng)",
         "Chương 2\nChương 5\nChương 5x",
         "• Viết mã nguồn trích xuất dữ liệu từ Web/API (Riot API / PokéAPI / YGOPRODeck / Spotify / Chợ Tốt API) và nạp dataset mẫu.\n"
         "• Thực hiện quy trình làm sạch dữ liệu khuyết, xử lý ngoại lai (IQR, Z-Score), chuẩn hóa đặc trưng.\n"
         "• Thiết kế lược đồ CSDL quan hệ SQLite/PostgreSQL chuẩn hóa, viết câu lệnh DDL tạo bảng và DML nạp dữ liệu.\n"
         "• Xây dựng ít nhất 4 truy vấn SQL nghiệp vụ phức tạp có JOIN nhiều bảng, GROUP BY, HAVING và Subqueries.\n"
         "• Xây dựng Pipeline Pandas: Lập chỉ mục đa cấp MultiIndex, tạo Pivot Tables ma trận tiện ích."),
        ("Thành viên 2:\nData Scientist &\nStatistician",
         "Chương 1\nChương 3\nChương 4 (Phần 1)",
         "• Thực hiện thống kê mô tả (Mean, Variance, IQR, phân phối chuẩn).\n"
         "• Xây dựng bài toán kiểm định giả thuyết thống kê A/B testing (t-test / Z-test, mức ý nghĩa alpha, tính p-value).\n"
         "• Thiết kế toàn bộ hệ thống bảng biểu trực quan hóa EDA (Line, Bar, Scatter, Box, KDE, 3D, Subplots).\n"
         "• Huấn luyện và đánh giá các mô hình Học máy có giám sát (Supervised): Naive Bayes, SVM, Random Forest, AdaBoost.\n"
         "• Huấn luyện mô hình hồi quy tuyến tính có điều chuẩn Ridge (L2) và Lasso (L1)."),
        ("Thành viên 3:\nRecommender &\nUnsupervised Specialist",
         "Chương 4 (Phần 2)\nChương 6\nBáo cáo & Demo",
         "• Huấn luyện mô hình phân cụm không giám sát K-Means kết hợp thuật toán giảm chiều PCA.\n"
         "• Xây dựng Content-based Recommender: Vector hóa đặc trưng bằng TF-IDF và tính độ tương đồng Cosine Similarity.\n"
         "• Xây dựng Collaborative Filtering (Item-Item hoặc User-User) trên ma trận tiện ích Utility Matrix.\n"
         "• Đo lường hiệu năng của hệ thống gợi ý bằng các chỉ số sai số RMSE, MAE.\n"
         "• Tổng hợp mã nguồn, xây dựng giao diện tương tác Web Demo (Streamlit) và viết báo cáo nghiệm thu hoàn chỉnh.")
    ]

    for i, row in enumerate(team_rows):
        for j, val in enumerate(row):
            tbl_team.cell(i+1, j).paragraphs[0].text = val

    style_table(tbl_team, [Inches(1.8), Inches(1.2), Inches(3.5)])

    # =========================================================================
    # PHẦN V: CHECKLIST KIỂM DUYỆT
    # =========================================================================
    add_custom_heading("PHẦN V: CHECKLIST 12 TIÊU CHÍ KIỂM DUYỆT ĐẠT ĐIỂM TỐI ĐA (60%)", 1)
    checklist_items = [
        "Đã có mã nguồn trích xuất dữ liệu từ Web/API và làm sạch missing/outlier (Chương 2)",
        "Đã lưu dữ liệu vào CSDL quan hệ (SQLite/PostgreSQL) với DDL và ràng buộc khóa chính/ngoại (Chương 5)",
        "Đã có ít nhất 3-5 câu truy vấn SQL phức tạp sử dụng GROUP BY, HAVING, JOIN và Subqueries (Chương 5)",
        "Đã sử dụng các thao tác nâng cao của Pandas: MultiIndex, GroupBy, Pivot Tables (Chương 5x)",
        "Đã thực hiện ít nhất 1 bài toán kiểm định giả thuyết thống kê có đặt H0, H1, mức alpha và tính p-value (Chương 1)",
        "Đã trực quan hóa dữ liệu với đầy đủ các loại đồ thị trong giáo trình: Line, Bar, Scatter, Box, KDE, Subplots (Chương 3)",
        "Đã áp dụng mô hình phân loại (Classification) với ít nhất 2 thuật toán trong slide: Naive Bayes, SVM, Random Forest (Chương 4)",
        "Đã áp dụng mô hình hồi quy (Regression) có kỹ thuật điều chuẩn Ridge hoặc Lasso (Chương 4)",
        "Đã áp dụng mô hình phân cụm K-Means kết hợp thuật toán giảm chiều PCA (Chương 4)",
        "Đã xây dựng hệ thống gợi ý Content-based sử dụng TF-IDF và độ tương đồng Cosine Similarity (Chương 6)",
        "Đã xây dựng hoặc mô phỏng Collaborative Filtering (Item-Item hoặc User-User) trên ma trận tiện ích (Chương 6)",
        "Có bảng so sánh độ đo đánh giá: Accuracy, F1, ROC-AUC cho ML và RMSE, MAE cho Recommender (Chương 4 & 6)"
    ]

    for item in checklist_items:
        p = doc.add_paragraph(style='List Bullet')
        r_box = p.add_run("[ ] ")
        r_box.bold = True
        r_box.font.color.rgb = COLOR_SECONDARY
        p.add_run(item)

    # =========================================================================
    # PHẦN VI: DANH MỤC CÁC CỔNG API MỞ, BỘ DỮ LIỆU & TÀI NGUYÊN KỸ THUẬT
    # =========================================================================
    doc.add_page_break()
    add_custom_heading("PHẦN VI: DANH MỤC CÁC CỔNG API MỞ, BỘ DỮ LIỆU CHUẨN & LINK TRUY CẬP", 1)

    p_api_intro = doc.add_paragraph(
        "Dưới đây là bảng tổng hợp các nguồn dữ liệu, REST API miễn phí và tập dữ liệu benchmark "
        "được phân loại chi tiết theo từng chủ đề. Mỗi chủ đề bao gồm nhiều đường link phục vụ cho từng giai đoạn của đồ án:"
    )

    api_headers = ["Thành phần", "Tên nguồn tài nguyên", "Đường dẫn truy cập (URL)", "Ghi chú & Đặc điểm kỹ thuật"]

    # Bảng API 1: Esports LoL
    add_custom_heading("1. Nguồn tài nguyên cho Đề tài 1: Esports & League of Legends", 2)
    tbl_api_es = doc.add_table(rows=7, cols=4)
    for j, h in enumerate(api_headers):
        tbl_api_es.cell(0, j).paragraphs[0].text = h
    api_es_rows = [
        ("Static CDN API", "Riot Data Dragon", "https://ddragon.leagueoflegends.com/cdn/16.18.1/data/vi_VN/champion.json", "Mở 100%, không cần key. Lấy toàn bộ 173 tướng tiếng Việt, stats, blurb cốt truyện."),
        ("Dynamic API", "Riot Developer Portal", "https://developer.riotgames.com/apis", "Cần Development Key miễn phí. Cung cấp MATCH-V5, MATCH-V5 Timeline, LEAGUE-V4."),
        ("Open Dataset", "Kaggle Diamond Matches", "https://raw.githubusercontent.com/SharnSingh/LeagueOfLegends_Diamond_PredictiveAnalysis/master/high_diamond_ranked_10min.csv", "Tải trực tiếp bằng Pandas. 9,879 trận đấu rank Kim Cương với 40 cột chỉ số mốc 10 phút."),
        ("Web Crawling", "OP.GG Champions", "https://www.op.gg/champions", "Dùng BeautifulSoup cào tỷ lệ thắng, tỷ lệ cấm/chọn và trang bị phổ biến theo patch."),
        ("Pro Play CSV", "Oracle's Elixir", "https://oracleselixir.com/tools/downloads", "Toàn bộ dữ liệu đấu giải chuyên nghiệp (VCS, LCK, LPL, CKTG). Đầy đủ 10 pick, 10 ban, goldat10, player, team."),
        ("Pro Play API", "Leaguepedia Cargo API", "https://lol.fandom.com/api.php", "REST API mở 100%, không cần key. Truy vấn trực tiếp các trận đấu VCS, LCK theo thời gian thực dạng JSON.")
    ]
    for i, row in enumerate(api_es_rows):
        for j, val in enumerate(row):
            tbl_api_es.cell(i+1, j).paragraphs[0].text = val
    style_table(tbl_api_es, [Inches(1.3), Inches(1.5), Inches(2.2), Inches(1.5)])

    # Bảng API 2: Spotify Music
    add_custom_heading("2. Nguồn tài nguyên cho Đề tài 2: Spotify Music Intelligence", 2)
    tbl_api_sp = doc.add_table(rows=4, cols=4)
    for j, h in enumerate(api_headers):
        tbl_api_sp.cell(0, j).paragraphs[0].text = h
    api_sp_rows = [
        ("Web API", "Spotify for Developers", "https://developer.spotify.com/documentation/web-api", "Cung cấp Endpoint Audio Features: danceability, energy, valence, tempo, acousticness."),
        ("Python Lib", "Spotipy Wrapper", "https://spotipy.readthedocs.io/", "Thư viện Python chuẩn kết nối Spotify API nhanh chóng chỉ với 3 dòng code."),
        ("Benchmark Dataset", "Kaggle 160k Tracks", "https://www.kaggle.com/datasets/yamaerenay/spotify-dataset-19212020-160k-tracks", "Tập dữ liệu 160,000+ bài hát từ năm 1921 đến nay với đầy đủ 10 chỉ số sóng âm và Popularity.")
    ]
    for i, row in enumerate(api_sp_rows):
        for j, val in enumerate(row):
            tbl_api_sp.cell(i+1, j).paragraphs[0].text = val
    style_table(tbl_api_sp, [Inches(1.3), Inches(1.5), Inches(2.2), Inches(1.5)])

    # Bảng API 3: Pokémon Champions VGC
    add_custom_heading("3. Nguồn tài nguyên cho Đề tài 3: Competitive Pokémon VGC", 2)
    tbl_api_pk = doc.add_table(rows=5, cols=4)
    for j, h in enumerate(api_headers):
        tbl_api_pk.cell(0, j).paragraphs[0].text = h
    api_pk_rows = [
        ("REST API", "PokéAPI Global", "https://pokeapi.co/api/v2/pokemon?limit=1025", "Mở 100%, không cần key. Đầy đủ 1,025 Pokémon, Base Stats (HP, Atk, Spe), Types, Abilities."),
        ("Type Chart API", "PokéAPI Damage Relations", "https://pokeapi.co/api/v2/type", "Cung cấp ma trận tương khắc 18 hệ để lập trình thuật toán Chọn con tối ưu khắc chế."),
        ("Meta Logs", "Smogon Usage Stats", "https://www.smogon.com/stats/", "Chứa tỉ lệ chọn, moveset và danh sách Teammates đồng đội phục vụ Collaborative Filtering."),
        ("Replay Logs", "Showdown Replays", "https://replay.pokemonshowdown.com/", "Kho dữ liệu hàng triệu trận đấu dạng JSON log để huấn luyện mô hình dự đoán thắng/thua.")
    ]
    for i, row in enumerate(api_pk_rows):
        for j, val in enumerate(row):
            tbl_api_pk.cell(i+1, j).paragraphs[0].text = val
    style_table(tbl_api_pk, [Inches(1.3), Inches(1.5), Inches(2.2), Inches(1.5)])

    # Bảng API 4: Thị trường Thẻ bài TCG
    add_custom_heading("4. Nguồn tài nguyên cho Đề tài 4: Thị trường Thẻ bài Chiến thuật TCG", 2)
    tbl_api_tcg = doc.add_table(rows=5, cols=4)
    for j, h in enumerate(api_headers):
        tbl_api_tcg.cell(0, j).paragraphs[0].text = h
    api_tcg_rows = [
        ("REST API", "pokemontcg.io", "https://api.pokemontcg.io/v2/cards", "15,000+ thẻ bài Pokémon, độ hiếm, giá sàn TCGPlayer và Cardmarket. Key miễn phí 20k req/ngày."),
        ("REST API", "YGOPRODeck API", "https://db.ygoprodeck.com/api/v7/cardinfo.php", "Mở 100%, không cần key. 13,000+ lá bài Yu-Gi-Oh!, ATK/DEF, văn bản hiệu ứng, giá sàn thế giới."),
        ("Decks API", "YGOPRODeck Tournaments", "https://ygoprodeck.com/api/tournament-decks", "Toàn bộ danh sách bộ bài vô địch giải đấu để phân tích ma trận Card x Deck."),
        ("Price Index", "TCGPlayer Marketplace", "https://www.tcgplayer.com/", "Sàn giao dịch định giá thẻ bài lớn nhất thế giới, cung cấp dữ liệu biến động giá phục vụ hồi quy.")
    ]
    for i, row in enumerate(api_tcg_rows):
        for j, val in enumerate(row):
            tbl_api_tcg.cell(i+1, j).paragraphs[0].text = val
    style_table(tbl_api_tcg, [Inches(1.3), Inches(1.5), Inches(2.2), Inches(1.5)])

    # Bảng API 5: Bất động sản Đô thị Việt Nam (MỚI BỔ SUNG Ở ƯU TIÊN CUỐI CÙNG)
    add_custom_heading("5. Nguồn tài nguyên cho Đề tài 5: Bất động sản & An cư Đô thị Việt Nam", 2)
    tbl_api_re = doc.add_table(rows=6, cols=4)
    for j, h in enumerate(api_headers):
        tbl_api_re.cell(0, j).paragraphs[0].text = h
    api_re_rows = [
        ("Public REST API", "Chợ Tốt Gateway API", "https://gateway.chotot.com/v1/public/ad-listing?region_v2=13000&cg=1000", "API mở trả JSON trực tiếp. Có giá (price), diện tích (size), quận/huyện, tọa độ GPS lat/lon, mô tả."),
        ("Web Crawling", "Alonhadat HTML Scraper", "https://alonhadat.com.vn/", "Cấu trúc HTML tĩnh cực kỳ dễ cào bằng BeautifulSoup. Không chặn bot, thẻ phân chia giá và diện tích sạch."),
        ("Web Crawling", "Batdongsan.com.vn", "https://batdongsan.com.vn/", "Sàn thông tin BĐS lớn nhất VN, dùng để cào tin đăng dự án căn hộ và phân tích xu hướng giá thị trường."),
        ("Open Dataset", "Kaggle Vietnam Housing", "https://www.kaggle.com/datasets/hcmc-real-estate-market", "Bộ dữ liệu 25,000+ tin rao bán/cho thuê BĐS tại Hà Nội & TP.HCM được cộng đồng làm sạch sẵn dạng CSV."),
        ("Geo & Amenities API", "OpenStreetMap Overpass API", "https://overpass-turbo.eu/", "Trích xuất tọa độ các tiện ích công cộng (14 ga Metro số 1, bệnh viện, trường học, trạm xe buýt) phục vụ tính khoảng cách.")
    ]
    for i, row in enumerate(api_re_rows):
        for j, val in enumerate(row):
            tbl_api_re.cell(i+1, j).paragraphs[0].text = val
    style_table(tbl_api_re, [Inches(1.3), Inches(1.5), Inches(2.2), Inches(1.5)])

    p_end = doc.add_paragraph()
    p_end.paragraph_format.space_before = Pt(24)
    p_end.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_end = p_end.add_run("--- HẾT BẢN ĐẶC TẢ & TÀI LIỆU TỔNG HỢP ---")
    r_end.font.bold = True
    r_end.font.color.rgb = COLOR_MUTED

    doc.save(output_path)
    print(f"File Word 5 đề tài kèm BĐS VN và Danh mục API đã tạo thành công tại: {output_path}")

if __name__ == "__main__":
    out_file = os.path.abspath("Dac_Ta_De_Tai_Va_Ke_Hoach_Data_Science_PTIT.docx")
    create_full_specialized_project_document(out_file)
