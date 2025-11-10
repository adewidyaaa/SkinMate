<<<<<<< HEAD
# IMPORT LIBRARIES
import os
import re
import string
import numpy as np
import pandas as pd
import streamlit as st
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from PIL import Image


# SETUP NLTK
nltk_data_dir = '/tmp/nltk_data'
os.makedirs(nltk_data_dir, exist_ok=True)
nltk.data.path.append(nltk_data_dir)

# Download stopwords dan punkt ke folder /tmp
nltk.download('stopwords', download_dir=nltk_data_dir)
nltk.download('punkt', download_dir=nltk_data_dir)

# Load stopwords Bahasa Indonesia
indo_stopwords = set(stopwords.words('indonesian'))

# FUNGSI-FUNGSI UTAMA

def load_resources():
    """Load model dan dataset."""
    base_path = os.path.dirname(os.path.abspath(__file__))

    model_path = os.path.join(base_path, "word2vec_model.model")
    csv_path = os.path.join(base_path, "skincare_clean.csv") 

    model = Word2Vec.load(model_path)
    
    # kalau data ada di src juga
    pkl_path = os.path.join(base_path, "skincare_df_w2v.pkl")
    df = pd.read_pickle(pkl_path)

    return model, df


def preprocess_text(text):
    """Membersihkan teks (sama dengan tahap training)."""
    if pd.isna(text):
        return text
    text = re.sub(r"\\n", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    keywords = ['ingredients', 'how to use', 'suitable']
    pattern = r'(?i)([a-zA-Z0-9])(' + '|'.join([k.replace(' ', '') for k in keywords]) + r')'
    text = re.sub(pattern, lambda m: f'{m.group(1)} {m.group(2)}', text)

    text = text.lower()
    text = re.sub(r'\bx\b', '', text)
    text = re.sub(r'\b\d+\b', '', text)
    text = re.sub(r'\b\d+[a-zA-Z]+\b', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))

    satuan_umum = {'ml', 'gram', 'menit', 'pump', 'pcs'}
    text = ' '.join([word for word in text.split() if word not in satuan_umum])

    for k in keywords:
        text = re.sub(k + r'\s*:?', k, text)

    text = ' '.join([word for word in text.split() if word not in indo_stopwords])
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def get_avg_w2v(tokens, model):
    """Mengambil rata-rata Word2Vec dari token."""
    vectors = [model.wv[w] for w in tokens if w in model.wv]
    if len(vectors) == 0:
        return np.zeros(model.vector_size)
    return np.mean(vectors, axis=0)


def recommended_products(query, df, model, alpha=0.7, beta=0.15, gamma=0.15, top_n=3):
    """Fungsi utama untuk menghasilkan rekomendasi."""
    df_temp = df.copy()

    # Preprocess query
    query_clean = preprocess_text(query)
    query_tokens = query_clean.split()
    query_vec = get_avg_w2v(query_tokens, model).reshape(1, -1)
    X_vectors = np.vstack(df_temp['w2v_vector'].values)

    # Hitung cosine similarity
    cos_sim = cosine_similarity(query_vec, X_vectors)[0]
    df_temp['similarity'] = cos_sim

    # Normalisasi rating & review_count
    df_temp['rating_norm'] = (
        (df_temp['rating'] - df_temp['rating'].min()) /
        (df_temp['rating'].max() - df_temp['rating'].min())
    )
    df_temp['review_norm'] = (
        (df_temp['review_count'] - df_temp['review_count'].min()) /
        (df_temp['review_count'].max() - df_temp['review_count'].min())
    )

    # Skor gabungan
    df_temp['final_score'] = (
        alpha * df_temp['similarity'] +
        beta * df_temp['rating_norm'] +
        gamma * df_temp['review_norm']
    )

    # Ambil top produk per kategori
    result = (
        df_temp.sort_values(by='final_score', ascending=False)
        .groupby('product_type', group_keys=False)
        .head(top_n)
        .sort_values(by='product_type', ascending=True)
        .reset_index(drop=True)
        [['product_type', 'product', 'brand', 'price', 'rating', 'review_count',
          'description', 'image_url', 'similarity', 'final_score']]
    )

    return result

# STREAMLIT APP — FUNGSI UTAMA

def run():
    """Main function untuk menjalankan aplikasi Streamlit."""
    # st.title("Skincare Recommendation App")
    # st.subheader("By SkinMate")
    # Logo
    img = Image.open("./src/image.png")
    st.image(img, caption="Temukan skincare terbaik sesuai kebutuhan kulitmu", use_container_width=True)
    st.markdown(
        "Ceritakan sedikit tentang kondisi kulitmu (misalnya: kering, kusam, atau berjerawat) "
        "untuk mendapatkan rekomendasi produk yang sesuai."
    )

    # Load resources
    model_w2v, df = load_resources()

    # Input user
    query = st.text_input("Ketikkan kebutuhan kulit kamu:")
    top_n = st.selectbox(
    "Jumlah rekomendasi per kategori",
    options=[1, 2, 3, 5, 10],
    index=2)

    # Tampilkan hasil rekomendasi
    if st.button("Dapatkan Rekomendasi") and query.strip() != "":
        with st.spinner("Mencari produk terbaik untuk kamu..."):
            recs = recommended_products(query, df, model_w2v, top_n=top_n)

        st.success("Berikut rekomendasi produk untuk kamu:")

        # Tampilkan hasil per kategori
        for category, group in recs.groupby('product_type', sort=False):
            # Header kategori
            st.markdown(f"# {category.title()}")
            st.divider()

            # Daftar produk di kategori ini
            for _, row in group.iterrows():
                with st.container():
                    st.markdown(f"### {row['product']}")
                    if pd.notna(row['image_url']):
                        st.image(row['image_url'], width=250)
                    st.markdown(
                        f"**Brand:** {row['brand']} | **Tipe:** {category.title()} | **Harga:** Rp{row['price']:,}  |  ⭐ {row['rating']} ({int(row['review_count'])} review)"
                    )
                    st.markdown(f"**Deskripsi:** {row['description']}")
                    st.markdown("---")

    else:
        st.info("Tekan tombol 'Dapatkan Rekomendasi' untuk melihat hasil rekomendasi yang telah kamu tulis.")

# ENTRY POINT
if __name__ == "__main__":
=======
# IMPORT LIBRARIES
import os
import re
import string
import numpy as np
import pandas as pd
import streamlit as st
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from PIL import Image


# SETUP NLTK
nltk_data_dir = '/tmp/nltk_data'
os.makedirs(nltk_data_dir, exist_ok=True)
nltk.data.path.append(nltk_data_dir)

# Download stopwords dan punkt ke folder /tmp
nltk.download('stopwords', download_dir=nltk_data_dir)
nltk.download('punkt', download_dir=nltk_data_dir)

# Load stopwords Bahasa Indonesia
indo_stopwords = set(stopwords.words('indonesian'))

# FUNGSI-FUNGSI UTAMA

def load_resources():
    """Load model dan dataset."""
    base_path = os.path.dirname(os.path.abspath(__file__))

    model_path = os.path.join(base_path, "word2vec_model.model")
    csv_path = os.path.join(base_path, "skincare_clean.csv") 

    model = Word2Vec.load(model_path)
    
    # kalau data ada di src juga
    pkl_path = os.path.join(base_path, "skincare_df_w2v.pkl")
    df = pd.read_pickle(pkl_path)

    return model, df


def preprocess_text(text):
    """Membersihkan teks (sama dengan tahap training)."""
    if pd.isna(text):
        return text
    text = re.sub(r"\\n", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    keywords = ['ingredients', 'how to use', 'suitable']
    pattern = r'(?i)([a-zA-Z0-9])(' + '|'.join([k.replace(' ', '') for k in keywords]) + r')'
    text = re.sub(pattern, lambda m: f'{m.group(1)} {m.group(2)}', text)

    text = text.lower()
    text = re.sub(r'\bx\b', '', text)
    text = re.sub(r'\b\d+\b', '', text)
    text = re.sub(r'\b\d+[a-zA-Z]+\b', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))

    satuan_umum = {'ml', 'gram', 'menit', 'pump', 'pcs'}
    text = ' '.join([word for word in text.split() if word not in satuan_umum])

    for k in keywords:
        text = re.sub(k + r'\s*:?', k, text)

    text = ' '.join([word for word in text.split() if word not in indo_stopwords])
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def get_avg_w2v(tokens, model):
    """Mengambil rata-rata Word2Vec dari token."""
    vectors = [model.wv[w] for w in tokens if w in model.wv]
    if len(vectors) == 0:
        return np.zeros(model.vector_size)
    return np.mean(vectors, axis=0)


def recommended_products(query, df, model, alpha=0.7, beta=0.15, gamma=0.15, top_n=3):
    """Fungsi utama untuk menghasilkan rekomendasi."""
    df_temp = df.copy()

    # Preprocess query
    query_clean = preprocess_text(query)
    query_tokens = query_clean.split()
    query_vec = get_avg_w2v(query_tokens, model).reshape(1, -1)
    X_vectors = np.vstack(df_temp['w2v_vector'].values)

    # Hitung cosine similarity
    cos_sim = cosine_similarity(query_vec, X_vectors)[0]
    df_temp['similarity'] = cos_sim

    # Normalisasi rating & review_count
    df_temp['rating_norm'] = (
        (df_temp['rating'] - df_temp['rating'].min()) /
        (df_temp['rating'].max() - df_temp['rating'].min())
    )
    df_temp['review_norm'] = (
        (df_temp['review_count'] - df_temp['review_count'].min()) /
        (df_temp['review_count'].max() - df_temp['review_count'].min())
    )

    # Skor gabungan
    df_temp['final_score'] = (
        alpha * df_temp['similarity'] +
        beta * df_temp['rating_norm'] +
        gamma * df_temp['review_norm']
    )

    # Ambil top produk per kategori
    result = (
        df_temp.sort_values(by='final_score', ascending=False)
        .groupby('product_type', group_keys=False)
        .head(top_n)
        .sort_values(by='product_type', ascending=True)
        .reset_index(drop=True)
        [['product_type', 'product', 'brand', 'price', 'rating', 'review_count',
          'description', 'image_url', 'similarity', 'final_score']]
    )

    return result

# STREAMLIT APP — FUNGSI UTAMA

def run():
    """Main function untuk menjalankan aplikasi Streamlit."""
    # st.title("Skincare Recommendation App")
    # st.subheader("By SkinMate")
    # Logo
    img = Image.open("./src/image.png")
    st.image(img, caption="Temukan skincare terbaik sesuai kebutuhan kulitmu", use_container_width=True)
    st.markdown(
        "Ceritakan sedikit tentang kondisi kulitmu (misalnya: kering, kusam, atau berjerawat) "
        "untuk mendapatkan rekomendasi produk yang sesuai."
    )

    # Load resources
    model_w2v, df = load_resources()

    # Input user
    query = st.text_input("Ketikkan kebutuhan kulit kamu:")
    top_n = st.selectbox(
    "Jumlah rekomendasi per kategori",
    options=[1, 2, 3, 5, 10],
    index=2)

    # Tampilkan hasil rekomendasi
    if st.button("Dapatkan Rekomendasi") and query.strip() != "":
        with st.spinner("Mencari produk terbaik untuk kamu..."):
            recs = recommended_products(query, df, model_w2v, top_n=top_n)

        st.success("Berikut rekomendasi produk untuk kamu:")

        # Tampilkan hasil per kategori
        for category, group in recs.groupby('product_type', sort=False):
            # Header kategori
            st.markdown(f"# {category.title()}")
            st.divider()

            # Daftar produk di kategori ini
            for _, row in group.iterrows():
                with st.container():
                    st.markdown(f"### {row['product']}")
                    if pd.notna(row['image_url']):
                        st.image(row['image_url'], width=250)
                    st.markdown(
                        f"**Brand:** {row['brand']} | **Tipe:** {category.title()} | **Harga:** Rp{row['price']:,}  |  ⭐ {row['rating']} ({int(row['review_count'])} review)"
                    )
                    st.markdown(f"**Deskripsi:** {row['description']}")
                    st.markdown("---")

    else:
        st.info("Tekan tombol 'Dapatkan Rekomendasi' untuk melihat hasil rekomendasi yang telah kamu tulis.")

# ENTRY POINT
if __name__ == "__main__":
>>>>>>> 847706be8d0a05e67f9cba53f612280ddd5d1a97
    run()