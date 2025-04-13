import pandas as pd
import streamlit as st
import json
import requests
import matplotlib.pyplot as plt

st.title("Weather App 🌤️")
st.subheader("Enter a city name to see current weather or forecast.")
api_key='3e1e57b36b71498089f92200242809'
option=st.radio("Choose an option:",["Current Weather","Forecast"])

if option=="Current Weather":
    city = st.text_input("Enter city name here:")
    if st.button("Display Weather Information"):
        base_url = f"http://api.weatherapi.com/v1/current.json?key=3e1e57b36b71498089f92200242809&q={city}&aqi=no"
        response = requests.get(base_url)


        if (response.status_code == 200):
            data = response.json()
            st.write(f"The name of the city is: {data['location']['name']}")
            st.write(f"The name of the region is: {data['location']['region']}")
            st.write(f"The local time is: {data['location']['localtime']}")
            st.write(f"The Temperature of the city is: {data['current']['temp_c']} C")
            st.write(f"The weather feels like: {data["current"]["condition"]["text"]}")

            img_url = data["current"]["condition"]["icon"]
            img_url = "https:" + img_url
            st.image(img_url)

            st.subheader("City On Map")
            lat = data["location"]["lat"]
            lon = data["location"]["lon"]
            dictx = {'lat': [lat], "lon": [lon]}
            df = pd.DataFrame(dictx)
            st.map(df)

        else:
            st.error("The weather info for the city could not be fetched...please try again.")

if option=="Forecast":
    city=st.text_input("Enter city name here:")
    days=st.number_input("Enter number of days:",min_value=0)
    if st.button("Forecast Weather"):
        base_url = f"http://api.weatherapi.com/v1/forecast.json?key=3e1e57b36b71498089f92200242809&q={city}&days={days}&aqi=no&alerts=no"
        response = requests.get(base_url)
        if response.status_code == 200:
            st.write("You have been blessed by the forecast data")
            data = response.json()
            # with open("Forecast.json","w") as file:
            #     json.dump(data,file,indent=4)
            #     print("The forecast data shines down upon you....")

            days = data["forecast"]["forecastday"]

            t = days[0]['hour']

            time_list = []
            temp_list = []

            for i in t:
                time_list.append(i['time'])
                temp_list.append(i["temp_c"])

            fig=plt.figure(figsize=(10, 6))
            plt.plot(time_list, temp_list, marker='p', color='r', mec='k')
            plt.xticks(rotation=90)
            plt.grid()
            plt.xlabel("Time")
            plt.ylabel("Temperature(Celsius)")
            plt.title(f"Weather forecast for {city}")
            st.pyplot(fig)

        else:
            st.error("Enter a proper city name 😡")
