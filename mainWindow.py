import tkinter as tk
import speech_recognition as sr
import webbrowser
from ytmusicapi import YTMusic
from PIL import Image, ImageTk, ImageDraw
from tuya_control import turn_on_light, turn_off_light, set_light_color
from time_functions import get_current_time, get_current_date, start_timer_from_text, stop_timer
from pc_functions import run_malwarebytes_cleanup, shutdown_pc

root = tk.Tk()
root.title("VoiceHelper")
root.geometry("300x300")

label = tk.Label(root, text="Press the button, after talk to me!")
label.pack(pady=20)

ytmusic = YTMusic()

bulb_setting_active = False
# Function to handle voice input
def listen_to_voice():
    global bulb_setting_active
    print("Listening function started")
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        label.config(text="Listening...")
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening for audio...")
        audio = recognizer.listen(source)
        print("Audio captured")

    try:
        text = recognizer.recognize_google(audio, language="en-US").lower()
        print(f"User said: {text}")  # Output to terminal
        label.config(text=f"You said: {text}")

        # Activating light setting mode
        if "setting with bulb" in text:
            print("Setting with light. What setting do you want?")
            label.config(text="What setting do you want?")
            bulb_setting_active = True
            return

        if bulb_setting_active:  # Check if light setting mode is active
            if "turn on" in text:
                print("Turning on light")
                turn_on_light()
                label.config(text="Light turned ON")
            elif "turn off" in text:
                print("Turning off light")
                turn_off_light()
                label.config(text="Light turned OFF")
            elif "set color" in text or "set colour" in text:
                color = text.replace("set color", "").replace("set colour", "").strip()
                if color:
                    print(f"Setting color to {color}")
                    response = set_light_color(color)
                    label.config(text=f"Light set to {color}" if "success" in response else "Error setting color")
                else:
                    print("No color specified")
                    label.config(text="Please specify a color")
            else:
                print("Unknown command")
                label.config(text="Unknown command")
        else:
            print("First, activate 'setting with bulb' mode")
            label.config(text="Please activate 'setting with bulb' mode first")

            # Google search
            if "search" in text and "in google" in text:
                search_query = text.replace("search", "").replace("in google", "").strip()
                if search_query:
                    print(f"Searching Google for: {search_query}")
                    label.config(text=f"Searching: {search_query}")
                    webbrowser.open(f"https://www.google.com/search?q={search_query}")
                else:
                    print("No search query specified")
                    label.config(text="Please specify a search query")

            # YouTube search
            elif "search" in text and "in youtube" in text:
                search_query = text.replace("search", "").replace("in youtube", "").strip()
                if search_query:
                    print(f"Searching YouTube for: {search_query}")
                    label.config(text=f"Searching YouTube: {search_query}")
                    webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")
                else:
                    print("No search query specified")
                    label.config(text="Please specify a search query")

            # Search and auto-play song on YouTube Music
            if "search song" in text:
                song_query = text.replace("search song", "").strip()
                if song_query:
                    print(f"Searching for song: {song_query}")
                    label.config(text=f"Playing song: {song_query}")

                    # Searching for track on YouTube Music
                    search_results = ytmusic.search(song_query, filter="songs")

                    if search_results:
                        song_id = search_results[0]['videoId']  # Get the first track ID
                        song_url = f"https://music.youtube.com/watch?v={song_id}"  # Form the URL
                        webbrowser.open(song_url)  # Open the song in a browser
                    else:
                        label.config(text="Song not found")
                        print("Song not found")
                else:
                    print("No song specified")
                    label.config(text="Please specify a song name")

            # Handling time and date requests
            if "what time is it" in text:
                current_time = get_current_time()
                print(f"Current time: {current_time}")

            elif "what date today" in text:
                current_date = get_current_date()
                print(f"Current date: {current_date}")

            elif "start timer on" in text:
                start_timer_from_text(text)

            elif "stop timer" in text:
                stop_timer()

            # Scan through Malwarebytes
            if "scan my pc" or "scan my PC" in text:
                print("Starting Malwarebytes cleanup...")
                label.config(text="Starting cleanup...")
                run_malwarebytes_cleanup()

            # Turn of pc
            if "turn of pc" in text:
                print("Turning of pc...")
                label.config(text="Turning of pc...")
                shutdown_pc()

    except sr.UnknownValueError:
        print("Could not understand the audio")
        label.config(text="Could not understand")
    except sr.RequestError:
        print("Speech recognition service error")
        label.config(text="Service error")

# Button size
canvas_size = 120
button_radius = canvas_size // 2
canvas = tk.Canvas(root, width=canvas_size, height=canvas_size, bg="white", highlightthickness=0)
canvas.pack()

# Button background (gray circle)
button_color = "#DCDCDC"
pressed_color = "#BEBEBE"

# Create a circle with a transparent background
circle_image = Image.new("RGBA", (canvas_size, canvas_size), (255, 255, 255, 0))
draw = ImageDraw.Draw(circle_image)
draw.ellipse((0, 0, canvas_size, canvas_size), fill=button_color)

# Load, resize, and center the icon
icon = Image.open("Img/img_microphone.png").convert("RGBA")
icon = icon.resize((50, 50), Image.LANCZOS)
circle_image.paste(icon, ((canvas_size - 50) // 2, (canvas_size - 50) // 2), icon)

# Convert to Tkinter format
circle_tk = ImageTk.PhotoImage(circle_image)
button_circle = canvas.create_image(button_radius, button_radius, image=circle_tk)

# Function to change color when pressed
def on_press(event):
    dark_circle = Image.new("RGBA", (canvas_size, canvas_size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(dark_circle)
    draw.ellipse((0, 0, canvas_size, canvas_size), fill=pressed_color)
    dark_circle.paste(icon, ((canvas_size - 50) // 2, (canvas_size - 50) // 2), icon)
    dark_circle_tk = ImageTk.PhotoImage(dark_circle)
    canvas.itemconfig(button_circle, image=dark_circle_tk)
    canvas.image = dark_circle_tk

def on_release(event):
    print("Button released, starting voice recognition...")
    canvas.itemconfig(button_circle, image=circle_tk)
    listen_to_voice()

# Bind events
canvas.tag_bind(button_circle, "<Button-1>", on_press)
canvas.tag_bind(button_circle, "<ButtonRelease-1>", on_release)

root.mainloop()
