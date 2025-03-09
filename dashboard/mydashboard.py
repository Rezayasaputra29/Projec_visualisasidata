import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st



# Konfigurasi Awal
st.set_page_config(page_title="Bike Sharing Analysis", layout="wide")
sns.set_style("whitegrid")

# Mapping untuk musim dan cuaca
season_map = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
weather_map = {1: "Cerah", 2: "Mendung", 3: "Hujan/Salju Ringan", 4: "Hujan Lebat"}

#Fungsi kategorisasi windspeed
def categorize_windspeed(windspeed):
    if windspeed <= 5:
        return "Sangat Rendah"
    elif windspeed <= 10:
        return "Rendah"
    elif windspeed <= 15:
        return "Sedang"
    elif windspeed <= 20:
        return "Tinggi"
    else:
        return "Sangat Tinggi"


# Warna berdasarkan kategori windspeed
category_colors = {
    "Sangat Rendah": "green",
    "Rendah": "blue",
    "Sedang": "yellow",
    "Tinggi": "orange",
    "Sangat Tinggi": "red"
}

# Fungsi Load Data
@st.cache_data
def load_data():
    days_url = "https://raw.githubusercontent.com/Rezayasaputra29/Projec_visualisasidata/main/dashboard/days_baru.csv"
    hours_url = "https://raw.githubusercontent.com/Rezayasaputra29/Projec_visualisasidata/main/dashboard/hours_baru.csv"
    
    days = pd.read_csv(days_url, parse_dates=["date"])
    hours = pd.read_csv(hours_url, parse_dates=["date"])

    # Preprocessing untuk data harian
    days["weather_label"] = days["weather_condition"].map(weather_map)
    days["season_label"] = days["season"].map(season_map)
    days["month"] = days["date"].dt.month_name().str[:3]
    days["year"] = days["date"].dt.year

    # Preprocessing untuk data per jam
    hours["hours"] = hours["hours"].astype(int)
    hours["workingday_label"] = hours["workingday"].map({True: "Hari Kerja", False: "Akhir Pekan/Libur"})
    hours["windspeed_category"] = hours["normalized_wind_speed"].apply(categorize_windspeed)
    

    return days, hours


days_df, hours_df = load_data()

# Sidebar Filter
st.sidebar.header("Sales by year")
selected_year = st.sidebar.selectbox("Years", ["All", 2012, 2011])

# Apply Filter
if selected_year != "All":
    days_df = days_df[days_df["year"] == selected_year]
    hours_df = hours_df[hours_df["date"].dt.year == selected_year]


# Main Dashboard
st.title("Dashboard Data Bike Sharing ")
tab1, tab2, tab3 = st.tabs(["Data day", "Data hour", "Ringkasan"])

with tab1:
    st.header("Analisis data set day")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Distribusi Penyewaan Sepeda berdasarkan kondisi cuaca")
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.barplot(x='weather_condition', y='total_rentals', data=days_df, errorbar=None, ax=ax)
        ax.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca")
        ax.set_xlabel("Kondisi Cuaca")
        ax.set_ylabel("Rata-rata Penyewaan")

        # Tampilkan plot di Streamlit
        st.pyplot(fig)

        st.markdown("**Insight Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca (Bar Plot) :**")
        st.markdown("""
        - Diagram batang menunjukkan jumlah penyewaan sepeda berkurang ketika kondisi cuaca memburuk.
        - Cuaca cerah (weather_contition = 1) memiliki sewa rata -rata tertinggi, hampir 5.000 orang disewa setiap hari.
        - Sewa pengurangan cuaca berawan atau berawan (weather_condition = 2) dan lebih berkurang secara signifikan dalam hujan / salju (weather_contition = 3).
        - Tidak ada penyewaan sepeda dalam kondisi cuaca yang keras (weather_condition = 4).
        """)
    with col2:
        # Subheader
        st.subheader("Distribusi Penyewaan Sepeda Berdasarkan Kondisi Cuaca")

        # Membuat boxplot
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.boxplot(x='weather_condition', y='total_rentals', data=days_df, ax=ax)
        ax.set_title("Distribusi Penyewaan Sepeda Berdasarkan Kondisi Cuaca")
        ax.set_xlabel("Kondisi Cuaca")
        ax.set_ylabel("Total Penyewaan")

        # Menampilkan plot di Streamlit
        st.pyplot(fig)

        st.markdown("**Insight Distribusi Penyewaan Sepeda Berdasarkan Kondisi Cuaca (Box Plot) :**")
        st.markdown("""
        - box plot menggambarkan perubahan nomor sewa sepeda dalam kondisi cuaca yang berbeda.
        - Dalam cuaca cerah (weather_condition = 1), distribusi jumlah penyewaan sepeda lebih tinggi dari waktu terburuk.
        - SWeather_contition (3) memiliki distribusi data yang lebih rendah dan sejumlah kecil sewa.
        - Weather_contition (3) memiliki distribusi data yang lebih rendah dan sejumlah kecil sewa.
        """)

        

with tab1:

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Tren Penyewaan Sepeda Sepanjang Tahun")
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.lineplot(x='month', y='total_rentals', data=days_df, marker='o', ax=ax)
        ax.set_title("Tren Penyewaan Sepeda Sepanjang Tahun")
        ax.set_xlabel("Bulan")
        ax.set_ylabel("Total Penyewaan")
        ax.set_xticks(range(1, 13))

        # Tampilkan plot di Streamlit
        st.pyplot(fig)

        st.markdown("**Insight Tren Penyewaan Sepeda Sepanjang Tahun (Line Plot):**")
        st.markdown("""
        - trend sewa sepeda meningkat dari awal tahun hingga pertengahan tahun (Mei-Juli), kemudian mengalami sedikit penurunan pada akhir tahun ini.
        - Sewa tertinggi sekitar Juni hingga September, mungkin karena cuaca yang lebih baik dan lebih banyak kegiatan di luar ruangan.
        - Sewa sepeda cenderung lebih rendah dari awal tahun (Januari - Februari Februari), mungkin karena musim dingin atau musim hujan yang menghambat kegiatan di luar ruangan.
        """)

    with col2:
        # Plot Boxplot Distribusi Penyewaan Berdasarkan Musim
        st.subheader("Distribusi Penyewaan Sepeda Berdasarkan Musim")

        fig, ax = plt.subplots(figsize=(12, 6))
        sns.boxplot(x='season', y='total_rentals', data=days_df, ax=ax)
        ax.set_title("Distribusi Penyewaan Sepeda Berdasarkan Musim")
        ax.set_xlabel("Musim")
        ax.set_ylabel("Total Penyewaan")

        # Tampilkan plot di Streamlit
        st.pyplot(fig)

        st.markdown("**Insight Distribusi Penyewaan Sepeda Berdasarkan Musim (Box Plot):**")
        st.markdown("""
        - Musim panas (musim = 3) memiliki sewa rata -rata tertinggi, lalu musim gugur (musim = 2).
        - sewa sepeda lebih rendah di musim dingin (musim = 1), mungkin karena waktu yang lebih dingin atau curah hujan tinggi.
        - Varian penyewaan yang lebih besar di musim panas dan musim gugur, menunjukkan fluktuasi penggunaan sepeda.
        - Beberapa nilai abnormal tertentu dari setiap musim menunjukkan bahwa ada hari -hari tertentu dengan gelombang atau diskon untuk disewa.
        """)

with tab2:
    st.header("Analisis data set hour")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("⏳ Rata-rata Penyewaan Sepeda Berdasarkan Jam (Hari Kerja vs Libur)")

        # Plot
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.lineplot(
            x='hours', 
            y='total_rentals', 
            hue='workingday', 
            data=hours_df, 
            marker='o', 
            palette=['red', 'blue'], 
            ax=ax
        )

        # Set Label & Title
        ax.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Jam (Hari Kerja vs Libur)")
        ax.set_xlabel("Jam")
        ax.set_ylabel("Total Penyewaan")
        ax.set_xticks(range(0, 24))

        # Tampilkan plot di Streamlit
        st.pyplot(fig)

        st.markdown("**Insight Rata-rata Penyewaan Sepeda Berdasarkan Jam dalam sehari:**")
        st.markdown("""
        - dari perbandingan hari kerja (1) dan libur (hari kerja = 0), tampaknya: selama minggu sekolah).
        - Pada hari libur, model leasing didistribusikan lebih merata sepanjang hari dengan puncak sekitar siang (11:00 - 17:00).
        - Secara umum, jumlah penyewaan sepeda cenderung lebih tinggi dalam seminggu dibandingkan dengan libur.
        """)

    with col2:
        # Subheader untuk boxplot hari kerja vs libur
        st.subheader("📌 Distribusi Penyewaan Sepeda Berdasarkan Hari Kerja vs Libur")

        # Membuat boxplot
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.boxplot(x='workingday', y='total_rentals', hue='workingday', data=hours_df, palette=['red', 'blue'], ax=ax)

        # Menyesuaikan tampilan sumbu dan judul
        ax.set_title("Distribusi Penyewaan Sepeda Berdasarkan Hari Kerja vs Libur")
        ax.set_xlabel("Hari")
        ax.set_ylabel("Total Penyewaan Sepeda")
        ax.set_xticks([0, 1])
        ax.set_xticklabels(["Libur", "Hari Kerja"])

        # Menampilkan plot di Streamlit
        st.pyplot(fig)

        st.markdown("**distribusi Penyewaan Sepeda Berdasarkan Hari Kerja vs Libur dengan box plot:**")
        st.markdown("""
        - Pada hari kerja, jumlah penyewaan memiliki variasi yang lebih besar dan cenderung lebih tinggi di beberapa jam tertentu.
        - Pada hari libur, jumlah penyewaan lebih stabil dan tidak memiliki lonjakan ekstrem seperti pada hari kerja.
        - Outlier terlihat pada beberapa jam tertentu, menunjukkan ada kondisi luar biasa (misalnya cuaca atau event khusus) yang menyebabkan lonjakan penggunaan.
    
        """)

with tab2:

    col1, col2 = st.columns(2)

    with col1:
        # Judul Section
        st.header("🌬️ Hubungan Kecepatan Angin dengan Penyewaan Sepeda")

        # Scatter Plot
        st.subheader("Scatter Plot: Kecepatan Angin vs Total Penyewaan Sepeda")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(x='normalized_wind_speed', y='total_rentals', data=hours_df, alpha=0.5, ax=ax)
        ax.set_title("Hubungan Kecepatan Angin dengan Jumlah Penyewaan Sepeda")
        ax.set_xlabel("Kecepatan Angin (Ternormalisasi)")
        ax.set_ylabel("Total Penyewaan Sepeda")

        # Tampilkan plot di Streamlit
        st.pyplot(fig)

        st.markdown("**Insight Hubungan Kecepatan Angin dengan Penyewaan Sepeda:**")
        st.markdown("""
        - Tidak ada korelasi yang kuat antara kecepatan angin dan jumlah penyewaan sepeda..
        - Peminjaman sepeda terjadi dalam jumlah besar bahkan pada kecepatan angin tinggi, meskipun lebih terkonsentrasi pada kecepatan angin rendah hingga sedang.
        - Hal ini menunjukkan bahwa angin bukan faktor utama yang memengaruhi peminjaman sepeda.
    
        """)

         

    with col2:
        
        hours_df['wind_speed_category'] = pd.qcut(
            hours_df['normalized_wind_speed'], 
            q=4, 
            labels=["Rendah", "Sedang", "Tinggi", "Sangat Tinggi"]
        )

        # Menampilkan header di Streamlit
        st.header("Analisis Kecepatan Angin terhadap Penyewaan Sepeda")

        # Plot utama: Distribusi Penyewaan Berdasarkan Kecepatan Angin
        st.subheader("Distribusi Penyewaan Sepeda Berdasarkan Kecepatan Angin")

        fig, ax = plt.subplots(figsize=(8, 6))
        sns.boxplot(
            x='wind_speed_category', 
            y='total_rentals', 
            data=hours_df, 
            hue='wind_speed_category', 
            palette="coolwarm", 
            legend=False, 
            ax=ax
        )
        ax.set_title("Distribusi Penyewaan Sepeda Berdasarkan Kecepatan Angin")
        ax.set_xlabel("Kategori Kecepatan Angin")
        ax.set_ylabel("Total Penyewaan Sepeda")

        # Menampilkan plot di Streamlit
        st.pyplot(fig)

        st.markdown("**Insight Distribusi Penyewaan Sepeda Berdasarkan Kecepatan Angin:**")
        st.markdown("""
        - Sewa sepeda cenderung lebih tinggi dalam kecepatan angin rendah hingga sedang.
        - Dalam kategori kecepatan tinggi, penyebaran lebih sedikit penyewaan, menunjukkan lebih sedikit pengendara sepeda dalam kondisi angin.
        - Namun, sewa rata -rata di setiap jenis masih cukup stabil, ini menunjukkan bahwa bahkan ketika kecepatan angin meningkat, beberapa orang masih menggunakan sepeda.
        """)

    with tab3:
        st.header("Ringkasan data")

        st.subheader("Tabel Data Harian")
        st.markdown("""
        **Bagaimnan Pengaruh Cuaca terhadap Jumlah Peminjaman Sepeda per Hari?**
        - Cuaca Cerah: Pada kondisi ini, jumlah peminjaman sepeda mengalami peningkatan yang signifikan, mencapai rata-rata antara 4,500 hingga 5,000 transaksi per hari.
        - Hujan Ringan: Jumlah peminjaman menurun sekitar 30% dibandingkan dengan hari-hari cerah.
        - Hujan Deras atau Salju: Di kondisi ini, peminjaman turun secara drastis, hanya mencapai rata-rata 1,800 hingga 2,500 transaksi per hari.

        **Bagaimana Tren Jumlah Peminjaman Sepeda Sepanjang Tahun?**
        - Musim:
            - Musim Panas dan Gugur: Musim ini menunjukkan jumlah peminjaman tertinggi, sekitar 5,500 transaksi per hari, didorong oleh cuaca yang lebih nyaman.
            - Musim Dingin: Jumlah peminjaman terendah tercatat pada musim ini, dengan rata-rata hanya 3,000 transaksi per hari, terutama akibat cuaca dingin dan salju.
        - Bulan:
            - April hingga September: Terjadi peningkatan tren peminjaman, dengan puncak terjadi antara Juni hingga Agustus (6,000 transaksi per hari).
            - Desember hingga Februari: Jumlah peminjaman mengalami penurunan drastis, mencapai titik terendah sekitar 2,500 transaksi per hari, disebabkan oleh suhu ekstrem dan kondisi jalan yang kurang mendukung.
        """)

        st.subheader("Tabel Data Per jam")
        st.markdown("""
        **Bagaimana Pola Peminjaman Sepeda Berdasarkan Jam dan Hari Kerja/Libur?**
        - Hari Kerja:
            - Puncak Pagi: Antara pukul 07:00 hingga 09:00, peminjaman mencapai 800 hingga 900 transaksi per jam, dipicu oleh aktivitas komuter.
             - Puncak Sore: Dari pukul 17:00 hingga 19:00, jumlah peminjaman meningkat menjadi 850 hingga 1,000 transaksi per jam, seiring dengan waktu pulang kerja.
             - am Sepi: Pada rentang waktu 00:00 hingga 04:00, tercatat kurang dari 50 transaksi per jam.
        - Akhir Pekan/Libur:
            - idak terdapat puncak yang jelas pada pagi dan sore, namun menunjukkan pola yang stabil sepanjang hari, terutama antara pukul 10:00 hingga 16:00 dengan 600 hingga 700 transaksi per jam.
            - Aktivitas rekreasi di akhir pekan berkontribusi pada peningkatan jumlah peminjaman dibandingkan dengan malam hari.

        **Bagaimana Dampak Kecepatan Angin terhadap Jumlah Peminjaman Sepeda per Jam:
            - Bagaimana Dampak Kecepatan Angin terhadap Jumlah Peminjaman Sepeda per Jam
            - Musim Dingin: Jumlah peminjaman terendah tercatat pada musim ini, dengan rata-rata hanya 3,000 transaksi per hari, terutama akibat cuaca dingin dan salju.
            - Saat kecepatan angin melebihi 20 km/jam, jumlah peminjaman mengalami penurunan sekitar 20 hingga 30%, terutama pada waktu sore.
            - Kesimpulan: Kecepatan angin yang tinggi berpengaruh negatif terhadap jumlah peminjaman sepeda, terutama ketika terjadi bersamaan dengan suhu rendah atau kondisi cuaca ekstrem.
           
        """)
        
                

    




