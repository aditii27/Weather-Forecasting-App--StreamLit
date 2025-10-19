import streamlit as st
from pyowm import OWM
from pyowm.utils.config import get_default_config
import matplotlib.pyplot as plt
import plotly.graph_objects as go

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

weather_icons = {
    "Clear": "☀️",
    "Clouds": "☁️",
    "Rain": "🌧️",
    "Snow": "❄️",
    "Mist": "🌫️",
    "Thunderstorm": "⛈️",
    "Drizzle": "🌦️"
}

st.title("Weather Forecast App")
city = st.text_input('Enter city, country (e.g., Jabalpur,IN):')
if city:
    data = get_weather(city)
    if data:
        # Emoji and City Name
        st.write(f"## Weather in {city} {weather_icons.get(data['Status'], '🌎')}")
        # Three metric columns
        col1, col2, col3 = st.columns(3)
        col1.metric("Temperature (°C)", f"{data['Temperature']}°C")
        col2.metric("Humidity (%)", f"{data['Humidity']}%")
        col3.metric("Wind Speed (m/s)", f"{data['Wind Speed']} m/s")

        # Plotly gauge chart for temperature
        fig1 = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = data["Temperature"],
            title = {'text': "Temperature (°C)"},
            gauge = {
                'axis': {'range': [-10, 50]},
                'bar': {'color': "#1e90ff"},
                'steps': [
                    {'range': [-10, 0], 'color': "#b0e0e6"},
                    {'range': [0, 20], 'color': "#90ee90"},
                    {'range': [20, 35], 'color': "#ffd700"},
                    {'range': [35, 50], 'color': "#ff6347"}
                ]
            }))
        st.plotly_chart(fig1, use_container_width=True)

        # Original matplotlib bar chart
        fig2, ax = plt.subplots()
        ax.bar(["Temperature"], [data["Temperature"]], color='skyblue')
        ax.set_ylabel("Degrees Celsius")
        st.pyplot(fig2)
    else:
        st.error("Could not fetch data. Check city name or API key.")
