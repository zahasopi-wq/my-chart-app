import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ========== TETAPAN ==========
st.set_page_config(
    page_title="Carta Analisis",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========== DATA CONTOH ==========
@st.cache_data
def buat_data(tarikh_mula, tarikh_akhir):
    tarikh_julat = pd.date_range(start=tarikh_mula, end=tarikh_akhir, freq='D')
    n = len(tarikh_julat)
    
    nilai_a = np.cumsum(np.random.randn(n)) * 5 + 50
    nilai_b = np.cumsum(np.random.randn(n)) * 3 + 40
    buka = 40 + np.cumsum(np.random.randn(n)) * 2
    tinggi = buka + np.random.rand(n) * 5
    rendah = buka - np.random.rand(n) * 5
    tutup = buka + np.random.randn(n) * 3
    
    return pd.DataFrame({
        'Tarikh': tarikh_julat,
        'Nilai A': nilai_a,
        'Nilai B': nilai_b,
        'Buka': buka,
        'Tinggi': tinggi,
        'Rendah': rendah,
        'Tutup': tutup
    })

# ========== MULAI HALAMAN ==========
st.title("📊 Carta Analisis Data")
st.markdown("---")

# ========== BAHAGIAN ATAS: PILIHAN & TARIKH ==========
st.subheader("⚙️ Tetapan & Pilihan")

col1, col2 = st.columns(2)

with col1:
    jenis_carta = st.selectbox(
        "Jenis Carta",
        ["Carta Garis", "Carta Bar", "Carta Lilin (Candlestick)"]
    )
    pilih_data = st.selectbox(
        "Pilih Data",
        ["Nilai A", "Nilai B"]
    )
    tunjuk_jadual = st.checkbox("Tunjuk Jadual Data")

with col2:
    st.markdown("**📅 Pilih Julat Tarikh**")
    tarikh_mula = st.date_input("Tarikh Mula", value=datetime(2024, 1, 1))
    tarikh_akhir = st.date_input("Tarikh Akhir", value=datetime.today())

st.markdown("---")

# ========== BAHAGIAN TENGAH: CARTA ==========
st.subheader("📈 Carta Utama")

df = buat_data(tarikh_mula, tarikh_akhir)

if jenis_carta == "Carta Garis":
    fig = px.line(df, x='Tarikh', y=pilih_data, title=f'{pilih_data} — Carta Garis')
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

elif jenis_carta == "Carta Bar":
    fig = px.bar(df, x='Tarikh', y=pilih_data, title=f'{pilih_data} — Carta Bar')
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

elif jenis_carta == "Carta Lilin (Candlestick)":
    fig = go.Figure(data=[go.Candlestick(
        x=df['Tarikh'],
        open=df['Buka'],
        high=df['Tinggi'],
        low=df['Rendah'],
        close=df['Tutup'],
        name='Harga'
    )])
    fig.update_layout(
        title='Carta Lilin (Candlestick)',
        xaxis_title='Tarikh',
        yaxis_title='Nilai',
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ========== BAHAGIAN BAWAH: JADUAL & CHAT ==========
bawah1, bawah2 = st.columns(2)

with bawah1:
    if tunjuk_jadual:
        st.subheader("📋 Jadual Data")
        st.dataframe(df, use_container_width=True, height=250)

with bawah2:
    st.subheader("💬 Chat")
    mesej_pengguna = st.text_input("Taip mesej...", placeholder="Tulis di sini")
    if st.button("Hantar Mesej", use_container_width=True):
        st.info(f"Awak: {mesej_pengguna}")
        st.success("Mesej dihantar!")

st.markdown("---")
st.caption(f'✅ Dikemaskini: {datetime.now().strftime("%d/%m/%Y %H:%M")}')
