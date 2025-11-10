<<<<<<< HEAD
import streamlit as st
from PIL import Image

def run():
    # Judul Halaman
    st.title("Skincare Recommendation App")
    st.subheader("Personalized Skincare Suggestions Based on Your Skin Needs - By SkinMate")

    # Gambar Utama
    img = Image.open("./src/image.png")
    st.image(img, caption="Temukan skincare terbaik sesuai kebutuhan kulitmu", use_container_width=True)

    # Deskripsi
    st.write(
        """
        **SkinMate** adalah sistem rekomendasi skincare yang membantu pengguna menemukan produk yang paling sesuai
        dengan kondisi dan kebutuhan kulit mereka.  

        Proyek ini berfokus pada pemahaman kebutuhan skincare pengguna melalui informasi produk dan memberikan rekomendasi 
        yang bersifat personal sesuai preferensi masing-masing.  

        Solusi ini bertujuan untuk **mempermudah, memperjelas, dan membuat proses pemilihan skincare menjadi lebih menyenangkan**
        """
    )

# ENTRY POINT
if __name__ == "__main__":
=======
import streamlit as st
from PIL import Image

def run():
    # Judul Halaman
    st.title("Skincare Recommendation App")
    st.subheader("Personalized Skincare Suggestions Based on Your Skin Needs - By SkinMate")

    # Gambar Utama
    img = Image.open("./src/image.png")
    st.image(img, caption="Temukan skincare terbaik sesuai kebutuhan kulitmu", use_container_width=True)

    # Deskripsi
    st.write(
        """
        **SkinMate** adalah sistem rekomendasi skincare yang membantu pengguna menemukan produk yang paling sesuai
        dengan kondisi dan kebutuhan kulit mereka.  

        Proyek ini berfokus pada pemahaman kebutuhan skincare pengguna melalui informasi produk dan memberikan rekomendasi 
        yang bersifat personal sesuai preferensi masing-masing.  

        Solusi ini bertujuan untuk **mempermudah, memperjelas, dan membuat proses pemilihan skincare menjadi lebih menyenangkan**
        """
    )

# ENTRY POINT
if __name__ == "__main__":
>>>>>>> 847706be8d0a05e67f9cba53f612280ddd5d1a97
    run()