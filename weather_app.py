import tkinter as tk
from tkinter import messagebox
import requests
from datetime import datetime

API_KEY = "3e8cfa82b3deefd7861ab74908cef7da"

history = []

# ---------------- Fetch Weather ---------------- #
def get_weather():
    city = city_entry.get().strip()

    if city == "":
        messagebox.showwarning("Warning", "Please enter a city name.")
        return

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            messagebox.showerror("Error", "City not found!")
            return

        city_name = data["name"]
        country = data["sys"]["country"]
        temp = data["main"]["temp"]
        feels = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        weather = data["weather"][0]["main"]
        description = data["weather"][0]["description"]

        sunrise = datetime.fromtimestamp(
            data["sys"]["sunrise"]
        ).strftime("%I:%M %p")

        sunset = datetime.fromtimestamp(
            data["sys"]["sunset"]
        ).strftime("%I:%M %p")

        if weather == "Clear":
            icon = "☀️"
        elif weather == "Clouds":
            icon = "☁️"
        elif weather == "Rain":
            icon = "🌧️"
        elif weather == "Thunderstorm":
            icon = "⛈️"
        elif weather == "Snow":
            icon = "❄️"
        else:
            icon = "🌤️"

        result.config(
            text=f"""
{icon} {weather}

📍 City : {city_name}, {country}

🌡 Temperature : {temp:.1f} °C

🤗 Feels Like : {feels:.1f} °C

💧 Humidity : {humidity} %

🌬 Wind Speed : {wind} m/s

🌡 Pressure : {pressure} hPa

🌅 Sunrise : {sunrise}

🌇 Sunset : {sunset}

📝 {description.title()}
""")

        history.insert(0, city_name)

        if len(history) > 5:
            history.pop()

        history_box.delete(0, tk.END)

        for item in history:
            history_box.insert(tk.END, item)

    except Exception:
        messagebox.showerror(
            "Error",
            "Check your internet connection."
        )


# ---------------- Window ---------------- #

root = tk.Tk()
root.title("Weather Report")
root.geometry("650x750")
root.configure(bg="#E3F2FD")
root.resizable(False, False)

title = tk.Label(
    root,
    text="🌦 Weather Report",
    font=("Segoe UI",22,"bold"),
    bg="#E3F2FD",
    fg="#0D47A1"
)
title.pack(pady=15)

city_entry = tk.Entry(
    root,
    font=("Segoe UI",14),
    justify="center",
    width=30
)
city_entry.pack(pady=10)

search_btn = tk.Button(
    root,
    text="Search Weather",
    command=get_weather,
    bg="#1976D2",
    fg="white",
    font=("Segoe UI",12,"bold"),
    width=18
)
search_btn.pack(pady=15)

card = tk.Frame(
    root,
    bg="#1565C0",
    width=520,
    height=320,
    bd=4,
    relief="ridge"
)
card.pack()
card.pack_propagate(False)

result = tk.Label(
    card,
    text="Search a city to view weather",
    font=("Segoe UI",12,"bold"),
    bg="#1565C0",
    fg="white",
    justify="left"
)
result.pack(pady=20)
# ---------------- Clear Search History ---------------- #

def clear_history():
    history.clear()
    history_box.delete(0, tk.END)


# ---------------- Buttons ---------------- #

button_frame = tk.Frame(root, bg="#E3F2FD")
button_frame.pack(pady=15)

copy_btn = tk.Button(
    button_frame,
    text="Clear History",
    command=clear_history,
    bg="#D32F2F",
    fg="white",
    font=("Segoe UI",11,"bold"),
    width=15
)
copy_btn.grid(row=0, column=0, padx=10)

exit_btn = tk.Button(
    button_frame,
    text="Exit",
    command=root.destroy,
    bg="#455A64",
    fg="white",
    font=("Segoe UI",11,"bold"),
    width=15
)
exit_btn.grid(row=0, column=1, padx=10)


# ---------------- Previous Searches ---------------- #

history_title = tk.Label(
    root,
    text="📜 Previous Searches",
    font=("Segoe UI",13,"bold"),
    bg="#E3F2FD",
    fg="#0D47A1"
)
history_title.pack(pady=(15,5))

history_box = tk.Listbox(
    root,
    width=40,
    height=6,
    font=("Segoe UI",11),
    justify="center"
)
history_box.pack(pady=10)


# ---------------- Footer ---------------- #

footer = tk.Label(
    root,
    text="Weather Report Application\nDeveloped using Python, Tkinter & OpenWeather API",
    font=("Segoe UI",10,"italic"),
    bg="#E3F2FD",
    fg="gray"
)
footer.pack(side="bottom", pady=15)


# ---------------- Run App ---------------- #

root.mainloop()