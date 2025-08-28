# pages/08_lab_results_detail.py

import io
import os
from datetime import datetime
from zoneinfo import ZoneInfo

import pandas as pd
import streamlit as st

# PDF generation (pure Python)
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

st.set_page_config(page_title="Lab Results (Detail)", layout="wide")
st.title("Lab Results (Detail)")

# ---- Back to list ----
back_col, _ = st.columns([1, 5])
with back_col:
    if st.button("← Back to Lab Results (List)", use_container_width=True):
        # Clear selection (optional) then go back
        st.session_state.pop("lab_file", None)
        st.switch_page("pages/07_lab_results_list.py")

LAB_DIR = "data/lab_results"

# ---------- Helpers ----------
def read_excel(file) -> dict[str, pd.DataFrame]:
    xls = pd.ExcelFile(file)
    sheets: dict[str, pd.DataFrame] = {}
    for name in xls.sheet_names:
        df = xls.parse(name)
        for col in df.select_dtypes(include=["float", "int"]).columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        sheets[name] = df
    return sheets

def df_to_table_block(df: pd.DataFrame, max_rows_for_pdf: int = 60):
    header = [str(c) for c in df.columns]
    body_rows = df.head(max_rows_for_pdf).fillna("").astype(str).values.tolist()
    data = [header] + body_rows

    tbl = Table(data, repeatRows=1)
    style = TableStyle([
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2F3B52")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.HexColor("#F7F9FC")]),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#D3DAE6")),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ])
    tbl.setStyle(style)
    return tbl

def build_pdf(sheets: dict[str, pd.DataFrame], title: str) -> bytes:
    """
    Portrait A4 PDF. Footer on every page. Logo only on last page, left-aligned.
    """
    buffer = io.BytesIO()

    class NumberedCanvas(canvas.Canvas):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._saved_page_states = []

        def showPage(self):
            self._saved_page_states.append(dict(self.__dict__))
            self._startPage()

        def save(self):
            num_pages = len(self._saved_page_states)
            for state in self._saved_page_states:
                self.__dict__.update(state)
                self.draw_page_footer(num_pages)
                super().showPage()
            super().save()

        def draw_page_footer(self, num_pages: int):
            width, height = A4
            y = 8 * mm
            x = 12 * mm

            footer_text = (
                "admin@nellie.tech  |  The information contained is private and confidential. "
                "All rights reserved."
            )
            self.setFont("Helvetica", 7)
            self.drawString(x, y + 5, footer_text)

            if self._pageNumber == num_pages:
                logo_path = "assets/nellie_wordmark.png"
                if os.path.exists(logo_path):
                    logo = ImageReader(logo_path)
                    self.drawImage(
                        logo,
                        x,
                        y + 12,
                        width=60 * mm,
                        preserveAspectRatio=True,
                        mask="auto",
                    )

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=12 * mm,
        rightMargin=12 * mm,
        topMargin=10 * mm,
        bottomMargin=18 * mm,
    )
    styles = getSampleStyleSheet()
    story = []

    now_uk = datetime.now(ZoneInfo("Europe/London")).strftime("%A, %d %B %Y, %H:%M:%S")
    story += [
        Paragraph(f"<b>{title}</b>", styles["Title"]),
        Spacer(1, 4),
        Paragraph(f"Generated: {now_uk}", styles["Normal"]),
        Spacer(1, 8),
    ]

    sheet_names = list(sheets.keys())
    for i, sheet_name in enumerate(sheet_names, start=1):
        df = sheets[sheet_name]
        story.append(Paragraph(f"<b>Sheet:</b> {sheet_name}", styles["Heading3"]))
        story.append(Spacer(1, 4))
        story.append(Paragraph("<i>(No rows)</i>", styles["Normal"]) if df.empty else df_to_table_block(df))
        if i < len(sheet_names):
            story.append(PageBreak())

    doc.build(story, canvasmaker=NumberedCanvas)
    return buffer.getvalue()

def extract_sample_id(sheets: dict[str, pd.DataFrame]) -> str | None:
    possible_field_cols = {"field", "parameter", "name"}
    possible_value_cols = {"value", "result", "data"}

    for df in sheets.values():
        cols_lower = {c.lower(): c for c in df.columns}
        field_col = next((cols_lower[c] for c in cols_lower if c in possible_field_cols), None)
        value_col = next((cols_lower[c] for c in cols_lower if c in possible_value_cols), None)
        if field_col and value_col:
            fields = df[field_col].astype(str).str.strip().str.lower().str.replace(r"[_\s]+", " ", regex=True)
            mask = fields.isin(["sample id", "sampleid", "sample id:"])
            if mask.any():
                val = df.loc[mask, value_col].astype(str).iloc[0].strip()
                return val or None
    return None

# ---------- Source selection ----------
file_to_open = st.session_state.get("lab_file")

if not file_to_open:
    st.info("No file selected. Choose a workbook from the list below.")
    if not os.path.isdir(LAB_DIR):
        st.stop()
    options = sorted([f for f in os.listdir(LAB_DIR) if f.lower().endswith(".xlsx")])
    if options:
        choice = st.selectbox("Select a lab results workbook", options)
        if st.button("Open selected"):
            st.session_state["lab_file"] = os.path.join(LAB_DIR, choice)
            st.rerun()
    st.stop()

st.caption(f"Viewing: `{os.path.basename(file_to_open)}`")

# ---------- Load & show ----------
try:
    sheets = read_excel(file_to_open)
except Exception as e:
    st.error(f"Could not read Excel: {e}")
    st.stop()

if not sheets:
    st.warning("No sheets found in the workbook.")
    st.stop()

tabs = st.tabs(list(sheets.keys()))
for tab, name in zip(tabs, sheets.keys()):
    with tab:
        st.subheader(name)
        st.dataframe(sheets[name], use_container_width=True)

st.markdown("---")

# ---------- Downloads ----------
col_d1, col_d2 = st.columns(2)

# Excel download
with col_d1:
    try:
        with open(file_to_open, "rb") as f:
            st.download_button(
                label="Download original Excel",
                data=f.read(),
                file_name=os.path.basename(file_to_open),
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
    except Exception:
        st.warning("Original Excel file not found for download.")

# PDF download — filename = Sample ID (if found), else fallback
with col_d2:
    try:
        sample_id = extract_sample_id(sheets)
        pdf_filename = f"{sample_id}.pdf" if sample_id else "Lab_Results_Summary.pdf"

        pdf_bytes = build_pdf(sheets, title="Lab Results Summary")
        st.download_button(
            label="Download as PDF",
            data=pdf_bytes,
            file_name=pdf_filename,
            mime="application/pdf",
        )
    except Exception as e:
        st.error(f"Could not generate PDF: {e}")