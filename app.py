
import streamlit as st
import numpy as np
from cv2 import imread
import requests
import json
import base64


# All interactions with user
def interactions():
    title_text = st.sidebar.selectbox("Which title has your Passenger?",
                                     ('Master', 'Young Miss', 'Miss', 'Mr', 'Mrs', 'Noble', 'Other'))
    
    p_class = st.sidebar.radio("Social-Economical Passenger Status: ",
                                   ("Upper Class", "Middle Class", 'Lower Class'),
                                   key='P_class')
    
    fare_num = st.sidebar.number_input("Ticket cost per family member: ", 0.0, 600.0, step=5.0, key='Fare_num')
    
    sex = st.sidebar.radio("Sex: ", ("Female", "Male"), key='Sex')
    
    age_num = st.sidebar.slider("Age of Passenger: ", 1, 80, key='Age_num')

    family_num = st.sidebar.slider("How many family members on the bort?", 0, 10, key='Family_num')
    
    if family_num != 0:
        family_surv = st.sidebar.radio("Anybody survived in this family?", ('Yes', "No"), key='Family_surv')
    else:
        family_surv = 'Unknown'
        
    return p_class, sex, age_num, family_num, family_surv, fare_num, title_text
        

#Read image from file    
@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


#Set backgroud image
def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/jpg;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return


# Set text style
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        return


def main():
    URI = 'http://127.0.0.1:5000'
    
    local_css('text.css')
    set_png_as_page_bg('background.jpg')
    
    st.title("Titanic disaster")
    st.header('The wreck of Titanic - a sea disaster that occurred 1912 in the North Atlantic Ocean')
    st.markdown("Can you create a passenger that could survive in this terrible disaster?")
    st.image(imread('titanic.jpg'), width = 400)
    
    st.sidebar.markdown("""<font color="black"
    font-family = "Times"
    font-size = "14pt"
    font-style = "normal"
    font-weight = "Normal">Let's select the characteristics of your Passenger</font>""", unsafe_allow_html=True)

    p_class, sex, age_num, family_num, family_surv, fare_num, title_text = interactions()
    
    if st.sidebar.button('Get predictions'):
        # Send data to server in 'data'
        response = requests.post(URI, data={'p_class':p_class,
                                           'sex':sex,
                                           'age_num':age_num,
                                           'family_num':family_num,
                                           'family_surv':family_surv,
                                           'fare_num':fare_num,
                                           'title_text':title_text})
        #read json response
        response = json.loads(response.text)
        #take information
        preds = response.get('prediction')[0][0]
                    
        st.markdown(f"The Passenger's probability of surviving is {round(preds*100, 2)}%")
    return

if __name__ == '__main__':
    main()
