import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

# ========== TETAPAN HALAMAN ==========
st.set_page_config(
    page_title="Chart Analysis",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========== CSS: YANG DIUBAH = 260px ==========
st.markdown("""
<style>
.block-container {
    padding-top: 260px !important;
    padding-left: 15px !important;
    padding-right: 15px !important;
}

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

# ========== SIMPAN SETTING ==========
if 'warna' not in st.session_state:
    st.session_state['warna'] = '#1f77b4'
if 'carta_dipilih' not in st.session_state:
    st.session_state['carta_dipilih'] = 'Carta 1'
if 'tf' not in st.session_state:
    st.session_state['tf'] = '1M'
if 'tarikh_mula' not in st.session_state:
    st.session_state['tarikh_mula'] = datetime(2024, 1, 1)
if 'tarikh_akhir' not in st.session_state:
    st.session_state['tarikh_akhir'] = datetime.today()

# ========== BUTANG TERAPUNG ==========
col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
with col_btn1: setting_buka = st.button('⚙️ Settings', use_container_width=True)
with col_btn2: menu_buka = st.button('📋 Menu', use_container_width=True)
with col_btn3: chat_buka = st.button('💬 Chat', use_container_width=True)

# ========== PANEL SETTINGS ==========
if setting_buka:
    with st.expander('⚙️ Tetapan', expanded=True):
        st.session_state['warna'] = st.color_picker('Pilih Warna Carta', st.session_state['warna'])

# ========== PANEL MENU ==========
if menu_buka:
    with st.expander('📋 Pilihan Menu', expanded=True):
        menu_pilih = st.radio('Pilih', ['💬 Quotes', '⏱️ Timeframe', '📅 Tarikh'], label_visibility='collapsed')
        
        if menu_pilih == '💬 Quotes':
            quotes = [
                'Kejayaan bermula dengan langkah pertama.',
                'Jangan berhenti bila penat, berhenti bila selesai.',
                'Hari ini susah, esok akan lebih baik.'
            ]
            st.info(np.random.choice(quotes))
        
        elif menu_pilih == '⏱️ Timeframe':
            st.session_state['tf'] = st.select_slider('Tempoh', ['1H', '1W', '1M', '3M', '6M', '1T'])
            st.success(f'Dipilih: {st.session_state["tf"]}')
        
        elif menu_pilih == '📅 Tarikh':
            st.session_state['tarikh_mula'] = st.date_input('Tarikh Mula', st.session_state['tarikh_mula'])
            st.session_state['tarikh_akhir'] = st.date_input('Tarikh Akhir', st.session_state['tarikh_akhir'])
            st.success(f'{st.session_state["tarikh_mula"]} — {st.session_state["tarikh_akhir"]}')

# ========== PANEL CHAT ==========
if chat_buka:
    with st.expander('💬 Chat', expanded=True):
        mesej = st.text_input('Taip mesej...', placeholder='Tulis di sini')
        if st.button('Hantar', use_container_width=True):
            st.write(f'Awak: {mesej}')

# ========== RUANG KOSONG TAMBAHAN ==========
st.markdown('<br><br><br><br><br>', unsafe_allow_html=True)

# ========== DATA CONTOH ==========
@st.cache_data
def buat_data():
    tarikh = pd.date_range(start='2024-01-01', periods=30, freq='D')
    nilai_a = np.cumsum(np.random.randn(30)) * 5 + 50
    nilai_b = np.cumsum(np.random.randn(30)) * 3 + 40
    return pd.DataFrame({
        'Tarikh': tarikh,
        'Nilai A': nilai_a,
        'Nilai B': nilai_b
    })

df = buat_data()
warna = st.session_state['warna']

# ========== BAHAGIAN CARTA ==========
st.subheader('📊 Carta Utama')
st.markdown('---')

# Carta 1
st.markdown('**📈 Carta 1 — Tekan untuk pilih**')
fig1 = px.line(df, x='Tarikh', y='Nilai A', color_discrete_sequence=[warna])
fig1.update_layout(height=240, margin=dict(l=10, r=10, t=20, b=10))
st.plotly_chart(fig1, use_container_width=True)
if st.button('✅ Pilih Carta 1', use_container_width=True):
    st.session_state['carta_dipilih'] = 'Carta 1'

st.markdown('<br>', unsafe_allow_html=True)

# Carta 2
st.markdown('**📊 Carta 2 — Tekan untuk pilih**')
fig2 = px.bar(df, x='Tarikh', y='Nilai B', color_discrete_sequence=[warna])
fig2.update_layout(height=240, margin=dict(l=10, r=10, t=20, b=10))
st.plotly_chart(fig2, use_container_width=True)
if st.button('✅ Pilih Carta 2', use_container_width=True):
    st.session_state['carta_dipilih'] = 'Carta 2'

st.markdown('<br>', unsafe_allow_html=True)
st.markdown('---')

# ========== BAHAGIAN EDIT CARTA ==========
st.subheader(f'✏️ Edit Carta — {st.session_state["carta_dipilih"]}')

e1, e2, e3 = st.columns(3)
with e1: nama_carta = st.text_input('Nama Carta', value=st.session_state['carta_dipilih'])
with e2: jenis_papar = st.selectbox('Jenis Paparan', ['Garis', 'Bar'])
with e3: tunjuk_data = st.checkbox('Tunjuk Jadual Data')

st.markdown('<br>', unsafe_allow_html=True)
st.markdown(f'### 📈 {nama_carta} — {st.session_state["tf"]}')

# Carta Besar di Bahagian Bawah
y_col = 'Nilai A' if st.session_state['carta_dipilih'] == 'Carta 1' else 'Nilai B'
if jenis_papar == 'Garis':
    fig_besar = px.line(df, x='Tarikh', y=y_col, color_discrete_sequence=[warna])
else:
    fig_besar = px.bar(df, x='Tarikh', y=y_col, color_discrete_sequence=[warna])
fig_besar.update_layout(height=280, margin=dict(l=10, r=10, t=20, b=10))
st.plotly_chart(fig_besar, use_container_width=True)

if tunjuk_data:
    st.dataframe(df, use_container_width=True, height=150)

st.caption(f'✅ Dikemaskini: {datetime.now().strftime("%d/%m/%Y %H:%M")} | Timeframe: {st.session_state["tf"]}')
