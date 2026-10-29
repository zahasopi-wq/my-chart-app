st.markdown("""
<style>
/* Ruang kosong di atas supaya butang terapung tidak tutup kandungan */
.block-container {
    padding-top: 130px !important;
    padding-left: 15px !important;
    padding-right: 15px !important;
}

/* Butang terapung */
div[data-testid="stHorizontalBlock"] > div:nth-child(1) {
    position: fixed;
    top: 12px;
    left: 12px;
    z-index: 999;
}

div[data-testid="stHorizontalBlock"] > div:nth-child(2) {
    position: fixed;
    top: 12px;
    right: 12px;
    z-index: 999;
}

div[data-testid="stHorizontalBlock"] > div:nth-child(3) {
    position: fixed;
    top: 58px;
    left: 12px;
    z-index: 999;
}

div[data-testid="stExpander"] {
    background-color: #f0f2f6;
    border-radius: 10px;
    padding: 12px;
}

button[kind="primary"] {
    width: 100% !important;
}
</style>
""", unsafe_allow_html=True)
