import streamlit as st
from pyowm import OWM
from pyowm.utils.config import get_default_config
import matplotlib.pyplot as plt

API_KEY = "d5cd74ae2cbdb90c0c350d68d5bca315" 
owm = OWM(API_KEY)
mgr = owm.weather_manager()

def get_weather(city):
    try:
        obs = mgr.weather_at_place(city)
        weather = obs.weather
        details = {
            "Status": weather.status,
            "Temperature": weather.temperature('celsius')['temp'],
            "Humidity": weather.humidity,
            "Wind Speed": weather.wind()['speed'],
        }
        return details
    except Exception as e:
        return None

st.title("Weather Forecast App")
city = st.text_input('Enter city, country (e.g., Jabalpur,IN):')
if city:
    data = get_weather(city)
    if data:
        st.write(f"### Weather in {city}")
        for k, v in data.items():
            st.write(f"**{k}**: {v}")
        # Basic Temperature Bar
        fig, ax = plt.subplots()
        ax.bar(["Temperature"], [data["Temperature"]], color='skyblue')
        ax.set_ylabel("Degrees Celsius")
        st.pyplot(fig)
    else:
        st.error("Could not fetch data. Check city name or API key.")
