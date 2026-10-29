import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ========== TETAPAN HALAMAN ==========
st.set_page_config(
    page_title="Chart Analysis",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========== CSS: Butang Terapung ==========
st.markdown("""
<style>
div[data-testid="stHorizontalBlock"] > div:first-child {position:fixed; top:8px; left:8px; z-index:999;}
div[data-testid="stHorizontalBlock"] > div:nth-child(2) {position:fixed; top:8px; right:8px; z-index:999;}
div[data-testid="stHorizontalBlock"] > div:nth-child(3) {position:fixed; top:48px; left:8px; z-index:999;}
div[data-testid="stExpander"] {background-color:#f0f2f6; border-radius:10px; padding:12px;}
button[kind="primary"] {width:100% !important;}
</style>
""", unsafe_allow_html=True)

# ========== INISIALISASI SESI ==========
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
                'Hari ini susah, esok akan lebih baik.',
                'Fokus pada matlamat, bukan halangan.'
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

# ========== DATA ANALISIS CONTOH ==========
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

# ========== BAHAGIAN ATAS: 2 CARTA INTERAKTIF ==========
st.markdown('<br>', unsafe_allow_html=True)
st.subheader('📊 Carta Utama — Tekan untuk pilih')

c1, c2 = st.columns(2, gap='medium')

with c1:
    st.markdown('**📈 Carta 1**')
    fig1 = px.line(
        df, x='Tarikh', y='Nilai A',
        color_discrete_sequence=[warna],
        title='Nilai A Masa ke Semasa'
    )
    fig1.update_layout(height=220, margin=dict(l=10, r=10, t=30, b=10))
    st.plotly_chart(fig1, use_container_width=True)
    
    if st.button('✅ Pilih Carta 1', use_container_width=True):
        st.session_state['carta_dipilih'] = 'Carta 1'

with c2:
    st.markdown('**📊 Carta 2**')
    fig2 = px.bar(
        df, x='Tarikh', y='Nilai B',
        color_discrete_sequence=[warna],
        title='Nilai B Mengikut Tarikh'
    )
    fig2.update_layout(height=220, margin=dict(l=10, r=10, t=30, b=10))
    st.plotly_chart(fig2, use_container_width=True)
    
    if st.button('✅ Pilih Carta 2', use_container_width=True):
        st.session_state['carta_dipilih'] = 'Carta 2'

# ========== BAHAGIAN BAWAH: EDIT & CARTA BESAR ==========
st.divider()
st.subheader(f'✏️ Edit Carta — {st.session_state["carta_dipilih"]}')

e1, e2, e3 = st.columns(3)
with e1: nama_carta = st.text_input('Nama Carta', value=st.session_state['carta_dipilih'])
with e2: jenis_papar = st.selectbox('Jenis Paparan', ['Garis', 'Bar'])
with e3: tunjuk_data = st.checkbox('Tunjuk Jadual Data')

# Carta Besar di Ruang Edit
st.markdown(f'### 📈 {nama_carta} — {st.session_state["tf"]}')

if st.session_state['carta_dipilih'] == 'Carta 1':
    y_col = 'Nilai A'
else:
    y_col = 'Nilai B'

if jenis_papar == 'Garis':
    fig_besar = px.line(df, x='Tarikh', y=y_col, color_discrete_sequence=[warna], title=f'{nama_carta} — {y_col}')
else:
    fig_besar = px.bar(df, x='Tarikh', y=y_col, color_discrete_sequence=[warna], title=f'{nama_carta} — {y_col}')

fig_besar.update_layout(height=300, margin=dict(l=10, r=10, t=40, b=10))
st.plotly_chart(fig_besar, use_container_width=True)

# Tunjuk data jika dipilih
if tunjuk_data:
    st.dataframe(df, use_container_width=True, height=150)

st.caption(f'✅ Dikemaskini: {datetime.now().strftime("%d/%m/%Y %H:%M")} | Timeframe: {st.session_state["tf"]}')
