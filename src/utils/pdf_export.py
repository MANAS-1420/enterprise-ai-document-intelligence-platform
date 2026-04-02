import tempfile
from fpdf import FPDF

def export_report_to_pdf(
    doc_type: str,
    summary: str,
    insights: str,
    risks: str,
    clauses: str,
    comparison: str = ""
) -> str:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=12)
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 16)
    pdf.multi_cell(0, 10, "Enterprise AI Document Intelligence Report")

    pdf.ln(4)
    pdf.set_font("Helvetica", "", 11)

    sections = [
        ("Document Type", doc_type or "Not generated."),
        ("Executive Summary", summary or "Not generated."),
        ("Key Insights", insights or "Not generated."),
        ("Risk Analysis", risks or "Not generated."),
        ("Clause Extraction", clauses or "Not generated."),
    ]

    if comparison:
        sections.append(("Comparison", comparison))

    for title, content in sections:
        pdf.set_font("Helvetica", "B", 13)
        pdf.multi_cell(0, 8, title)
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 6, content)
        pdf.ln(3)

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_file.name)
    return temp_file.name