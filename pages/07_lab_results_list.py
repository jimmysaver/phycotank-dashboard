import io
from datetime import datetime
from zoneinfo import ZoneInfo

import pandas as pd
import streamlit as st

# PDF generation (pure Python)
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

st.set_page_config(page_title="Lab Results (List)", layout="wide")
st.title("Lab Results (List)")

st.caption("Upload a Celignis (or other) Excel file to preview nicely and export a polished PDF.")

# --- Helper: read Excel into dict of DataFrames ---
def read_excel(file) -> dict[str, pd.DataFrame]:
    xls = pd.ExcelFile(file)
    sheets: dict[str, pd.DataFrame] = {}
    for name in xls.sheet_names:
        df = xls.parse(name)
        # ensure simple, readable dtypes
        for col in df.select_dtypes(include=["float", "int"]).columns:
            # Avoid excessive decimals by rounding
            df[col] = pd.to_numeric(df[col], errors="coerce")
        sheets[name] = df
    return sheets

# --- Helper: DataFrame -> ReportLab Table data (+basic formatting) ---
def df_to_table_block(df: pd.DataFrame, max_rows_for_pdf: int = 60):
    # Convert to list-of-lists with header row
    header = [str(c) for c in df.columns]
    body_rows = df.head(max_rows_for_pdf).fillna("").astype(str).values.tolist()
    data = [header] + body_rows

    tbl = Table(data, repeatRows=1)
    # Base style
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

# --- Helper: build PDF (bytes) from many sheets ---
def build_pdf(sheets: dict[str, pd.DataFrame], title: str) -> bytes:
    buffer = io.BytesIO()
    # Landscape A4 helps wide tables
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        leftMargin=12 * mm,
        rightMargin=12 * mm,
        topMargin=10 * mm,
        bottomMargin=10 * mm,
    )
    styles = getSampleStyleSheet()
    story = []

    now_uk = datetime.now(ZoneInfo("Europe/London")).strftime("%A, %d %B %Y, %H:%M:%S")
    header = Paragraph(f"<b>{title}</b>", styles["Title"])
    sub = Paragraph(f"Generated: {now_uk}", styles["Normal"])

    story += [header, Spacer(1, 4), sub, Spacer(1, 8)]

    sheet_count = len(sheets)
    for i, (sheet_name, df) in enumerate(sheets.items(), start=1):
        story.append(Paragraph(f"<b>Sheet:</b> {sheet_name}", styles["Heading3"]))
        story.append(Spacer(1, 4))
        if df.empty:
            story.append(Paragraph("<i>(No rows)</i>", styles["Normal"]))
        else:
            story.append(df_to_table_block(df))
        if i < sheet_count:
            story.append(PageBreak())

    doc.build(story)
    return buffer.getvalue()

# --- UI: source of data (upload or default) ---
col_u1, col_u2 = st.columns([2, 1])
with col_u1:
    uploaded = st.file_uploader("Upload lab results Excel (.xlsx)", type=["xlsx"], accept_multiple_files=False)
with col_u2:
    use_default = st.toggle("Use default example", value=(uploaded is None), help="Loads data/Celignis_Sample_3344_Analysis_Summary.xlsx")

# Determine file source
file_to_open = None
if uploaded is not None:
    file_to_open = uploaded
elif use_default:
    # Put your example file here in your repo: data/Celignis_Sample_3344_Analysis_Summary.xlsx
    try:
        file_to_open = "data/Celignis_Sample_3344_Analysis_Summary.xlsx"
    except Exception:
        st.warning("Default file not found. Upload an Excel to continue.")

if not file_to_open:
    st.stop()

# --- Load and display sheets in tabs ---
try:
    sheets = read_excel(file_to_open)
except Exception as e:
    st.error(f"Could not read Excel: {e}")
    st.stop()

if not sheets:
    st.warning("No sheets found in the workbook.")
    st.stop()

tab_labels = list(sheets.keys())
tabs = st.tabs(tab_labels)

for tab, name in zip(tabs, tab_labels):
    with tab:
        df = sheets[name]

        # Smart formatting: freeze first few columns if typical 'Sample'/'Parameter'
        st.subheader(name)
        # Show shaped dataframe (Streamlit handles large tables well)
        st.dataframe(df, use_container_width=True)

st.markdown("---")

# --- Downloads: original Excel + generated PDF ---
col_d1, col_d2 = st.columns(2)
with col_d1:
    if uploaded is not None:
        st.download_button(
            label="Download original Excel",
            data=uploaded.getvalue(),
            file_name=uploaded.name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    else:
        try:
            with open(file_to_open, "rb") as f:
                st.download_button(
                    label="Download original Excel",
                    data=f.read(),
                    file_name="Celignis_Sample_3344_Analysis_Summary.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
        except Exception:
            st.warning("Default Excel file not found for download.")

with col_d2:
    try:
        pdf_bytes = build_pdf(sheets, title="Lab Results Summary")
        st.download_button(
            label="Download as PDF",
            data=pdf_bytes,
            file_name="Lab_Results_Summary.pdf",
            mime="application/pdf",
        )
    except Exception as e:
        st.error(f"Could not generate PDF: {e}")