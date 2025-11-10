<<<<<<< HEAD
# Import Packages
import os
import numpy as np
import pandas as pd
from PIL import Image
import streamlit as st

import scipy as sp
import seaborn as sns
import scipy.stats as stats
import matplotlib.pyplot as plt


# Load model
def load_resources():
    """Load model dan dataset."""
    base_path = os.path.dirname(os.path.abspath(__file__))

    csv_path = os.path.join(base_path, "skincare_clean.csv") 
    
    # kalau data ada di src juga
    pkl_path = os.path.join(base_path, "skincare_df_w2v.pkl")
    df = pd.read_pickle(pkl_path)

    return df

# Streamlit interface
def run():
    # Dapatkan path folder tempat file ini berada
    base_path = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(base_path, "image.png")

    # akses gambar
    img = Image.open("./src/image.png")
    st.image(img, caption="Temukan skincare terbaik sesuai kebutuhan kulitmu", use_container_width=True)
    st.subheader('EXPLORATORY DATA ANALYSIS')
    st.markdown('---')

    pkl_path = os.path.join(base_path, "skincare_df_w2v.pkl")
    df = pd.read_pickle(pkl_path)
    st.write('### Sample Data')
    st.dataframe(df)
    st.markdown('''
    ### Dataset Overview
    Data ini merupakan kumpulan informasi produk skincare yang diambil dari berbagai merek terkenal di platform [Female Daily](https://reviews.femaledaily.com).

    Dataset ini digunakan untuk menganalisis tren produk skincare berdasarkan jenis, merk, harga dan ulasan pengguna.

    Faktor faktor yang dianalisis mencakup :
    - :lipstick: **Product type**
    - :label: **brand**
    - :star: **rating**
    - :speech_balloon: **Review Count**
    - :moneybag: **Price**
    - :page_facing_up: **Description**
                    
    ''')
    
    st.markdown('---')
    st.header('Top 10 Brand by Ratings')
    # DataFrame Summary
    top_brandrating = df.groupby(['brand'])['rating'].sum().sort_values(ascending=False).head(10)
    # st.dataframe(top_brandrating, use_container_width=True)

    # bar horizontal
    fig, ax = plt.subplots()
    sns.barplot(x=top_brandrating.values, y=top_brandrating.index, palette="inferno")

    # set label and titel
    ax.set_title('Top 10 Brand by Ratings')
    ax.set_xlabel('Ratings')
    ax.set_ylabel('Brand')

    # show plot
    st.pyplot(fig)
    st.markdown('''
    ### Insight
    Dapat dilihat dari plot diatas: 
    - *Wardah*
    - *Pond's*
    - *L'Oreal Paris* 
                    
    sebagai brand yang sudah lama berdiri, menjadi Top 3 brand yang mendapat rating tertinggi dari perempuan Indonesia.
    Lalu diikuti oleh startup brand lokal yaitu Azarine, Somethinc, dan Avoskin, yang termasuk startup kecantikan yang unggul dalam melakukan inovasi produk.
    Dapat disimpulkan konsumen produk kecantikan di Indonesia mementingkan reputasi brand dan kualitas produk dalam memilih produk skincare yang mereka gunakan.                 
    ''')

    # Visualisasi 2 : By review count
    st.markdown('---')
    st.header('Top 10 Brand by Review Count')
    # === DataFrame Summary
    top_brandrating = df.groupby(['brand'])['review_count'].sum().sort_values(ascending=False).head(10)

    # buat figure
    fig, ax = plt.subplots(figsize=(12,6))

    # buat line chart
    ax.plot(top_brandrating.index, top_brandrating.values, 
            marker='o', linestyle='-', color='blue', linewidth=2)

    # set label dan title
    ax.set_title('Top 10 Brand by Reviews', fontsize=14, fontweight='bold')
    ax.set_xlabel('Brand', fontsize=12)
    ax.set_ylabel('Total Reviews', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()
    st.pyplot(fig)
    st.markdown('''
    ### Insight
    Lima brand teratas yang paling banyak mendapatkan review atas produk-produknya adalah Azarine, Emina, Hada Labo, Somethinc, dan Wardah.
    Kelima brand tersebut banyak mendapatkan review konsumen karena inovasi dan variasi atas produk yang dikeluarkan dan juga termasuk kategori produk skincare terjangkau.

    Lalu ada Cosrx sebagai satu-satunya brand skincare asal Korea yang banyak mendapat perhatian, yang juga karena kualitas dan *value-for-money* atas produk yang dikeluarkan sehingga mendapat kepercayaan para perempuan Indonesia.
    ''')
    
    # Visualisasi 3 : Top Engagement Product Type
    st.markdown('---')
    st.header('Top Engagement Product Type')

    # === DataFrame Summary
    top_brandrating = df.groupby(['product_type'])['review_count'].sum().sort_values(ascending=False)

    # buat figure
    fig, ax = plt.subplots(figsize=(8,8))
    top_brandrating.plot(
        kind='pie',
        autopct = '%.2f%%',
        figsize=(8,8),
        ylabel="",
        title= "Top Engagement Product Type" 
    )
    st.pyplot(fig)
    st.markdown('''
    ### Insight
    Dari lima tipe produk, serum/essence menjadi produk yang paling banyak mendapat review konsumen.
    Hal ini dikarenakan serum merupakan produk skincare yang bertujuan untuk menyelesaikan target masalah kesehatan kulit konsumen.

    Lalu kategori selanjutnya yang banyak mendapat perhatian adalah sun protection dan cleanser, yang merupakan bagian dari rutinitas dasar sehari-hari dalam menggunakan skincare.
    ''')

    # Visualisasi 4 : Top 10 Product by Reviews
    st.markdown('---')
    st.header('Top 10 Product by Reviews')

    # DataFrame Summary
    top_productreviews = df.groupby(['unique_id'])['review_count'].sum().sort_values(ascending=False).head(10)
    
    # buat figure
    fig, ax = plt.subplots(figsize=(10,6))
    sns.barplot(
        x=top_productreviews.values, 
        y=top_productreviews.index, 
        palette="viridis"  ,
        ax=ax
    )
    # set label and titel
    ax.set_title('Top 10 Product by Reviews')
    ax.set_xlabel('Reviews')
    ax.set_ylabel('Product')

    plt.tight_layout()

    st.pyplot(fig)
    st.markdown('''
    ### Insight
    Dari plot diatas, lima produk yang memiliki review terbanyak, empat produk merupakan produk sun protection, yaitu dari Emina, Azarine, Skin Aqua, dan Biore.
    Dan satu produk merupakan produk cleanser yang aman dari Cetaphil.

    Kedua kategori produk tersebut merupakan bagian dari bagian skincare dasar.
    Hal ini menandakan tingginya kesadaran konsumen atas kebutuhan skincare dasar dan pentingnya pemakaian sunscreen di Indonesia sebagai negara tropis.
    ''')

    # Visualisasi 5 : Top 10 Price Range by Reviews
    st.markdown('---')
    st.header('Top 10 Price Range by Reviews')

    # DataFrame Summary
    top_pricereviews = df.groupby(['price'])['review_count'].sum().sort_values(ascending=False).head(10)

    # buat figure
    fig, ax = plt.subplots(figsize=(10,6))
    sns.barplot(
        x=top_pricereviews.values, 
        y=top_pricereviews.index, 
        palette="hls",
        ax=ax
    )
    # set label and titel
    ax.set_title('Top 10 Price Range by Reviews')
    ax.set_xlabel('Reviews')
    ax.set_ylabel('Brand')

    plt.tight_layout()

    st.pyplot(fig)
    st.markdown('''
    ### Insight
    Dari berbagai jenis produk dengan beragam harga, konsumen paling banyak memberikan review pada produk di rentang harga 26.000-115.000.
    Dapat disimpulkan bahwa masyarakat Indonesia menyukai produk dengan harga terjangkau.
    Itulah mengapa brand seperti Azarine, Emina, dan Wardah yang menyasar middle-low customer berhasil mendapat tempat di masyarakat Indonesia.
    ''')

if __name__ == '__main__':
=======
# Import Packages
import os
import numpy as np
import pandas as pd
from PIL import Image
import streamlit as st

import scipy as sp
import seaborn as sns
import scipy.stats as stats
import matplotlib.pyplot as plt


# Load model
def load_resources():
    """Load model dan dataset."""
    base_path = os.path.dirname(os.path.abspath(__file__))

    csv_path = os.path.join(base_path, "skincare_clean.csv") 
    
    # kalau data ada di src juga
    pkl_path = os.path.join(base_path, "skincare_df_w2v.pkl")
    df = pd.read_pickle(pkl_path)

    return df

# Streamlit interface
def run():
    # Dapatkan path folder tempat file ini berada
    base_path = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(base_path, "image.png")

    # akses gambar
    img = Image.open("./src/image.png")
    st.image(img, caption="Temukan skincare terbaik sesuai kebutuhan kulitmu", use_container_width=True)
    st.subheader('EXPLORATORY DATA ANALYSIS')
    st.markdown('---')

    pkl_path = os.path.join(base_path, "skincare_df_w2v.pkl")
    df = pd.read_pickle(pkl_path)
    st.write('### Sample Data')
    st.dataframe(df)
    st.markdown('''
    ### Dataset Overview
    Data ini merupakan kumpulan informasi produk skincare yang diambil dari berbagai merek terkenal di platform [Female Daily](https://reviews.femaledaily.com).

    Dataset ini digunakan untuk menganalisis tren produk skincare berdasarkan jenis, merk, harga dan ulasan pengguna.

    Faktor faktor yang dianalisis mencakup :
    - :lipstick: **Product type**
    - :label: **brand**
    - :star: **rating**
    - :speech_balloon: **Review Count**
    - :moneybag: **Price**
    - :page_facing_up: **Description**
                    
    ''')
    
    st.markdown('---')
    st.header('Top 10 Brand by Ratings')
    # DataFrame Summary
    top_brandrating = df.groupby(['brand'])['rating'].sum().sort_values(ascending=False).head(10)
    # st.dataframe(top_brandrating, use_container_width=True)

    # bar horizontal
    fig, ax = plt.subplots()
    sns.barplot(x=top_brandrating.values, y=top_brandrating.index, palette="inferno")

    # set label and titel
    ax.set_title('Top 10 Brand by Ratings')
    ax.set_xlabel('Ratings')
    ax.set_ylabel('Brand')

    # show plot
    st.pyplot(fig)
    st.markdown('''
    ### Insight
    Dapat dilihat dari plot diatas: 
    - *Wardah*
    - *Pond's*
    - *L'Oreal Paris* 
                    
    sebagai brand yang sudah lama berdiri, menjadi Top 3 brand yang mendapat rating tertinggi dari perempuan Indonesia.
    Lalu diikuti oleh startup brand lokal yaitu Azarine, Somethinc, dan Avoskin, yang termasuk startup kecantikan yang unggul dalam melakukan inovasi produk.
    Dapat disimpulkan konsumen produk kecantikan di Indonesia mementingkan reputasi brand dan kualitas produk dalam memilih produk skincare yang mereka gunakan.                 
    ''')

    # Visualisasi 2 : By review count
    st.markdown('---')
    st.header('Top 10 Brand by Review Count')
    # === DataFrame Summary
    top_brandrating = df.groupby(['brand'])['review_count'].sum().sort_values(ascending=False).head(10)

    # buat figure
    fig, ax = plt.subplots(figsize=(12,6))

    # buat line chart
    ax.plot(top_brandrating.index, top_brandrating.values, 
            marker='o', linestyle='-', color='blue', linewidth=2)

    # set label dan title
    ax.set_title('Top 10 Brand by Reviews', fontsize=14, fontweight='bold')
    ax.set_xlabel('Brand', fontsize=12)
    ax.set_ylabel('Total Reviews', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()
    st.pyplot(fig)
    st.markdown('''
    ### Insight
    Lima brand teratas yang paling banyak mendapatkan review atas produk-produknya adalah Azarine, Emina, Hada Labo, Somethinc, dan Wardah.
    Kelima brand tersebut banyak mendapatkan review konsumen karena inovasi dan variasi atas produk yang dikeluarkan dan juga termasuk kategori produk skincare terjangkau.

    Lalu ada Cosrx sebagai satu-satunya brand skincare asal Korea yang banyak mendapat perhatian, yang juga karena kualitas dan *value-for-money* atas produk yang dikeluarkan sehingga mendapat kepercayaan para perempuan Indonesia.
    ''')
    
    # Visualisasi 3 : Top Engagement Product Type
    st.markdown('---')
    st.header('Top Engagement Product Type')

    # === DataFrame Summary
    top_brandrating = df.groupby(['product_type'])['review_count'].sum().sort_values(ascending=False)

    # buat figure
    fig, ax = plt.subplots(figsize=(8,8))
    top_brandrating.plot(
        kind='pie',
        autopct = '%.2f%%',
        figsize=(8,8),
        ylabel="",
        title= "Top Engagement Product Type" 
    )
    st.pyplot(fig)
    st.markdown('''
    ### Insight
    Dari lima tipe produk, serum/essence menjadi produk yang paling banyak mendapat review konsumen.
    Hal ini dikarenakan serum merupakan produk skincare yang bertujuan untuk menyelesaikan target masalah kesehatan kulit konsumen.

    Lalu kategori selanjutnya yang banyak mendapat perhatian adalah sun protection dan cleanser, yang merupakan bagian dari rutinitas dasar sehari-hari dalam menggunakan skincare.
    ''')

    # Visualisasi 4 : Top 10 Product by Reviews
    st.markdown('---')
    st.header('Top 10 Product by Reviews')

    # DataFrame Summary
    top_productreviews = df.groupby(['unique_id'])['review_count'].sum().sort_values(ascending=False).head(10)
    
    # buat figure
    fig, ax = plt.subplots(figsize=(10,6))
    sns.barplot(
        x=top_productreviews.values, 
        y=top_productreviews.index, 
        palette="viridis"  ,
        ax=ax
    )
    # set label and titel
    ax.set_title('Top 10 Product by Reviews')
    ax.set_xlabel('Reviews')
    ax.set_ylabel('Product')

    plt.tight_layout()

    st.pyplot(fig)
    st.markdown('''
    ### Insight
    Dari plot diatas, lima produk yang memiliki review terbanyak, empat produk merupakan produk sun protection, yaitu dari Emina, Azarine, Skin Aqua, dan Biore.
    Dan satu produk merupakan produk cleanser yang aman dari Cetaphil.

    Kedua kategori produk tersebut merupakan bagian dari bagian skincare dasar.
    Hal ini menandakan tingginya kesadaran konsumen atas kebutuhan skincare dasar dan pentingnya pemakaian sunscreen di Indonesia sebagai negara tropis.
    ''')

    # Visualisasi 5 : Top 10 Price Range by Reviews
    st.markdown('---')
    st.header('Top 10 Price Range by Reviews')

    # DataFrame Summary
    top_pricereviews = df.groupby(['price'])['review_count'].sum().sort_values(ascending=False).head(10)

    # buat figure
    fig, ax = plt.subplots(figsize=(10,6))
    sns.barplot(
        x=top_pricereviews.values, 
        y=top_pricereviews.index, 
        palette="hls",
        ax=ax
    )
    # set label and titel
    ax.set_title('Top 10 Price Range by Reviews')
    ax.set_xlabel('Reviews')
    ax.set_ylabel('Brand')

    plt.tight_layout()

    st.pyplot(fig)
    st.markdown('''
    ### Insight
    Dari berbagai jenis produk dengan beragam harga, konsumen paling banyak memberikan review pada produk di rentang harga 26.000-115.000.
    Dapat disimpulkan bahwa masyarakat Indonesia menyukai produk dengan harga terjangkau.
    Itulah mengapa brand seperti Azarine, Emina, dan Wardah yang menyasar middle-low customer berhasil mendapat tempat di masyarakat Indonesia.
    ''')

if __name__ == '__main__':
>>>>>>> 847706be8d0a05e67f9cba53f612280ddd5d1a97
    run()