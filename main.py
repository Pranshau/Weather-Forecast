import streamlit as st
import plotly.express as px
from backend import get_data

# Add title, text input, slider, selectbox, and subheader
st.title("Weather Forecast For the Next Days")
place = st.text_input("Place: ")
days = st.slider("Forecast Days", min_value=1, max_value=5,
                 help="Select the number of forecasted days")
option = st.selectbox("Select data to view",
                      ("Temperature", "Sky"))
st.subheader(f"{option} for the next {days} days in {place}")

if place:
    # Get the temperature/Sky data
    try:
        filtered_data = get_data(place, days)

        if option == "Temperature":
            temperatures = [data["main"]["temp"] / 10 for data in filtered_data]
            dates = [data["dt_txt"] for data in filtered_data]
            # Create a temperature plot
            figure = px.line(x=dates, y=temperatures, labels={"x": "Date", "y": "Temperature (c)"})
            st.plotly_chart(figure)

        if option == "Sky":
            images = {"Clear": "images/clear.png", "Clouds": "images/cloud.png",
                      "Rain": "images/rain.png", "Snow": "images/snow.png"}
            sky_conditions = [data["weather"][0]["main"] for data in filtered_data]

            # Display images based on sky conditions

            for condition in sky_conditions:
                if condition in images:
                    st.image(images[condition], caption=condition, width=150)
                else:
                    st.write(f"No image available for {condition}")
    except KeyError:
        st.write("That place does not exist")
