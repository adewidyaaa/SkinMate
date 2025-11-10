<<<<<<< HEAD
import streamlit as st
import Prediction
import Homepage
import EDA

st.set_page_config(
    page_title='SkinMate App',
    layout='centered',
    initial_sidebar_state='expanded'
)

page = st.sidebar.selectbox('Pilih Halaman: ', ('Homepage', 'EDA', 'Prediction'))

if page == 'Homepage':
    Homepage.run()
elif page == 'EDA':
    EDA.run()
else:
=======
import streamlit as st
import Prediction
import Homepage
import EDA

st.set_page_config(
    page_title='SkinMate App',
    layout='centered',
    initial_sidebar_state='expanded'
)

page = st.sidebar.selectbox('Pilih Halaman: ', ('Homepage', 'EDA', 'Prediction'))

if page == 'Homepage':
    Homepage.run()
elif page == 'EDA':
    EDA.run()
else:
>>>>>>> 847706be8d0a05e67f9cba53f612280ddd5d1a97
    Prediction.run()