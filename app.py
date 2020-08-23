
import streamlit as st
import numpy as np
from cv2 import imread
import requests
import json


@st.cache(persist=True)
def interactions():
    title_text = st.sidebar.selectbox("Which title has your Passanger?",
                                     ('Master', 'Young Miss', 'Miss', 'Mr', 'Mrs', 'Noble', 'Other'))
    
    p_class = st.sidebar.radio("Social-Economical Passanger Status: ",
                                   ("Upper Class", "Middle Class", 'Lower Class'),
                                   key='P_class')
    
    fare_num = st.sidebar.number_input("Ticket cost per family member: ", 0.1, 600.0, step=5.0, key='Fare_num')
    
    sex = st.sidebar.radio("Sex: ", ("Female", "Male"), key='Sex')
    
    age_num = st.sidebar.slider("Age of Passanger: ", 1, 80, key='Age_num')

    family_num = st.sidebar.slider("How many family members on the bort?", 0, 10, key='Family_num')
    
    if family_num != 0:
        family_surv = st.sidebar.radio("Anybody survived in this family?", ('Yes', "No"), key='Family_surv')
    else:
        family_surv = 'Unknown'
        
    return p_class, sex, age_num, family_num, family_surv, fare_num, title_text


def main():
    URI = 'http://127.0.0.1:5000'
    
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
#     local_css('style.css')
    
    st.title("Titanic disaster")
    st.image(imread('titanic.jpg'), width = 500)
    st.sidebar.title("Pass")

    p_class, sex, age_num, family_num, family_surv, fare_num, title_text = interactions()
    
    if st.sidebar.button('Get predictions'):

        response = requests.post(URI, data={'p_class':p_class,
                                           'sex':sex,
                                           'age_num':age_num,
                                           'family_num':family_num,
                                           'family_surv':family_surv,
                                           'fare_num':fare_num,
                                           'title_text':title_text})
        response = json.loads(response.text)
        preds = response.get('prediction')[0][0]

        st.write(f"The passenger's probability of surviving is {round(preds*100, 2)}% ")


if __name__ == '__main__':
    main()
