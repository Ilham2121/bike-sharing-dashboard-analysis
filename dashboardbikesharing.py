import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Membaca data
day = pd.read_csv("day.csv")

# Fungsi untuk membuat dataframe baru berdasarkan agregasi data
def create_daily_rent_df(df):
    daily_rent_df = df.groupby(by='Dateday').agg({'Count': 'sum'}).reset_index()
    return daily_rent_df

def create_daily_casual_rent_df(df):
    daily_casual_rent_df = df.groupby(by='Dateday').agg({'casual': 'sum'}).reset_index()
    return daily_casual_rent_df

def create_daily_registered_rent_df(df):
    daily_registered_rent_df = df.groupby(by='Dateday').agg({'registered': 'sum'}).reset_index()
    return daily_registered_rent_df

def create_monthly_trend(df):
    monthly_trend = df.groupby('Month')['Count'].mean().reset_index()
    return monthly_trend

# Sidebar untuk filter tanggal
min_date = pd.to_datetime(day['Dateday']).dt.date.min()
max_date = pd.to_datetime(day['Dateday']).dt.date.max()

with st.sidebar:
    # Mengganti logo sidebar dengan gambar random
    st.image('https://st2.depositphotos.com/40527348/44435/v/450/depositphotos_444356130-stock-illustration-bicycle-rental-icons-set-logo.jpg')

    # Filter tanggal menggunakan kalender
    st.sidebar.title('Filter Data')
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

    st.sidebar.header("Visit my Profile:")

    st.sidebar.markdown("Ilham Aly Abdillah")

    # membuat link 
    st.markdown("[![LinkedIn](https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg)](https://www.linkedin.com/in/ilham-aly-abdillah-318856248/)")
   

# Filter data berdasarkan rentang tanggal
main_df = day[(pd.to_datetime(day['Dateday']).dt.date >= start_date) &
              (pd.to_datetime(day['Dateday']).dt.date <= end_date)]

# Menyiapkan berbagai dataframe untuk analisa
daily_rent_df = create_daily_rent_df(main_df)
daily_casual_rent_df = create_daily_casual_rent_df(main_df)
daily_registered_rent_df = create_daily_registered_rent_df(main_df)
monthly_trend = day.groupby('Month')['Count'].mean().reset_index()
weather_effect = day.groupby('Weather_Cond')['Count'].mean().reset_index()

# Menampilkan total penyewa dan pengguna
st.title("Dashboard Bike Sharing")


col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Pengguna Biasa", value=daily_casual_rent_df['casual'].sum())
with col2:
    st.metric("Pengguna Terdaftar", value=daily_registered_rent_df['registered'].sum())
with col3:
    st.metric("Total Penyewa", value=daily_rent_df['Count'].sum())

# Visualisasi kondisi cuaca terhadap penyewaan
st.subheader("Rata rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca")
fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(x='Weather_Cond', y='Count', data=weather_effect, palette='coolwarm', ci=None, ax=ax)
plt.xlabel('Kondisi Cuaca')
plt.ylabel('Rata-rata')
st.pyplot(fig)

#Visualisasi Trend bulanan rata rata peminjam sepeda
st.subheader('Tren Musiman Penyewaan Sepeda Berdasarkan Bulan')
fig, ax = plt.subplots(figsize=(10,6))
sns.lineplot(x='Month', y='Count', data=monthly_trend, marker='o', color='b', ax=ax)
ax.set_title('Tren Musiman Penyewaan Sepeda Berdasarkan Bulan')
ax.set_xlabel('Bulan')
ax.set_ylabel('Rata-rata Jumlah Sepeda yang Disewa')
ax.set_xticks(range(1, 13))
ax.grid(True)
st.pyplot(fig)

# Regplot untuk hubungan suhu dan jumlah penyewa
st.subheader("Hubungan Suhu udara dengan Jumlah Sepeda yang Disewa")
corr_temp_count = day['temp'].corr(day['Count'])
plt.figure(figsize=(8,6))
sns.regplot(x='temp', y='Count', data=day, color='g')
plt.title(f'Hubungan Suhu Udara dengan Jumlah Sepeda yang Disewa\nKorelasi: {corr_temp_count:.2f}')
plt.xlabel('Suhu Udara')
plt.ylabel('Jumlah Sepeda yang Disewa')
plt.grid(True)
st.pyplot(plt)

# Membuat Barplot untuk hubungan suhu dan jumlahnya
st.subheader("Versi barplot")

bins = np.arange(0, 1.1, 0.2)  # Rentang suhu
labels = [f'{b:.1f}-{b+0.2:.1f}' for b in bins[:-1]]

day['temp_range'] = pd.cut(day['temp'], bins=bins, labels=labels, include_lowest=True)

temp_rentals = day.groupby('temp_range')['Count'].mean().reset_index()

# Barplot untuk rentang suhu
plt.figure(figsize=(10,6))
sns.barplot(x='temp_range', y='Count', data=temp_rentals, palette='coolwarm')
plt.title('Jumlah Rata-rata Penyewaan Sepeda Berdasarkan Rentang Suhu')
plt.xlabel('Rentang Suhu')
plt.ylabel('Rata-rata Jumlah Sepeda yang Disewa')
plt.grid(True)
st.pyplot(plt)

# Visualisasi pengguna berdasarkan musim
st.subheader("Penyewaan Berdasarkan Musim")
season_label = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
main_df['season_label'] = main_df['season'].replace(season_label)
fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(x='season_label', y='Count', data=main_df, palette='Set2', ci=None, ax=ax)
st.pyplot(fig)

st.header("Analisis Tambahan")
# Membuat visualisasi sewa bulanan
st.subheader('Jumlah Penyewaan Bulanan')
fig, ax = plt.subplots(figsize=(10, 5))
monthly_rent = main_df.groupby(main_df['Dateday'].str[:7])['Count'].sum()
ax.plot(monthly_rent.index, monthly_rent.values, marker='o', color='blue')
plt.xticks(rotation=45)
st.pyplot(fig)


# Informasi footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center;">
        <h4 style="color: #007BFF;">Dashboard Analysis Bike Sharing Data</h4>
        <h4 style="color: #007BFF; font-weight: bold;">Copyright &copy; Ilham Aly Abdillah 2024</h3>
        <p>Data period: {} to {}</p>
    </div>
""".format(min_date, max_date), unsafe_allow_html=True)
