
import json
import tensorflow as tf
import numpy as np
import os
import random
import string
from flask import Flask, request

app = Flask(__name__)


def pclass_preprocessing(p_class):
    dict_pclass = {'Upper Class':0, 'Middle Class':1, 'Lower Class':2}
    choosen_indx= dict_pclass[p_class]
    
    pclass = np.zeros((1,len(dict_pclass)))
    pclass[0,choosen_indx] = 1
    return pclass

def sex_preprocessing(sex):
    dict_sex = {'Female': 0, 'Male': 1}
    choosen_indx = dict_sex[sex]
    
    sex = np.zeros((1,len(dict_sex)))
    sex[0, choosen_indx] = 1
    return sex


def age_preprocessing(age_num):
    age_group = np.zeros((1,5))
    if 0 < age_num < 15:
        age_group[0, 0] = 1
    elif 15 <= age_num < 30:
        age_group[0, 1] = 1
    elif 30 <= age_num < 45:
        age_group[0, 2] = 1
    elif 45 <= age_num < 60:
        age_group[0, 3] = 1
    else:
        age_group[0, 4] = 1
    return age_group


def family_preprocessing(family_num):
    family_size = np.zeros((1,3))
    if family_num == 0:
        family_size[0,1] = 1
    elif 0 < family_num <= 3:
        family_size[0,2] = 1
    else:
        family_size[0,0] = 1
    return family_size



def family_surv_preprocessing(family_surv):
    dict_survived = {'Yes':2, 'No':0, 'Unknown':1}
    choosen_indx = dict_survived[family_surv]
    
    family_survived = np.zeros((1,len(dict_survived)))
    family_survived[0,choosen_indx] = 1
    return family_survived


def fare_preprocessing(fare_num):
    fare_group = np.zeros((1,7))                                                                                       
    if -0.001< fare_num <= 7.0:
        fare_group[0,0]=1
    elif 7.0< fare_num <= 7.75:
        fare_group[0,1]=1
    elif 7.75< fare_num <= 7.925:
        fare_group[0,2]=1                                                                                             
    elif 7.925< fare_num <= 9.588:
        fare_group[0,3]=1
    elif 9.588< fare_num <= 13.0:
        fare_group[0,4]=1
    elif 13.0< fare_num <= 27.721:
        fare_group[0,5]=1
    else:
        fare_group[0,6]=1
    return fare_group
    
        
def title_preprocessing(title_text):
    dict_title = {'Master':0, 'Young Miss':6, 'Miss':1, 'Mr':2, 'Mrs':3, 'Noble':4, 'Other':5}
    choosen_indx = dict_title[title_text]
    
    title = np.zeros((1,len(dict_title)))
    title[0,choosen_indx] = 1
    return title


def preprocessing_all_data(p_class, sex, age_num, family_num, family_surv, fare_num, title_text):
    pclass = pclass_preprocessing(p_class)
    sex = sex_preprocessing(sex)
    age_group = age_preprocessing(age_num)
    family_size = family_preprocessing(family_num)
    family_survived = family_surv_preprocessing(family_surv)
    fare_group = fare_preprocessing(fare_num)
    title = title_preprocessing(title_text)
    result = np.hstack((pclass, sex, title, age_group, family_size, family_survived, fare_group))
    
    return result


model = tf.keras.models.load_model('basemodel.hdf5')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        p_class = request.form.get('p_class')
        sex = request.form.get('sex')
        age_num = int(request.form.get('age_num'))
        family_num= int(request.form.get('family_num'))
        family_surv= request.form.get('family_surv')
        fare_num = float(request.form.get('fare_num'))
        title_text = request.form.get('title_text')
        result = preprocessing_all_data(p_class, sex, age_num, family_num, family_surv, fare_num, title_text)
        predictions = model.predict(result)
        
        return json.dumps({'prediction':predictions.tolist()})
    
    return 'Welcome to the ml server'



if __name__ == '__main__':
    app.run(debug=True)
