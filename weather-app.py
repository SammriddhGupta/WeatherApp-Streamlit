import streamlit as st
import requests
import pandas as pd
from datetime import datetime,time
from PIL import Image

api_key = st.secrets["api_key"]

url_current = 'https://api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}'

url_oneCall = 'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={part}&appid={API key}'

def getweather(city):
    result = requests.get(url_current.format(city, api_key))
    if result:
        json = result.json()
        country = json['sys']['country']
        temp = json['main']['temp'] - 273.15
        temp_feels = json['main']['feels_like'] - 273.15
        humid = json['main']['humidity'] - 273.15
        icon = json['weather'][0]['icon']
        lon = json['coord']['lon']
        lat = json['coord']['lat']
        des = json['weather'][0]['description']
        res = [country, round(temp,1), round(temp_feels,1),humid,lon,lat,icon,des]
        return res, json
    else:
        print("Error in Search!")
        

def get_hist_data(lat, lon, start):
    res = requests.get(url_oneCall.format(lat, lon, start, api_key))
    data = res.json()
    temp = []
    for hour in data["hourly"]:
        t = hour["temp"]
        temp.append(t)
        return data,temp
    
# writing the streamlit app

st.title("Sam's Weather Reporting")

im1 = st.columns(1)

image = Image.open('img.png')
st.image(image, caption="This is my stack", use_column_width=True)

col1,col2 = st.columns(2)

with col1:
    city = st.text_input("Please enter your city name")
with col2:
        if city:
            res, json = getweather(city)
            st.success('Current: '+ str(round(res[1],2)))
            st.info('Feels like: '+ str(round(res[2],2)))
            #st.info('Humidity: '+ str(round(res[3],2)))
            st.subheader('Status: '+ res[7])
            web_str = "![Alt Text]"+"(http://openweathermap.org/img/wn/"+str(res[6])+"@2x.png"
            st.markdown(web_str)