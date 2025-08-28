# pages/07_lab_results_list.py
import os
from datetime import datetime
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Lab Results (List)", layout="wide")
st.title("Lab Results (List)")
st.caption("Browse all uploaded lab result workbooks. Click a row to open details.")

LAB_DIR = "data/lab_results"

def extract_sample_id_quick(xlsx_path: str) -> str | None:
    """
    Light-weight sampler: tries to read first sheet and find a 'Sample ID'
    in long/tidy sheets with columns like ['Field','Value'] (case/spacing tolerant).
    Returns None if not found or file unreadable.
    """
    try:
        xls = pd.ExcelFile(xlsx_path)
        # Try first sheet only for speed
        df = xls.parse(xls.sheet_names[0], nrows=500)
        cols_lower = {c.lower(): c for c in df.columns}
        field_col = next((cols_lower[c] for c in cols_lower if c in {"field", "parameter", "name"}), None)
        value_col = next((cols_lower[c] for c in cols_lower if c in {"value", "result", "data"}), None)
        if field_col and value_col:
            fields = df[field_col].astype(str).str.strip().str.lower().str.replace(r"[_\s]+", " ", regex=True)
            mask = fields.isin(["sample id", "sampleid", "sample id:"])
            if mask.any():
                return df.loc[mask, value_col].astype(str).iloc[0].strip() or None
    except Exception:
        return None
    return None

# Ensure directory exists (don’t crash if missing)
if not os.path.isdir(LAB_DIR):
    st.info(f"Folder not found: `{LAB_DIR}`. Create it and add .xlsx files.")
    st.stop()

# Gather files
files = sorted(
    [f for f in os.listdir(LAB_DIR) if f.lower().endswith(".xlsx")],
    key=lambda x: x.lower()
)

if not files:
    st.warning(f"No Excel files found in `{LAB_DIR}`.")
    st.stop()

# Build table data
rows = []
for fname in files:
    path = os.path.join(LAB_DIR, fname)
    mtime = datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y-%m-%d %H:%M")
    sample_id = extract_sample_id_quick(path) or "—"
    rows.append({"Filename": fname, "Sample ID": sample_id, "Modified": mtime})

df = pd.DataFrame(rows)

# Show list
st.dataframe(df, use_container_width=True, hide_index=True)

st.markdown("### Open a result")
for r in rows:
    cols = st.columns([4, 3, 2, 1])
    cols[0].markdown(f"**{r['Filename']}**")
    cols[1].markdown(f"{r['Sample ID']}")
    cols[2].markdown(f"{r['Modified']}")
    if cols[3].button("Open", key=f"open_{r['Filename']}"):
        # Pass selection via session_state and switch page
        st.session_state["lab_file"] = os.path.join(LAB_DIR, r["Filename"])
        st.switch_page("pages/08_lab_results_detail.py")

st.markdown("---")
st.caption("Tip: drop new Excel files into `data/lab_results/` and refresh.")