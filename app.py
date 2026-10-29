import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

# ========== TETAPAN ==========
st.set_page_config(
    page_title="Carta Analisis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== DATA CONTOH ==========
@st.cache_data
def buat_data():
    tarikh = pd.date_range(start='2024-01-01', periods=30, freq='D')
    nilai_a = np.cumsum(np.random.randn(30)) * 5 + 50
    nilai_b = np.cumsum(np.random.randn(30)) * 3 + 40
    
    # Data untuk Carta Lilin (Candlestick)
    buka = 40 + np.cumsum(np.random.randn(30)) * 2
    tinggi = buka + np.random.rand(30) * 5
    rendah = buka - np.random.rand(30) * 5
    tutup = buka + np.random.randn(30) * 3
    
    return pd.DataFrame({
        'Tarikh': tarikh,
        'Nilai A': nilai_a,
        'Nilai B': nilai_b,
        'Buka': buka,
        'Tinggi': tinggi,
        'Rendah': rendah,
        'Tutup': tutup
    })

df = buat_data()

# ========== MULAI HALAMAN ==========
st.title("📊 Carta Analisis Data")
st.markdown("---")

# ========== BAHAGIAN PILIHAN ==========
st.subheader("Pilihan Carta")

col1, col2, col3 = st.columns(3)
with col1:
    jenis_carta = st.selectbox(
        "Jenis Carta",
        ["Carta Garis", "Carta Bar", "Carta Lilin (Candlestick)"]
    )
with col2:
    pilih_data = st.selectbox(
        "Pilih Data",
        ["Nilai A", "Nilai B"]
    )
with col3:
    tunjuk_jadual = st.checkbox("Tunjuk Jadual Data")

st.markdown("---")

# ========== BAHAGIAN CARTA BESAR ==========
st.subheader("Carta Utama")

if jenis_carta == "Carta Garis":
    fig = px.line(df, x='Tarikh', y=pilih_data, title=f'{pilih_data} — Carta Garis')
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

elif jenis_carta == "Carta Bar":
    fig = px.bar(df, x='Tarikh', y=pilih_data, title=f'{pilih_data} — Carta Bar')
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

elif jenis_carta == "Carta Lilin (Candlestick)":
    import plotly.graph_objects as go
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

# ========== BAHAGIAN JADUAL DATA ==========
if tunjuk_jadual:
    st.subheader("📋 Jadual Data")
    st.dataframe(df, use_container_width=True, height=300)

st.caption(f'Dikemaskini: {datetime.now().strftime("%d/%m/%Y %H:%M")}')
