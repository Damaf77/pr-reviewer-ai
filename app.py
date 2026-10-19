
import streamlit as st
from static_analyzer import analyze_python

st.set_page_config(
    page_title="PR Reviewer AI",
    page_icon="🔎",
)

st.title("PR Reviewer AI")
st.caption("Prototype code review untuk Python")

code = st.text_area(
    "Masukkan kode Python",
    height=250,
    value="""def average(total, count):
    return total / count
""",
)

if st.button("Jalankan static analysis"):
    try:
        findings = analyze_python(code)

        if findings:
            st.write(f"Ditemukan {len(findings)} temuan.")
            st.dataframe(findings, use_container_width=True)
        else:
            st.success("Tidak ada pelanggaran aturan Ruff.")
    except Exception as error:
        st.error(f"Analisis gagal: {error}")
