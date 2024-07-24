import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import io  

API_KEY = 'ea63be12e10815b89962ee5249872b7e'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

def get_weather(city, units='metric'):
    try:
        if not city:
            raise ValueError("City name cannot be empty.")  
        
        params = {
            'q': city,
            'appid': API_KEY,
            'units': units
        }
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        
        if data["cod"] != 200:
            raise Exception(f"Error {data['cod']}: {data['message']}")
        
        weather = {
            'city': data['name'],
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'],
            'wind_speed': data['wind']['speed'],
            'icon': data['weather'][0]['icon']
        }
        return weather
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return None
def show_weather():
    city = city_entry.get()
    units = 'metric' if unit_var.get() == 'Celsius' else 'imperial'
    weather = get_weather(city, units)
    
    if weather:
        icon_url = f"http://openweathermap.org/img/wn/{weather['icon']}@2x.png"
        icon_response = requests.get(icon_url)
        icon_data = icon_response.content
        icon_image = ImageTk.PhotoImage(Image.open(io.BytesIO(icon_data)))

        icon_label.config(image=icon_image)
        icon_label.image = icon_image
        result_label.config(text=f"City: {weather['city']}\n"
                                 f"Temperature: {weather['temperature']}°{'C' if units == 'metric' else 'F'}\n"
                                 f"Description: {weather['description']}\n"
                                 f"Wind Speed: {weather['wind_speed']} {'m/s' if units == 'metric' else 'mph'}")

root = tk.Tk()
root.title("Weather App")
root.configure(bg='#add8e6')  
label_font = ('Helvetica', 12)
button_font = ('Helvetica', 10, 'bold')

city_label = tk.Label(root, text="Enter City:", bg='#add8e6', font=label_font)
city_label.pack(pady=5)

city_entry = tk.Entry(root, font=label_font)
city_entry.pack(pady=5)

unit_var = tk.StringVar(value='Celsius')
celsius_radio = tk.Radiobutton(root, text='Celsius', variable=unit_var, value='Celsius', bg='#add8e6', font=label_font)
celsius_radio.pack(pady=5)
fahrenheit_radio = tk.Radiobutton(root, text='Fahrenheit', variable=unit_var, value='Fahrenheit', bg='#add8e6', font=label_font)
fahrenheit_radio.pack(pady=5)

get_weather_button = tk.Button(root, text="Get Weather", command=show_weather, font=button_font, bg='#87CEEB')
get_weather_button.pack(pady=10)

result_label = tk.Label(root, text="", justify='left', bg='#add8e6', font=label_font)
result_label.pack(pady=10)

icon_label = tk.Label(root, bg='#add8e6')
icon_label.pack(pady=10)
root.mainloop()
