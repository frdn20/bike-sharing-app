import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

@st.cache_data
def load_data():
    day_df = pd.read_csv('day_data.csv')
    hour_df = pd.read_csv('hour_data.csv')
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    return day_df, hour_df

day_df, hour_df = load_data()

st.sidebar.title("Navigasi Dashboard")
page = st.sidebar.selectbox(
    "Pilih Halaman:",
    ["Tampilkan Data", "Analisis Musiman & Bulanan", "Analisis Tahunan"]
)

if page == "Tampilkan Data":
    st.title("Tampilkan Data")
    st.write("Dataset Bike Sharing")
    

    st.dataframe(day_df)

    st.write("Informasi Dataset:")
    st.write(day_df.describe())

elif page == "Analisis Musiman & Bulanan":
    st.title("Analisis Musiman & Bulanan")
    
    st.subheader("Rata-rata Penyewaan Sepeda Berdasarkan Musim")
    season_labels = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    season_data = day_df.groupby('season')['cnt'].mean().reset_index()
    season_data['season_label'] = season_data['season'].map(season_labels)
    
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(data=season_data, x='season_label', y='cnt', palette='Set2', ax=ax)
    ax.set_title("Rata-rata Penyewaan Berdasarkan Musim", fontsize=16)
    ax.set_xlabel("Musim", fontsize=12)
    ax.set_ylabel("Rata-rata Penyewaan", fontsize=12)
    st.pyplot(fig)
    
    st.subheader("Rata-rata Penyewaan Sepeda Berdasarkan Bulan")
    monthly_data = day_df.groupby('mnth')['cnt'].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=monthly_data, x='mnth', y='cnt', palette='Blues_d', ax=ax)
    ax.set_title("Rata-rata Penyewaan Berdasarkan Bulan", fontsize=16)
    ax.set_xlabel("Bulan", fontsize=12)
    ax.set_ylabel("Rata-rata Penyewaan", fontsize=12)
    ax.set_xticks(range(12))
    ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
    st.pyplot(fig)

elif page == "Analisis Tahunan":
    st.title("Analisis Tahunan")
    

    st.subheader("Rata-rata Penyewaan Sepeda Berdasarkan Tahun")
    yearly_data = day_df.groupby('yr')['cnt'].mean().reset_index()
    yearly_data['yr_label'] = yearly_data['yr'].map({0: "2011", 1: "2012"})
    
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(data=yearly_data, x='yr_label', y='cnt', palette='coolwarm', ax=ax)
    ax.set_title("Rata-rata Penyewaan Berdasarkan Tahun", fontsize=16)
    ax.set_xlabel("Tahun", fontsize=12)
    ax.set_ylabel("Rata-rata Penyewaan", fontsize=12)
    st.pyplot(fig)
    
    st.subheader("Tren Penyewaan Bulanan (2011 vs 2012)")
    monthly_yearly_data = day_df.groupby(['yr', 'mnth'])['cnt'].mean().reset_index()
    monthly_yearly_data['yr_label'] = monthly_yearly_data['yr'].map({0: "2011", 1: "2012"})
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=monthly_yearly_data, x='mnth', y='cnt', hue='yr_label', palette='coolwarm', marker="o", ax=ax)
    ax.set_title("Tren Penyewaan Bulanan (2011 vs 2012)", fontsize=16)
    ax.set_xlabel("Bulan", fontsize=12)
    ax.set_ylabel("Rata-rata Penyewaan", fontsize=12)
    ax.legend(title="Tahun", labels=["2011", "2012"])
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
    st.pyplot(fig)
    
    st.subheader("Tren Kumulatif Penyewaan Sepeda")
    day_df['cumulative_cnt'] = day_df['cnt'].cumsum()
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=day_df, x='dteday', y='cumulative_cnt', color='green', ax=ax)
    ax.set_title("Tren Kumulatif Penyewaan Sepeda (2011-2012)", fontsize=16)
    ax.set_xlabel("Tanggal", fontsize=12)
    ax.set_ylabel("Total Kumulatif Penyewaan", fontsize=12)
    st.pyplot(fig)
