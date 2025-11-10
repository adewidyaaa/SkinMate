# SkinMate : Your Skin Soulmate

## Repository Outline

```
1. README.md - Penjelasan gambaran umum project
2. /dataset_scraping  
   Folder berisi hasil scraping dari masing-masing tipe produk skincare :
   - cleanser_full.csv
   - moisturizer_full.csv
   - serm_essence_full.csv
   - sun_protection_full.csv
   - toner_full.csv
3. /deployment  
   Folder berisi script atau file terkait deployment aplikasi di Hugging Face
4. data_cleaning.ipynb - Proses pembersihan dataset mentah menjadi dataset yang siap untuk dilakukan modelling
5. data_validation.ipynb - Validasi data menggunakan Great Expectations
6. eda.ipynb - Eksplorasi data dan analisis insight
7. model_inference.ipynb - Proses inferensi dan pembobotan hasil rekomendasi (70% similarity, 15% rating, 15% review)
8. model_NLP_Word2Vec.ipynb - Pembangunan model Word2Vec untuk representasi deskripsi produk
9. scraping.ipynb - Proses scraping data dari website Female Daily
10. project_url.txt - Berisi link Streamlit dashboard dan Google Form evaluasi pengguna
11. skincare_clean.csv - Dataset akhir setelah proses data cleaning
12. skincare.csv - Dataset mentah hasil penggabungan data scraping

```


## Problem Background
Kesadaran terhadap kesehatan kulit terus meningkat setiap tahunnya, tidak hanya di kalangan perempuan, tetapi juga laki-laki yang kini semakin peduli terhadap perawatan kulit. Fenomena ini mendorong meningkatnya minat masyarakat terhadap produk skincare yang sesuai dengan kebutuhan dan kondisi kulit masing-masing.

Namun, di tengah maraknya informasi mengenai produk perawatan kulit, banyak pengguna masih kesulitan menemukan produk yang benar-benar cocok. Mereka harus mencari rekomendasi produk dari satu sumber, lalu berpindah ke platform lain untuk melihat ulasan atau rating pengguna. Hal ini membuat proses pemilihan produk menjadi tidak efisien dan memakan waktu.

Melalui pengembangan platform SkinMate, pengguna dapat dengan mudah menemukan produk skincare yang sesuai dengan skin concern mereka dalam satu tempat. Dengan memasukkan permasalahan kulit yang dialami, pengguna akan mendapatkan rekomendasi produk yang relevan, lengkap dengan rating dan review dari pengguna lain sebagai bahan pertimbangan tambahan.

Project ini bertujuan untuk menciptakan pengalaman pencarian skincare yang lebih personal, efisien, dan terpercaya, sekaligus membantu pengguna membuat keputusan pembelian yang lebih tepat.

## Project Output
Project ini menghasilkan:
1. Dashboard sederhana berbasis Streamlit yang menampilkan hasil eksplorasi data skincare dalam bentuk visualisasi dan insight.
2. Model rekomendasi berbasis konten (Content-Based Hybrid Recommendation) yang menggabungkan kemiripan deskripsi produk (Word2Vec) dengan faktor rating dan jumlah review menggunakan bobot:
- 70% kemiripan deskripsi (Word2Vec + Cosine Similarity)
- 15% rating produk
- 15% jumlah review
3. Dataset skincare bersih dan terstruktur, hasil scraping dan pembersihan data dari website Female Daily.
4. Analisis insight data mengenai brand, kategori, serta hubungan antara harga, rating, dan jumlah review produk.


## Data
Dataset digunakan merupakan data hasil scraping dari website femaledaily.com
Data yang diambil sebanyak :
- Cleanser : 220 data
- Moisturizer : 220 data
- Serum/essence : 220 data
- Sun protection : 220 data
- Toner : 220 data

Karakteristik dataset awal :
- Jumlah Kolom : 9 kolom
- Jumlah Baris : 1080 baris

## Method
Metode dan alur kerja project:
1. Mengambil data produk skincare dari website Female Daily menggunakan Selenium.
2. Melakukan data cleaning, validasi, dan eksplorasi data menggunakan Python & Great Expectations.
3. Melatih model Word2Vec untuk merepresentasikan teks deskripsi produk.
4. Menghitung kemiripan antar produk menggunakan Cosine Similarity.
5. Membangun dashboard interaktif dengan Streamlit untuk menampilkan insight dan sistem rekomendasi produk skincare.


## Stacks
Teknologi dan tools yang digunakan:
- Programming: Python
- Web Scraping: Selenium
- Data Analysis: Pandas, NumPy, Matplotlib, Seaborn
- Data Validation: Great Expectations
- Modelling: Gensim (Word2Vec), Scikit-learn (Cosine Similarity)
- App & Deployment: Streamlit
- Environment: VS Code, Jupyter Notebook