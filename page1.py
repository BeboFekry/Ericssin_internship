import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
from keras.models import load_model
from sklearn.metrics import accuracy_score

st.title('Task 1: Mobile Network Geographical Area')

def prepare():
    if 'model' not in st.session_state:
        if os.path.isfile('scaler.pkl'):
            st.session_state.model = load_model('model.h5')
        else:
            print("model file directory not found!")
    if 'scaler' not in st.session_state:
        if os.path.isfile('scaler.pkl'):
            st.session_state.scaler = pickle.load(open('scaler.pkl','rb'))
        else:
            print("scaler file directory not found!")
    if 'pca' not in st.session_state:
        if os.path.isfile('pca.pkl'):
            st.session_state.pca = pickle.load(open('pca.pkl','rb'))
        else:
            print("pca file directory not found!")

def preprocess(day, type='old'):
    day.drop("cell_id", axis=1, inplace=True)
    day.drop("feature_14", axis=1, inplace=True)
    day.drop("feature_8", axis=1, inplace=True)
    day.drop("feature_18", axis=1, inplace=True)
    day.drop("feature_9", axis=1, inplace=True)
    day.drop("feature_15", axis=1, inplace=True)
    day.drop("feature_2", axis=1, inplace=True)
    if type=='old':
        day["feature_11"] = day['feature_11'].astype(int)
        day['feature_12'] = day['feature_12'].astype('category').cat.codes
        x  = day.iloc[:].values
        x  = st.session_state.scaler.transform(x)
        x  = st.session_state.pca.transform(x)
        return x
    elif type=='current':
        day.insert(10, 'feature_11', [0 for i in range(len(day))])
        day.insert(11, 'feature_12', [0 for i in range(len(day))])
        x = day.iloc[:].values
        return x
    else:
        print("Error: Invalid type!")

def predict(old_day, current_day):
    x_old = preprocess(old_day)
    current_features = preprocess(current_day, type='current')
    # x_old, y_old, yy_old = CreateDS(x=x_old, y=y_old, yy=yy_old)
    yp = {
            "feature_11":[],
            "feature_12":[]
         }
    x_current = []
    for i in range(len(current_features)):
        x = list(x_old[i:]) + x_current[:i]
        x = np.array(x)
        p = st.session_state.model.predict(x.reshape(1,171,1))
        feature_11 = (p[0]>0.5).astype(int)[0,0]
        feature_12 = (p[1]).argmax(axis=1)[0]
        yp['feature_11'].append(feature_11)
        yp['feature_12'].append(feature_12)
        current_features[i][10] = feature_11
        current_features[i][11] = feature_12
        current_features[i] = st.session_state.scaler.transform([current_features[i]])
        x_current.append(st.session_state.pca.transform([current_features[i]])[0])
    yp = pd.DataFrame(yp)
    return yp

def evaluate(y_actual, yp):
    f11_accuracy = accuracy_score(y_actual.feature_11.values, yp.feature_11.values)
    f12_accuracy = accuracy_score(y_actual.feature_12.values, yp.feature_12.values)
    st.write(f"Feature 11 Accuracy: {round(f11_accuracy*100,2)} %")
    st.write(f"Feature 12 Accuracy: {round(f12_accuracy*100,2)} %")

prepare()

uploaded_file = st.file_uploader("Choose the first day 'csv' file...", type=["csv"])
uploaded_file2 = st.file_uploader("Choose the second day 'csv' file...", type=["csv"])

if uploaded_file is not None and uploaded_file2 is not None:
    st.write("---")
    old_day = pd.read_csv(uploaded_file)
    current_day = pd.read_csv(uploaded_file2)
    y_actual = current_day[['feature_11','feature_12']]
    y_actual['feature_11'] = y_actual['feature_11'].astype(int)
    y_actual['feature_12'] = y_actual['feature_12'].astype('category').cat.codes
    current_day.drop("feature_11", axis=1, inplace=True)
    current_day.drop("feature_12", axis=1, inplace=True)

    with st.spinner():
        yp = predict(old_day=old_day, current_day=current_day)

    st.subheader("Actual Values")
    st.data_editor(y_actual, hide_index=True, use_container_width=1, disabled=("feature_11","feature_12"))
    st.subheader("Predicted Values")
    st.data_editor(yp, hide_index=True, use_container_width=1, disabled=("feature_11","feature_12"))
    
    st.write("---")
    st.subheader("Accuracy")
    f11_accuracy = accuracy_score(y_actual.feature_11.values, yp.feature_11.values)
    f12_accuracy = accuracy_score(y_actual.feature_12.values, yp.feature_12.values)
    st.write(f"Feature 11 Accuracy: {round(f11_accuracy*100,2)} %")
    st.write(f"Feature 12 Accuracy: {round(f12_accuracy*100,2)} %")
    st.write("---")

st.write("---")
st.subheader("Run using a stored sample")
if st.button("Run using a stored sample"):
    st.write("---")
    old_day = pd.read_csv(f"features_day1.csv")
    current_day = pd.read_csv(f"features_day2.csv")
    y_actual = current_day[['feature_11','feature_12']]
    y_actual['feature_11'] = y_actual['feature_11'].astype(int)
    y_actual['feature_12'] = y_actual['feature_12'].astype('category').cat.codes
    current_day.drop("feature_11", axis=1, inplace=True)
    current_day.drop("feature_12", axis=1, inplace=True)

    with st.spinner():
        yp = predict(old_day=old_day, current_day=current_day)

    st.subheader("Actual Values")
    st.data_editor(y_actual, hide_index=True, use_container_width=1, disabled=("feature_11","feature_12"))
    st.subheader("Predicted Values")
    st.data_editor(yp, hide_index=True, use_container_width=1, disabled=("feature_11","feature_12"))
    
    st.write("---")
    st.subheader("Accuracy")
    f11_accuracy = accuracy_score(y_actual.feature_11.values, yp.feature_11.values)
    f12_accuracy = accuracy_score(y_actual.feature_12.values, yp.feature_12.values)
    st.write(f"Feature 11 Accuracy: {round(f11_accuracy*100,2)} %")
    st.write(f"Feature 12 Accuracy: {round(f12_accuracy*100,2)} %")
    st.write("---")
