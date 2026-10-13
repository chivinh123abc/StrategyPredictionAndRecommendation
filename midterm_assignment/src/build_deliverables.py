"""
build_deliverables.py
Script tự động biên tập và xuất bản bài báo cáo học thuật (Word .docx)
và bộ slide thuyết trình (PowerPoint .pptx) cho Bài tập lớn Giữa kỳ:
Topic 2 - Outlier Detection (TS. Thái Tuyết Hải - PTIT).
"""

from pathlib import Path
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

import pptx
from pptx import Presentation
from pptx.util import Inches as PPT_Inches, Pt as PPT_Pt
from pptx.dml.color import RGBColor as PPT_RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# Thiết lập đường dẫn
BASE_DIR = Path(__file__).resolve().parent.parent
FIGURES_DIR = BASE_DIR / "figures"
REPORT_DIR = BASE_DIR / "report"
SLIDES_DIR = BASE_DIR / "slides"


def set_cell_background(cell, fill_hex):
    """Đặt màu nền cho ô trong bảng Word."""
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tc_pr.append(shd)


def create_word_report():
    """Tạo file báo cáo Word .docx đạt chuẩn học thuật."""
    doc = Document()

    # Thiết lập lề trang tiêu chuẩn (1 inch = 2.54 cm)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # 1. TRANG BÌA (COVER PAGE)
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_inst = p_inst.add_run("HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG\nKHOA CÔNG NGHỆ THÔNG TIN")
    run_inst.font.name = "Times New Roman"
    run_inst.font.size = Pt(14)
    run_inst.font.bold = True
    run_inst.font.color.rgb = RGBColor(16, 44, 87)

    doc.add_paragraph().paragraph_format.space_after = Pt(40)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sub = p_title.add_run("BÀI TẬP LỚN GIỮA KỲ: NHẬP MÔN KHOA HỌC DỮ LIỆU\n\n")
    run_sub.font.name = "Times New Roman"
    run_sub.font.size = Pt(13)
    run_sub.font.bold = True
    run_sub.font.color.rgb = RGBColor(80, 80, 80)

    run_main = p_title.add_run("CHỦ ĐỀ 2: PHÁT HIỆN VÀ XỬ LÝ ĐIỂM NGOẠI LAI\nTRONG PHÂN TÍCH DỮ LIỆU (OUTLIER DETECTION)\n")
    run_main.font.name = "Times New Roman"
    run_main.font.size = Pt(18)
    run_main.font.bold = True
    run_main.font.color.rgb = RGBColor(15, 32, 67)

    run_desc = p_title.add_run("Nghiên cứu thực nghiệm trên 2,304 ván đấu Đấu Giải Chuyên Nghiệp LMHT 2026\n(LCK, LPL, LCP, EWC, MSI)")
    run_desc.font.name = "Times New Roman"
    run_desc.font.size = Pt(12)
    run_desc.font.italic = True
    run_desc.font.color.rgb = RGBColor(40, 116, 166)

    doc.add_paragraph().paragraph_format.space_after = Pt(60)

    # Thông tin sinh viên & giảng viên
    table_info = doc.add_table(rows=4, cols=2)
    table_info.alignment = WD_TABLE_ALIGNMENT.CENTER
    info_data = [
        ("Giảng viên hướng dẫn:", "TS. Thái Tuyết Hải"),
        ("Học phần:", "Nhập môn Khoa học Dữ liệu (Introduction to Data Science)"),
        ("Sinh viên thực hiện:", "[Họ và tên sinh viên] - [Mã sinh viên]"),
        ("Học kỳ / Năm học:", "Học kỳ II - Năm học 2025 - 2026")
    ]
    for row_idx, (k, v) in enumerate(info_data):
        row = table_info.rows[row_idx]
        p_k = row.cells[0].paragraphs[0]
        r_k = p_k.add_run(k)
        r_k.font.name = "Times New Roman"
        r_k.font.bold = True
        r_k.font.size = Pt(11)

        p_v = row.cells[1].paragraphs[0]
        r_v = p_v.add_run(v)
        r_v.font.name = "Times New Roman"
        r_v.font.size = Pt(11)

    doc.add_page_break()

    # 2. TÓM TẮT NỘI DUNG (ABSTRACT)
    h_abs = doc.add_heading("TÓM TẮT NỘI DUNG (ABSTRACT)", level=1)
    h_abs.paragraph_format.space_before = Pt(12)
    p_abs = doc.add_paragraph(
        "Điểm ngoại lai (Outliers) là một trong những bài toán nền tảng của quy trình phân tích và khai phá dữ liệu. "
        "Sự hiện diện của các giá trị cực trị không chỉ bóp méo các đại lượng đo lường vị trí trung tâm (Mean) và độ biến thiên (Standard Deviation) "
        "mà còn làm sai lệch giả định phân phối chuẩn của nhiều mô hình học máy. Báo cáo này trình bày cơ sở lý thuyết toàn diện về khái niệm ngoại lai, "
        "phân biệt rạch ròi giữa ngoại lai thực sự (True Outliers) và dữ liệu sai hỏng do lỗi kỹ thuật (Erroneous Data), đồng thời phân tích các nguyên nhân hình thành.\n\n"
        "Về mặt thực nghiệm, báo cáo tiến hành một nghiên cứu đối sánh thực tế trên 2,304 ván đấu chuyên nghiệp đỉnh cao LMHT mùa giải 2026 "
        "(trích xuất từ các giải đấu LCK, LPL, LCP, EWC, MSI). Ba phương pháp phát hiện ngoại lai được triển khai và kiểm chứng: "
        "Khoảng tứ phân vị (IQR), Điểm số tiêu chuẩn (Z-Score), và Mô hình học máy không giám sát Isolation Forest. "
        "Kết quả chỉ ra rằng Z-Score (|Z| > 3.0) cực kỳ bảo thủ (chỉ gắn cờ 2 điểm - 0.09%) do chính các giá trị cực trị đã thổi phồng độ lệch chuẩn mẫu; "
        "trong khi IQR phát hiện 23 điểm (1.00%) và bảo vệ phân phối tốt hơn. Phân tích định lượng cũng chứng minh rằng việc loại bỏ thô bạo (Trimming) "
        "làm tổn thất thông tin của những trận đấu kinh điển lăn cầu tuyết, và phương pháp Cắt ngọn phân vị (Winsorization 1% - 99%) "
        "là giải pháp tối ưu nhất khi vừa kiểm soát được phương sai vừa giữ nguyên 100% kích thước mẫu và tính trung thực của dữ liệu thể thao điện tử."
    )
    p_abs.paragraph_format.line_spacing = 1.2
    p_abs.paragraph_format.space_after = Pt(14)

    # 3. NỘI DUNG CHÍNH
    def add_section_header(title, level=1):
        h = doc.add_heading(title, level=level)
        h.paragraph_format.space_before = Pt(14)
        h.paragraph_format.space_after = Pt(6)
        return h

    # Section 1
    add_section_header("1. TỔNG QUAN VỀ ĐIỂM NGOẠI LAI (OUTLIERS)")
    p1 = doc.add_paragraph(
        "Theo định nghĩa kinh điển của Hawkins (1980), một điểm ngoại lai (Outlier) là một quan sát sai lệch quá nhiều so với "
        "các quan sát khác trong cùng tập dữ liệu, đến mức làm nảy sinh nghi ngờ rằng nó được tạo ra bởi một cơ chế hoàn toàn khác biệt. "
        "Trong khoa học dữ liệu hiện đại, ngoại lai mang hai bản chất đối lập:\n"
        "• Ngoại lai mang giá trị phát hiện tri thức (Informative Outliers): Phản ánh các hiện tượng đặc biệt, đột biến hiếm gặp nhưng "
        "hoàn toàn có thật trong thế giới thực (ví dụ: giao dịch gian lận ngân hàng, hạt hạ nguyên tử mới, hoặc một trận đấu LMHT mà một đội "
        "áp đảo toàn diện dẫn trước hơn 3,500 vàng ở phút thứ 10).\n"
        "• Ngoại lai phi giá trị (Harmful Noise): Gây nhiễu tín hiệu thống kê, làm mô hình hồi quy bị lệch trọng số hoặc làm thuật toán phân cụm méo mó."
    )

    doc.add_heading("1.1. Phân biệt Ngoại lai và Dữ liệu Sai hỏng", level=2)
    doc.add_paragraph("Bảng đối chiếu tiêu chuẩn phân biệt giữa True Outliers và Erroneous Data:")

    # Table 1: Phân biệt
    tbl_diff = doc.add_table(rows=5, cols=3)
    tbl_diff.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Tiêu chí phân biệt", "Điểm Ngoại Lai Thực Sự (True Outliers)", "Dữ liệu Sai hỏng (Erroneous Data)"]
    for i, h_text in enumerate(headers):
        cell = tbl_diff.rows[0].cells[i]
        cell.paragraphs[0].add_run(h_text).bold = True
        set_cell_background(cell, "2B4C7E")
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)

    diff_rows = [
        ("Bản chất", "Giá trị cực trị nhưng hợp lệ và có thực trong không gian biến thiên.", "Giá trị phi lý, sai lệch hoàn toàn do lỗi ghi nhận kỹ thuật."),
        ("Nguồn gốc", "Biến động tự nhiên cực đoan (Natural Variability), sự kiện ngoại lệ.", "Lỗi cảm biến, gõ nhầm, bug hệ thống trích xuất, mất mạng/Remake."),
        ("Ví dụ LMHT", "Một đội dẫn trước +3,580 vàng lúc 10 phút do khai thác triệt để sai lầm đối phương.", "Trận đấu kéo dài 2 phút do lỗi mạng (Remake) nhưng hệ thống ghi nhận vàng 0."),
        ("Chiến lược xử lý", "Giữ lại, biến đổi log, hoặc cắt ngọn bền vững (Winsorization).", "Bắt buộc loại bỏ hoặc sửa chữa triệt để ngay ở khâu Data Cleaning.")
    ]
    for r_idx, row_vals in enumerate(diff_rows):
        row = tbl_diff.rows[r_idx + 1]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.paragraphs[0].add_run(val)
            if r_idx % 2 == 1:
                set_cell_background(cell, "F2F4F7")

    # Section 2
    add_section_header("2. NGUYÊN NHÂN PHÁT SINH NGOẠI LAI TRONG DỮ LIỆU")
    doc.add_paragraph(
        "Ngoại lai có thể xuất phát từ nhiều khâu trong vòng đời dữ liệu:\n"
        "1. Lỗi con người trong quá trình nhập liệu (Data Entry Errors): Gõ nhầm dấu phẩy, thừa chữ số 0.\n"
        "2. Lỗi thiết bị và đường truyền (Measurement / Network Faults): Mất gói tin, rớt mạng, cảm biến bị hỏng.\n"
        "3. Lỗi tích hợp dữ liệu (ETL Pipeline Bugs): Trộn lẫn đơn vị đo (giây vs mili-giây, mét vs feet).\n"
        "4. Biến động tự nhiên mang tính phân phối đuôi dày (Heavy-tailed Distributions): Phổ biến trong kinh tế, tài chính và thể thao điện tử, "
        "nơi thành công sinh ra lợi thế lũy tiến (quy luật lăn cầu tuyết).\n"
        "Trong LMHT chuyên nghiệp, chênh lệch vàng phút 10 vượt mốc 3,000 thường xảy ra do: Giao tranh cướp rừng cấp 1 (Level 1 Invade) "
        "thành công mang về 3-4 điểm hạ gục sớm, hoặc chiến thuật đảo đường (Lane Swap) bào trọn vẹn giáp trụ."
    )

    # Section 3
    add_section_header("3. CÁC PHƯƠNG PHÁP PHÁT HIỆN NGOẠI LAI")
    doc.add_paragraph(
        "3.1. Phương pháp Khoảng Tứ Phân Vị (IQR - Tukey's Method)\n"
        "IQR là phương pháp phi tham số dựa trên vị trí phân vị: IQR = Q3 - Q1. Ngưỡng phát hiện ngoại lai được xác định bởi "
        "[Q1 - 1.5 * IQR, Q3 + 1.5 * IQR]. Ưu điểm nổi trội là cực kỳ bền vững (Robust), không bị bóp méo bởi chính các giá trị cực trị "
        "và không phụ thuộc vào giả định phân phối chuẩn.\n\n"
        "3.2. Phương pháp Điểm Tiêu Chuẩn (Z-Score)\n"
        "Z-Score đo khoảng cách từ điểm quan sát đến giá trị trung bình theo đơn vị độ lệch chuẩn: Z = (X - Mean) / Std. "
        "Ngưỡng 3-sigma (|Z| > 3.0) được dùng để định danh ngoại lai. Tuy nhiên, Z-Score mắc phải nhược điểm chí mạng là Hiệu ứng che khuất "
        "(Masking Effect): Bản thân Mean và Std bị các ngoại lai thổi phồng, khiến mẫu số Std lớn bất thường và làm cho Z-Score bỏ sót nhiều ngoại lai rõ ràng.\n\n"
        "3.3. Phương pháp Rừng Cô Lập (Isolation Forest - Mở rộng nâng cao)\n"
        "Là thuật toán học máy không giám sát dựa trên giả thuyết: Ngoại lai là những điểm ít và khác biệt, dễ dàng bị cô lập ở những nhánh nông "
        "của cây quyết định ngẫu nhiên. Phương pháp này có tốc độ tuyến tính O(n) và hoạt động xuất sắc trên không gian đa chiều."
    )

    # Section 4 & 5
    add_section_header("4. THỰC NGHIỆM ĐỐI SÁNH TRÊN 2,304 TRẬN ĐẤU LMHT PRO PLAY 2026")
    doc.add_paragraph(
        "Nghiên cứu sử dụng 2,304 trận đấu chuyên nghiệp thuộc các giải đấu LCK, LPL, LCP, EWC, MSI mùa giải 2026. "
        "Biến phân tích trọng tâm là golddiffat10 (chênh lệch vàng lúc 10 phút giữa hai đội). "
        "Đặc trưng ban đầu của tập dữ liệu: Cỡ mẫu N = 2,304; Mean = +98.37 vàng; Median = +86.00 vàng; "
        "Std Dev = 1,171.80 vàng; Khoảng giá trị từ -3,606 đến +3,580 vàng; Độ lệch Skewness = 0.0616; Độ nhọn Kurtosis = -0.0220."
    )

    # Chèn Hình 1
    fig1_file = FIGURES_DIR / "fig1_outlier_detection_iqr_zscore.png"
    if fig1_file.exists():
        doc.add_paragraph().paragraph_format.space_before = Pt(8)
        p_img1 = doc.add_paragraph()
        p_img1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img1.add_run().add_picture(str(fig1_file), width=Inches(6.0))
        p_cap1 = doc.add_paragraph("Hình 1: Phân phối chênh lệch vàng phút 10 và các ngưỡng phát hiện ngoại lai (IQR vs Z-Score)")
        p_cap1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap1.runs[0].font.italic = True
        p_cap1.runs[0].font.size = Pt(10)

    # Bảng kết quả phát hiện
    doc.add_paragraph("Bảng 2: Kết quả nhận diện ngoại lai giữa các phương pháp")
    tbl_res = doc.add_table(rows=4, cols=4)
    tbl_res.alignment = WD_TABLE_ALIGNMENT.CENTER
    res_headers = ["Phương pháp", "Ngưỡng xác định", "Số ngoại lai phát hiện", "Tỷ lệ phát hiện (%)"]
    for i, h_text in enumerate(res_headers):
        cell = tbl_res.rows[0].cells[i]
        cell.paragraphs[0].add_run(h_text).bold = True
        set_cell_background(cell, "2B4C7E")
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)

    res_data = [
        ("Khoảng tứ phân vị (IQR)", "[-2,961.2 vàng, +3,136.8 vàng]", "23", "1.00%"),
        ("Điểm số tiêu chuẩn (Z-Score)", "[-3,417.0 vàng, +3,613.8 vàng]", "2", "0.09%"),
        ("Rừng cô lập (Isolation Forest)", "Anomaly Score < 0 (Contam = 0.03)", "70", "3.04%")
    ]
    for r_idx, row_vals in enumerate(res_data):
        row = tbl_res.rows[r_idx + 1]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.paragraphs[0].add_run(val)
            if r_idx % 2 == 1:
                set_cell_background(cell, "F2F4F7")

    doc.add_paragraph(
        "\nPhân tích đối chiếu chỉ ra: Z-Score chỉ phát hiện được 2 ván đấu có chênh lệch vàng cực đại (-3,606 vàng và +3,580 vàng). "
        "Có tới 21 ván đấu lăn cầu tuyết mạnh mẽ (trong khoảng 2,960 đến 3,400 vàng) bị Z-Score bỏ sót hoàn toàn do độ lệch chuẩn bị đội lên "
        "mức 1,171.80 vàng. Đây là minh chứng thực nghiệm sinh động nhất cho hiện tượng Masking Effect."
    )

    # Chèn Hình 3
    fig3_file = FIGURES_DIR / "fig3_scatter_multivariate_outliers.png"
    if fig3_file.exists():
        p_img3 = doc.add_paragraph()
        p_img3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img3.add_run().add_picture(str(fig3_file), width=Inches(5.8))
        p_cap3 = doc.add_paragraph("Hình 2: Tương quan 2D giữa Chênh lệch Vàng vs Kinh nghiệm và mức độ đồng thuận nhận diện")
        p_cap3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap3.runs[0].font.italic = True
        p_cap3.runs[0].font.size = Pt(10)

    # Section 6
    add_section_header("5. TÁC ĐỘNG CỦA CÁC CHIẾN LƯỢC XỬ LÝ NGOẠI LAI")
    doc.add_paragraph(
        "Nghiên cứu tiến hành đánh giá định lượng 4 chiến lược can thiệp lên tập dữ liệu: "
        "1) Giữ nguyên (Retaining); 2) Loại bỏ theo IQR (Trimming IQR); 3) Loại bỏ theo Z-Score (Trimming Z-Score); "
        "và 4) Cắt ngọn phân vị 1% - 99% (Winsorization)."
    )

    # Bảng tác động thống kê
    tbl_impact = doc.add_table(rows=5, cols=8)
    tbl_impact.alignment = WD_TABLE_ALIGNMENT.CENTER
    imp_headers = ["Chiến lược", "Cỡ mẫu N", "Giữ lại %", "Mean", "Std Dev", "Δ Std %", "Min", "Max"]
    for i, h_text in enumerate(imp_headers):
        cell = tbl_impact.rows[0].cells[i]
        cell.paragraphs[0].add_run(h_text).bold = True
        set_cell_background(cell, "2B4C7E")
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)

    imp_data = [
        ("Gốc (Retaining)", "2,304", "100.0%", "+98.37", "1,171.80", "0.00%", "-3,606.0", "+3,580.0"),
        ("Loại bỏ IQR", "2,281", "99.00%", "+97.43", "1,130.64", "-3.51%", "-2,947.0", "+3,098.0"),
        ("Loại bỏ Z-Score", "2,302", "99.91%", "+101.58", "1,167.24", "-0.39%", "-3,374.0", "+3,580.0"),
        ("Cắt ngọn (Winsorize)", "2,304", "100.0%", "+98.84", "1,156.90", "-1.27%", "-2,702.0", "+2,921.0")
    ]
    for r_idx, row_vals in enumerate(imp_data):
        row = tbl_impact.rows[r_idx + 1]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.paragraphs[0].add_run(val)
            if r_idx % 2 == 1:
                set_cell_background(cell, "F2F4F7")

    # Chèn Hình 2 & 4
    fig2_file = FIGURES_DIR / "fig2_distribution_before_after.png"
    fig4_file = FIGURES_DIR / "fig4_statistical_impact_comparison.png"
    if fig2_file.exists():
        p_img2 = doc.add_paragraph()
        p_img2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img2.add_run().add_picture(str(fig2_file), width=Inches(5.8))
        p_cap2 = doc.add_paragraph("Hình 3: So sánh hàm mật độ xác suất (KDE) trước và sau khi xử lý ngoại lai")
        p_cap2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap2.runs[0].font.italic = True
        p_cap2.runs[0].font.size = Pt(10)

    if fig4_file.exists():
        p_img4 = doc.add_paragraph()
        p_img4.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img4.add_run().add_picture(str(fig4_file), width=Inches(5.8))
        p_cap4 = doc.add_paragraph("Hình 4: Tác động định lượng của 4 chiến lược lên Mean, Độ lệch chuẩn và Biên độ giá trị")
        p_cap4.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap4.runs[0].font.italic = True
        p_cap4.runs[0].font.size = Pt(10)

    # Section 7 & 8
    add_section_header("6. KHUYẾN NGHỊ VÀ KẾT LUẬN")
    doc.add_paragraph(
        "Từ kết quả thực nghiệm, báo cáo đề xuất hướng dẫn thực hành như sau:\n"
        "1. Giữ nguyên (Retaining): Áp dụng khi phân tích các đột biến chiến thuật hoặc phát hiện hiện tượng hiếm.\n"
        "2. Loại bỏ (Trimming): Chỉ áp dụng cho dữ liệu sai hỏng (Erroneous Data). Tuyệt đối không xóa bỏ tùy tiện dữ liệu thật.\n"
        "3. Cắt ngọn (Winsorization 1%-99%): Khuyến nghị hàng đầu khi chuẩn bị dữ liệu huấn luyện học máy (Regression, Neural Networks), "
        "giúp bảo toàn nguyên vẹn cỡ mẫu N = 2,304, triệt tiêu nguy cơ bùng nổ gradient từ các giá trị cực trị mà vẫn phản ánh trung thực cấu trúc dữ liệu.\n"
        "4. Biến đổi dữ liệu (Transformation): Áp dụng log hoặc Box-Cox khi dữ liệu có độ lệch quá lớn."
    )

    # References
    add_section_header("TÀI LIỆU THAM KHẢO")
    refs = [
        "Hawkins, D. M. (1980). Identification of Outliers. Chapman and Hall, London.",
        "Tukey, J. W. (1977). Exploratory Data Analysis. Addison-Wesley.",
        "Liu, F. T., Ting, K. M., & Zhou, Z. H. (2008). Isolation Forest. In 2008 Eighth IEEE International Conference on Data Mining (pp. 413-422).",
        "Rousseeuw, P. J., & Hubert, M. (2011). Robust statistics for outlier detection. Wiley Interdisciplinary Reviews: Data Mining and Knowledge Discovery, 1(1), 73-79.",
        "Oracle's Elixir (2026). League of Legends Esports Match Data. https://oracleselixir.com/",
        "Riot Games API Documentation (2026). LoL Match-v5 & Tournament Endpoints. https://developer.riotgames.com/"
    ]
    for r in refs:
        p_r = doc.add_paragraph(f"[{refs.index(r)+1}] {r}")
        p_r.paragraph_format.left_indent = Inches(0.25)
        p_r.paragraph_format.space_after = Pt(4)

    output_path = REPORT_DIR / "MIDTERM_REPORT_TOPIC2.docx"
    doc.save(output_path)
    print(f"📄 ĐÃ XUẤT BẢN THÀNH CÔNG BÁO CÁO WORD: {output_path.name}")


def create_powerpoint_slides():
    """Tạo bộ slide PowerPoint 16:9 chuyên nghiệp, hiện đại."""
    prs = Presentation()
    # Tỷ lệ 16:9 Widescreen (13.33 x 7.5 inches)
    prs.slide_width = PPT_Inches(13.333)
    prs.slide_height = PPT_Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Bảng màu chủ đạo (Deep Navy, Indigo, Cyan, Slate Gray, Pure White)
    COLOR_BG = PPT_RGBColor(15, 23, 42)          # Slate Dark Navy
    COLOR_CARD = PPT_RGBColor(30, 41, 59)        # Card Navy
    COLOR_TEXT = PPT_RGBColor(241, 245, 249)     # Bright Slate
    COLOR_MUTED = PPT_RGBColor(148, 163, 184)    # Muted Slate
    COLOR_ACCENT = PPT_RGBColor(56, 189, 248)    # Sky Cyan
    COLOR_GOLD = PPT_RGBColor(251, 191, 36)      # Amber Gold
    COLOR_RED = PPT_RGBColor(248, 113, 113)      # Coral Red

    fig1_file = FIGURES_DIR / "fig1_outlier_detection_iqr_zscore.png"
    fig2_file = FIGURES_DIR / "fig2_distribution_before_after.png"
    fig3_file = FIGURES_DIR / "fig3_scatter_multivariate_outliers.png"
    fig4_file = FIGURES_DIR / "fig4_statistical_impact_comparison.png"

    def add_background_and_header(slide, title_text, category_text="NHẬP MÔN KHOA HỌC DỮ LIỆU - PTIT"):
        # Nền tối
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, PPT_Inches(13.333), PPT_Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = COLOR_BG
        bg.line.fill.background()

        # Tiêu đề danh mục
        tb_cat = slide.shapes.add_textbox(PPT_Inches(0.8), PPT_Inches(0.5), PPT_Inches(11.7), PPT_Inches(0.3))
        p_cat = tb_cat.text_frame.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = PPT_Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = COLOR_ACCENT

        # Tiêu đề slide
        tb_t = slide.shapes.add_textbox(PPT_Inches(0.8), PPT_Inches(0.8), PPT_Inches(11.7), PPT_Inches(0.6))
        p_t = tb_t.text_frame.paragraphs[0]
        p_t.text = title_text
        p_t.font.size = PPT_Pt(22)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_TEXT

    # SLIDE 1: BÌA
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, PPT_Inches(13.333), PPT_Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = COLOR_BG
    bg1.line.fill.background()

    tb1 = s1.shapes.add_textbox(PPT_Inches(1.0), PPT_Inches(1.8), PPT_Inches(11.3), PPT_Inches(4.0))
    tf1 = tb1.text_frame
    p1 = tf1.paragraphs[0]
    p1.text = "HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG - KHOA CNTT"
    p1.font.size = PPT_Pt(14)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_ACCENT

    p2 = tf1.add_paragraph()
    p2.text = "PHÁT HIỆN & XỬ LÝ ĐIỂM NGOẠI LAI\n(OUTLIER DETECTION & HANDLING)"
    p2.font.size = PPT_Pt(32)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_TEXT
    p2.space_before = PPT_Pt(15)

    p3 = tf1.add_paragraph()
    p3.text = "Thực nghiệm đối sánh trên 2,304 ván đấu Đấu Giải Chuyên Nghiệp LMHT 2026 (LCK, LPL, MSI, EWC)"
    p3.font.size = PPT_Pt(16)
    p3.font.color.rgb = COLOR_MUTED
    p3.space_before = PPT_Pt(10)

    p4 = tf1.add_paragraph()
    p4.text = "Giảng viên hướng dẫn: TS. Thái Tuyết Hải  |  Sinh viên thực hiện: [Họ và tên] - [MSSV]"
    p4.font.size = PPT_Pt(13)
    p4.font.bold = True
    p4.font.color.rgb = COLOR_GOLD
    p4.space_before = PPT_Pt(30)

    # SLIDE 2: MỤC TIÊU & CÂU HỎI CỐT LÕI
    s2 = prs.slides.add_slide(blank_layout)
    add_background_and_header(s2, "MỤC TIÊU NGHIÊN CỨU & CÂU HỎI THỐNG KÊ")
    
    # 3 Thẻ bài học
    cards = [
        ("1. Bản Chất Ngoại Lai", "Thấu hiểu toán học của Outliers và phân biệt rạch ròi với Dữ liệu Sai hỏng (Erroneous Data). Tránh xóa nhầm tri thức."),
        ("2. Đối Sánh Thuật Toán", "Kiểm chứng thực tế 3 phương pháp: IQR, Z-Score và Isolation Forest trên 2,304 trận đấu Pro Play LMHT 2026."),
        ("3. Cẩm Nang Xử Lý", "Đo lường định lượng tác động lên Mean, Std Dev và Skewness. Đề xuất chiến lược Cắt ngọn (Winsorization) tối ưu.")
    ]
    for idx, (title, desc) in enumerate(cards):
        left = PPT_Inches(0.8 + idx * 4.0)
        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, PPT_Inches(2.0), PPT_Inches(3.7), PPT_Inches(4.5))
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_CARD
        card.line.color.rgb = COLOR_ACCENT
        tf = card.text_frame
        tf.word_wrap = True
        p_h = tf.paragraphs[0]
        p_h.text = title
        p_h.font.size = PPT_Pt(18)
        p_h.font.bold = True
        p_h.font.color.rgb = COLOR_ACCENT
        p_b = tf.add_paragraph()
        p_b.text = desc
        p_b.font.size = PPT_Pt(14)
        p_b.font.color.rgb = COLOR_TEXT
        p_b.space_before = PPT_Pt(15)

    # SLIDE 3: BẢN CHẤT & PHÂN BIỆT
    s3 = prs.slides.add_slide(blank_layout)
    add_background_and_header(s3, "PHÂN BIỆT: NGOẠI LAI THỰC SỰ vs DỮ LIỆU SAI HỎNG")
    
    box_l = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, PPT_Inches(0.8), PPT_Inches(1.8), PPT_Inches(5.6), PPT_Inches(4.8))
    box_l.fill.solid()
    box_l.fill.fore_color.rgb = COLOR_CARD
    box_l.line.color.rgb = COLOR_GOLD
    tf_l = box_l.text_frame
    tf_l.word_wrap = True
    tf_l.paragraphs[0].text = "⭐ ĐIỂM NGOẠI LAI THỰC SỰ (TRUE OUTLIERS)"
    tf_l.paragraphs[0].font.size = PPT_Pt(16)
    tf_l.paragraphs[0].font.bold = True
    tf_l.paragraphs[0].font.color.rgb = COLOR_GOLD
    p_lb = tf_l.add_paragraph()
    p_lb.text = (
        "• Bản chất: Giá trị cực trị nhưng HỢP LỆ và CÓ THẬT trong đời thực.\n\n"
        "• Nguyên nhân: Đột biến tự nhiên, sự kiện ngoại lệ, quy luật lăn cầu tuyết.\n\n"
        "• Ví dụ LMHT: Đội T1 dẫn trước +3,580 vàng lúc 10 phút nhờ ăn trọn trụ đầu và out trình.\n\n"
        "• Giá trị: Mang tính tri thức cao, phản ánh đỉnh cao chiến thuật.\n\n"
        "• Xử lý: Giữ lại, biến đổi hàm số hoặc dùng Winsorization."
    )
    p_lb.font.size = PPT_Pt(13)
    p_lb.font.color.rgb = COLOR_TEXT
    p_lb.space_before = PPT_Pt(12)

    box_r = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, PPT_Inches(6.9), PPT_Inches(1.8), PPT_Inches(5.6), PPT_Inches(4.8))
    box_r.fill.solid()
    box_r.fill.fore_color.rgb = COLOR_CARD
    box_r.line.color.rgb = COLOR_RED
    tf_r = box_r.text_frame
    tf_r.word_wrap = True
    tf_r.paragraphs[0].text = "⚠️ DỮ LIỆU SAI HỎNG (ERRONEOUS DATA)"
    tf_r.paragraphs[0].font.size = PPT_Pt(16)
    tf_r.paragraphs[0].font.bold = True
    tf_r.paragraphs[0].font.color.rgb = COLOR_RED
    p_rb = tf_r.add_paragraph()
    p_rb.text = (
        "• Bản chất: Giá trị PHI LÝ, SAI LỆCH do lỗi kỹ thuật và hệ thống.\n\n"
        "• Nguyên nhân: Lỗi cảm biến, nhập liệu sai, bug API, rớt mạng, mất dữ liệu.\n\n"
        "• Ví dụ LMHT: Ván đấu Remake 2 phút do disconnect nhưng hệ thống vẫn ghi nhận chỉ số 0.\n\n"
        "• Tác hại: Phá hủy tính toàn vẹn của mô hình phân tích.\n\n"
        "• Xử lý: BẮT BUỘC LOẠI BỎ TRIỆT ĐỂ ở khâu Data Cleaning ban đầu."
    )
    p_rb.font.size = PPT_Pt(13)
    p_rb.font.color.rgb = COLOR_TEXT
    p_rb.space_before = PPT_Pt(12)

    # SLIDE 4: IQR vs Z-SCORE (LÝ THUYẾT)
    s4 = prs.slides.add_slide(blank_layout)
    add_background_and_header(s4, "HAI TRƯỜNG PHÁI: PHI THAM SỐ (IQR) vs THAM SỐ (Z-SCORE)")
    
    box4_l = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, PPT_Inches(0.8), PPT_Inches(1.8), PPT_Inches(5.6), PPT_Inches(4.8))
    box4_l.fill.solid()
    box4_l.fill.fore_color.rgb = COLOR_CARD
    box4_l.line.color.rgb = COLOR_ACCENT
    tf4_l = box4_l.text_frame
    tf4_l.word_wrap = True
    tf4_l.paragraphs[0].text = "📊 KHOẢNG TỨ PHÂN VỊ (IQR - TUKEY)"
    tf4_l.paragraphs[0].font.size = PPT_Pt(16)
    tf4_l.paragraphs[0].font.bold = True
    tf4_l.paragraphs[0].font.color.rgb = COLOR_ACCENT
    p4_lb = tf4_l.add_paragraph()
    p4_lb.text = (
        "• Công thức: IQR = Q3 - Q1 | Ngưỡng: [Q1 - 1.5*IQR, Q3 + 1.5*IQR]\n\n"
        "• Bản chất: Dựa trên phân vị vị trí (Non-parametric).\n\n"
        "• Ưu điểm: Bền vững (Robust) hoàn toàn trước các giá trị cực trị. Không đòi hỏi phân phối chuẩn.\n\n"
        "• Nhược điểm: Hệ số 1.5 mang tính kinh nghiệm thực nghiệm."
    )
    p4_lb.font.size = PPT_Pt(13)
    p4_lb.font.color.rgb = COLOR_TEXT
    p4_lb.space_before = PPT_Pt(12)

    box4_r = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, PPT_Inches(6.9), PPT_Inches(1.8), PPT_Inches(5.6), PPT_Inches(4.8))
    box4_r.fill.solid()
    box4_r.fill.fore_color.rgb = COLOR_CARD
    box4_r.line.color.rgb = COLOR_RED
    tf4_r = box4_r.text_frame
    tf4_r.word_wrap = True
    tf4_r.paragraphs[0].text = "📉 ĐIỂM TIÊU CHUẨN (Z-SCORE - 3 SIGMA)"
    tf4_r.paragraphs[0].font.size = PPT_Pt(16)
    tf4_r.paragraphs[0].font.bold = True
    tf4_r.paragraphs[0].font.color.rgb = COLOR_RED
    p4_rb = tf4_r.add_paragraph()
    p4_rb.text = (
        "• Công thức: Z = (X - Mean) / Std | Ngoại lai khi |Z| > 3.0\n\n"
        "• Bản chất: Giả định phân phối chuẩn Gauss (Parametric).\n\n"
        "• LỖI CHE KHUẤT (MASKING EFFECT):\n"
        "  - Chính các ngoại lai cực lớn kéo lệch Mean và THỔI PHỒNG Std.\n"
        "  - Mẫu số Std quá lớn làm Z-Score bị co lại, khiến Z-Score trở nên 'quá trơ' và BỎ SÓT nhiều ngoại lai nghiêm trọng!"
    )
    p4_rb.font.size = PPT_Pt(13)
    p4_rb.font.color.rgb = COLOR_TEXT
    p4_rb.space_before = PPT_Pt(12)

    # SLIDE 5: DỮ LIỆU THỰC NGHIỆM & PHÂN PHỐI GỐC
    s5 = prs.slides.add_slide(blank_layout)
    add_background_and_header(s5, "DỮ LIỆU THỰC NGHIỆM: 2,304 TRẬN ĐẤU LMHT PRO PLAY 2026")
    
    # Text tóm tắt bên trái
    tb5 = s5.shapes.add_textbox(PPT_Inches(0.8), PPT_Inches(1.8), PPT_Inches(5.0), PPT_Inches(4.8))
    tf5 = tb5.text_frame
    tf5.word_wrap = True
    tf5.paragraphs[0].text = "TẬP DỮ LIỆU ĐỈNH CAO THỰC TẾ"
    tf5.paragraphs[0].font.size = PPT_Pt(16)
    tf5.paragraphs[0].font.bold = True
    tf5.paragraphs[0].font.color.rgb = COLOR_ACCENT
    p5_b = tf5.add_paragraph()
    p5_b.text = (
        "• Quy mô: 2,304 ván đấu Đội Xanh từ LCK, LPL, LCP, EWC, MSI 2026.\n\n"
        "• Biến trọng tâm: golddiffat10 (Chênh lệch vàng phút 10).\n\n"
        "• Thống kê mô tả:\n"
        "  - Mean: +98.37 vàng (Đội Xanh có ưu thế nhẹ)\n"
        "  - Median: +86.00 vàng\n"
        "  - Std Dev: 1,171.80 vàng\n"
        "  - Khoảng giá trị: [-3,606 đến +3,580] vàng\n"
        "  - Skewness: 0.0616 (gần đối xứng)\n"
        "  - Kurtosis: -0.0220 (gần phân phối chuẩn)"
    )
    p5_b.font.size = PPT_Pt(13)
    p5_b.font.color.rgb = COLOR_TEXT
    p5_b.space_before = PPT_Pt(10)

    # Hình Fig 1 bên phải
    if fig1_file.exists():
        s5.shapes.add_picture(str(fig1_file), PPT_Inches(6.0), PPT_Inches(1.8), width=PPT_Inches(6.5))

    # SLIDE 6: KẾT QUẢ ĐỐI SÁNH
    s6 = prs.slides.add_slide(blank_layout)
    add_background_and_header(s6, "KẾT QUẢ ĐỐI SÁNH: IQR vs Z-SCORE vs ISOLATION FOREST")
    
    # Bảng kết quả giữa slide
    rows = 4
    cols = 4
    left = PPT_Inches(0.8)
    top = PPT_Inches(1.8)
    width = PPT_Inches(11.7)
    height = PPT_Inches(2.5)
    tbl6 = s6.shapes.add_table(rows, cols, left, top, width, height).table

    headers6 = ["Phương pháp", "Ngưỡng xác định", "Số ngoại lai gắn cờ", "Tỷ lệ phát hiện (%)"]
    for i, h in enumerate(headers6):
        cell = tbl6.cell(0, i)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_CARD
        for p in cell.text_frame.paragraphs:
            p.font.bold = True
            p.font.size = PPT_Pt(14)
            p.font.color.rgb = COLOR_ACCENT

    table_data = [
        ("Khoảng tứ phân vị (IQR)", "[-2,961.2 vàng, +3,136.8 vàng]", "23 ván đấu", "1.00%"),
        ("Điểm số tiêu chuẩn (Z-Score)", "[-3,417.0 vàng, +3,613.8 vàng]", "2 ván đấu", "0.09% (Quá bảo thủ)"),
        ("Rừng cô lập (Isolation Forest)", "Score < 0 (Contam = 0.03)", "70 ván đấu", "3.04% (Đa chiều)")
    ]
    for r_idx, r_data in enumerate(table_data):
        for c_idx, val in enumerate(r_data):
            cell = tbl6.cell(r_idx + 1, c_idx)
            cell.text = val
            for p in cell.text_frame.paragraphs:
                p.font.size = PPT_Pt(13)
                p.font.color.rgb = COLOR_TEXT

    # Hộp đúc kết bên dưới
    box6 = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, PPT_Inches(0.8), PPT_Inches(4.8), PPT_Inches(11.7), PPT_Inches(2.0))
    box6.fill.solid()
    box6.fill.fore_color.rgb = COLOR_CARD
    box6.line.color.rgb = COLOR_GOLD
    tf6 = box6.text_frame
    tf6.word_wrap = True
    tf6.paragraphs[0].text = "💡 PHÁT HIỆN KHOA HỌC THEN CHỐT"
    tf6.paragraphs[0].font.size = PPT_Pt(15)
    tf6.paragraphs[0].font.bold = True
    tf6.paragraphs[0].font.color.rgb = COLOR_GOLD
    p6_b = tf6.add_paragraph()
    p6_b.text = (
        "• Z-Score bỏ sót tới 21 ván đấu lăn cầu tuyết cực lớn vì độ lệch chuẩn mẫu bị đội lên 1,171.80 vàng.\n"
        "• IQR hoàn toàn miễn nhiễm với biến thiên cực đoan, bao quát chính xác 1.00% các trận đấu có tính chất bất thường.\n"
        "• Cả 2 thuật toán chỉ đồng thuận trên đúng 2 ván đấu cực đoan nhất: -3,606 vàng và +3,580 vàng."
    )
    p6_b.font.size = PPT_Pt(13)
    p6_b.font.color.rgb = COLOR_TEXT
    p6_b.space_before = PPT_Pt(6)

    # SLIDE 7: HÌNH ẢNH MINH HỌA ĐA CHIỀU (FIG 3)
    s7 = prs.slides.add_slide(blank_layout)
    add_background_and_header(s7, "KHÔNG GIAN ĐA CHIỀU: VÀNG vs KINH NGHIỆM (FIG 3)")
    if fig3_file.exists():
        s7.shapes.add_picture(str(fig3_file), PPT_Inches(0.8), PPT_Inches(1.6), width=PPT_Inches(7.2))
    tb7 = s7.shapes.add_textbox(PPT_Inches(8.3), PPT_Inches(1.8), PPT_Inches(4.5), PPT_Inches(4.8))
    tf7 = tb7.text_frame
    tf7.word_wrap = True
    tf7.paragraphs[0].text = "SỰ ĐỒNG THUẬN GIỮA CÁC THUẬT TOÁN"
    tf7.paragraphs[0].font.size = PPT_Pt(16)
    tf7.paragraphs[0].font.bold = True
    tf7.paragraphs[0].font.color.rgb = COLOR_ACCENT
    p7_b = tf7.add_paragraph()
    p7_b.text = (
        "• Màu Đỏ: Cả IQR và Z-Score cùng nhận diện (2 trận đấu cực đại).\n\n"
        "• Màu Cam: 21 trận chỉ có IQR nhận diện nhưng Z-Score bỏ sót hoàn toàn.\n\n"
        "• Màu Xanh lá: Isolation Forest phát hiện thêm các trận lệch đồng thời cả Vàng và Kinh nghiệm ở vùng biên.\n\n"
        "• Kết luận: Kết hợp đa chiều giúp bao quát triệt để hiện tượng chiến thuật."
    )
    p7_b.font.size = PPT_Pt(13)
    p7_b.font.color.rgb = COLOR_TEXT
    p7_b.space_before = PPT_Pt(12)

    # SLIDE 8: TÁC ĐỘNG LÊN THƯỚC ĐO THỐNG KÊ (BẢNG SỐ LIỆU)
    s8 = prs.slides.add_slide(blank_layout)
    add_background_and_header(s8, "TÁC ĐỘNG CỦA CÁC CHIẾN LƯỢC XỬ LÝ LÊN MEAN VÀ STD DEV")
    
    # Bảng 4 chiến lược
    tbl8 = s8.shapes.add_table(5, 7, PPT_Inches(0.8), PPT_Inches(1.8), PPT_Inches(11.7), PPT_Inches(3.2)).table
    headers8 = ["Chiến lược xử lý", "Cỡ mẫu (N)", "Giữ lại %", "Mean (vàng)", "Std Dev (vàng)", "Δ Std (%)", "Biên độ [Min, Max]"]
    for i, h in enumerate(headers8):
        cell = tbl8.cell(0, i)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_CARD
        for p in cell.text_frame.paragraphs:
            p.font.bold = True
            p.font.size = PPT_Pt(13)
            p.font.color.rgb = COLOR_ACCENT

    table8_data = [
        ("Gốc (Retaining)", "2,304", "100.0%", "+98.37", "1,171.80", "0.00%", "[-3606, +3580]"),
        ("Xóa bỏ IQR (Trimming)", "2,281", "99.00%", "+97.43", "1,130.64", "-3.51%", "[-2947, +3098]"),
        ("Xóa bỏ Z-Score", "2,302", "99.91%", "+101.58", "1,167.24", "-0.39%", "[-3374, +3580]"),
        ("Cắt ngọn (Winsorize 1%-99%)", "2,304", "100.0%", "+98.84", "1,156.90", "-1.27%", "[-2702, +2921]")
    ]
    for r_idx, r_data in enumerate(table8_data):
        for c_idx, val in enumerate(r_data):
            cell = tbl8.cell(r_idx + 1, c_idx)
            cell.text = val
            for p in cell.text_frame.paragraphs:
                p.font.size = PPT_Pt(12)
                p.font.color.rgb = COLOR_TEXT

    # Kết luận Slide 8
    tb8_bot = s8.shapes.add_textbox(PPT_Inches(0.8), PPT_Inches(5.3), PPT_Inches(11.7), PPT_Inches(1.8))
    tf8_b = tb8_bot.text_frame
    p8_t = tf8_b.paragraphs[0]
    p8_t.text = "🎯 ĐÁNH GIÁ ĐỊNH LƯỢNG:"
    p8_t.font.bold = True
    p8_t.font.size = PPT_Pt(14)
    p8_t.font.color.rgb = COLOR_GOLD
    p8_d = tf8_b.add_paragraph()
    p8_d.text = (
        "1. Trimming theo IQR làm mất 23 ván đấu và giảm 3.51% phương sai mẫu.\n"
        "2. Winsorization (Cắt ngọn) vừa bảo vệ 100% cỡ mẫu N = 2,304, vừa ổn định hóa phương sai (-1.27%) mà không làm lệch Mean!"
    )
    p8_d.font.size = PPT_Pt(13)
    p8_d.font.color.rgb = COLOR_TEXT
    p8_d.space_before = PPT_Pt(4)

    # SLIDE 9: HÌNH ẢNH MINH HỌA TÁC ĐỘNG (FIG 4)
    s9 = prs.slides.add_slide(blank_layout)
    add_background_and_header(s9, "TRỰC QUAN HÓA TÁC ĐỘNG THỐNG KÊ (FIG 2 & FIG 4)")
    if fig4_file.exists():
        s9.shapes.add_picture(str(fig4_file), PPT_Inches(0.8), PPT_Inches(1.6), width=PPT_Inches(6.2))
    if fig2_file.exists():
        s9.shapes.add_picture(str(fig2_file), PPT_Inches(7.2), PPT_Inches(1.6), width=PPT_Inches(5.3))

    # SLIDE 10: KHUYẾN NGHỊ HÀNH ĐỘNG
    s10 = prs.slides.add_slide(blank_layout)
    add_background_and_header(s10, "BẢN ĐỒ CHIẾN LƯỢC XỬ LÝ NGOẠI LAI (RECOMMENDATIONS)")
    
    rec_cards = [
        ("1. GIỮ NGUYÊN (RETAINING)", "Khi nghiên cứu sự kiện hiếm, đột biến chiến thuật hoặc phát hiện gian lận. Xóa bỏ sẽ làm mất tri thức cốt lõi.", COLOR_ACCENT),
        ("2. LOẠI BỎ (TRIMMING)", "CHỈ DÙNG KHI là Dữ liệu Sai hỏng (Erroneous Data / Remake / Lỗi mạng). Tuyệt đối không xóa True Outliers.", COLOR_RED),
        ("3. CẮT NGỌN (WINSORIZING)", "LỰA CHỌN TỐI ƯU cho Machine Learning. Giữ nguyên 100% kích thước mẫu, tránh bùng nổ gradient và ổn định hóa Loss.", COLOR_GOLD),
        ("4. BIẾN ĐỔI (TRANSFORM)", "Áp dụng Log hoặc Box-Cox khi phân phối có độ lệch cực lớn mang tính nhân tính (Multiplicative).", COLOR_TEXT)
    ]
    for idx, (title, desc, c_col) in enumerate(rec_cards):
        top_c = PPT_Inches(1.8 + idx * 1.3)
        c_box = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, PPT_Inches(0.8), top_c, PPT_Inches(11.7), PPT_Inches(1.1))
        c_box.fill.solid()
        c_box.fill.fore_color.rgb = COLOR_CARD
        c_box.line.color.rgb = c_col
        tf_c = c_box.text_frame
        tf_c.word_wrap = True
        p_ch = tf_c.paragraphs[0]
        p_ch.text = title
        p_ch.font.size = PPT_Pt(14)
        p_ch.font.bold = True
        p_ch.font.color.rgb = c_col
        p_cd = tf_c.add_paragraph()
        p_cd.text = desc
        p_cd.font.size = PPT_Pt(12)
        p_cd.font.color.rgb = COLOR_TEXT
        p_cd.space_before = PPT_Pt(3)

    # SLIDE 11: TỔNG KẾT & KẾT LUẬN
    s11 = prs.slides.add_slide(blank_layout)
    add_background_and_header(s11, "TỔNG KẾT BÀI HỌC KINH NGHIỆM")
    
    box11 = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, PPT_Inches(1.5), PPT_Inches(1.8), PPT_Inches(10.3), PPT_Inches(4.8))
    box11.fill.solid()
    box11.fill.fore_color.rgb = COLOR_CARD
    box11.line.color.rgb = COLOR_ACCENT
    tf11 = box11.text_frame
    tf11.word_wrap = True
    tf11.paragraphs[0].text = "3 BÀI HỌC VÀNG TRONG KHOA HỌC DỮ LIỆU"
    tf11.paragraphs[0].font.size = PPT_Pt(18)
    tf11.paragraphs[0].font.bold = True
    tf11.paragraphs[0].font.color.rgb = COLOR_ACCENT
    p11_b = tf11.add_paragraph()
    p11_b.text = (
        "1. Không có thuật toán vạn năng: IQR bền vững hơn Z-Score trên dữ liệu có biến thiên lớn nhờ tính phi tham số.\n\n"
        "2. Đừng vội vàng xóa bỏ ngoại lai: Các trận đấu 'lăn cầu tuyết' phản ánh thế trận thật của thể thao điện tử, xóa bỏ là phá hủy tri thức thực tế.\n\n"
        "3. Kết hợp Toán học với Kiến thức Nghiệp vụ (Domain Knowledge): Quyết định xử lý ngoại lai phải luôn bắt nguồn từ ngữ cảnh thực tế của bài toán."
    )
    p11_b.font.size = PPT_Pt(15)
    p11_b.font.color.rgb = COLOR_TEXT
    p11_b.space_before = PPT_Pt(20)

    # SLIDE 12: KẾT THÚC
    s12 = prs.slides.add_slide(blank_layout)
    bg12 = s12.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, PPT_Inches(13.333), PPT_Inches(7.5))
    bg12.fill.solid()
    bg12.fill.fore_color.rgb = COLOR_BG
    bg12.line.fill.background()

    tb12 = s12.shapes.add_textbox(PPT_Inches(1.0), PPT_Inches(2.5), PPT_Inches(11.3), PPT_Inches(3.0))
    tf12 = tb12.text_frame
    p12_1 = tf12.paragraphs[0]
    p12_1.alignment = PP_ALIGN.CENTER
    p12_1.text = "XIN CHÂN THÀNH CẢM ƠN!"
    p12_1.font.size = PPT_Pt(38)
    p12_1.font.bold = True
    p12_1.font.color.rgb = COLOR_ACCENT

    p12_2 = tf12.add_paragraph()
    p12_2.alignment = PP_ALIGN.CENTER
    p12_2.text = "Cảm ơn TS. Thái Tuyết Hải và các bạn sinh viên đã theo dõi bài thuyết trình."
    p12_2.font.size = PPT_Pt(16)
    p12_2.font.color.rgb = COLOR_MUTED
    p12_2.space_before = PPT_Pt(20)

    output_pptx = SLIDES_DIR / "MIDTERM_SLIDES_TOPIC2.pptx"
    prs.save(output_pptx)
    print(f"📊 ĐÃ XUẤT BẢN THÀNH CÔNG SLIDE POWERPOINT: {output_pptx.name}")


if __name__ == "__main__":
    print("🚀 Bắt đầu quá trình biên tập deliverables...")
    create_word_report()
    create_powerpoint_slides()
    print("🎉 TẤT CẢ DELIVERABLES ĐÃ HOÀN TẤT 100%!")
