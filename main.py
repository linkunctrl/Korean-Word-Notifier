from customtkinter import CTkImage
from PIL import Image, ImageTk
import customtkinter as ctk
import datetime
import json
import random


app = ctk.CTk()

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")  
app.geometry("600x550")
#app.iconbitmap("assets/app_icon.ico")
app.title("Korean Word Notifier")

MATCHA_GREEN = "#B2D3B6"
STRAWBERRY_PINK = "#F7C6CE"
PETAL_PINK = "#FAD9E6"
TEXT_COLOR = "#444444"

def get_learned_words():
    try:
        with open("learned.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    
def get_vocab():
    with open("vocab_data.json", "r", encoding="utf-8") as file:
        return json.load(file)

def save_to_history(word):
    today = datetime.date.today().isoformat()
    try:
        with open("history.json", "r", encoding="utf-8") as file:
            history = json.load(file)
    except FileNotFoundError:
        history = []

    history.append({"date": today, "word": word})
    with open("history.json", "w", encoding="utf-8") as file:
        json.dump(history, file, ensure_ascii=False, indent=2)

def get_new_word():
    vocab = get_vocab()
    learned = get_learned_words()
    learned_set = {w["word"] for w in learned}
    unlearned = [w for w in vocab if w["word"] not in learned_set]

    if not unlearned:
        return {
            "word": "🎉 다 했어요!",
            "meaning": "You’ve learned everything!",
            "example": "단어를 모두 배웠습니다!"
        }

    selected = random.choice(unlearned)
    save_to_history(selected)
    return selected


word_data = get_new_word()
word_kr = word_data["word"]
word_en = word_data["meaning"]
example = word_data["example"]

read_img = ctk.CTkImage(Image.open("assets/read.png"), size=(100,100))
glasses_img = ctk.CTkImage(Image.open("assets/glasses.png"), size=(100,100))


frame = ctk.CTkFrame(master=app, fg_color=MATCHA_GREEN)
frame.pack(fill="both", expand=True, padx=10, pady=10)

icon_label = ctk.CTkLabel(frame, image=read_img, text="")
icon_label.pack(pady=(6,15))

title_label = ctk.CTkLabel(frame, text = "한국어 단어 알리미 : 갑시다", font=("Consolas", 20, "bold"), text_color=TEXT_COLOR, bg_color=MATCHA_GREEN)
title_label.pack(pady=(5, 2))
title_label2 = ctk.CTkLabel(frame, text = "Korean Word Notifier : Let's go", font=("Consolas", 20, "bold"), text_color=TEXT_COLOR, bg_color=MATCHA_GREEN)
title_label2.pack(pady=(0, 10))

label_word_kr = ctk.CTkLabel(frame, text=word_kr, font=("Consolas", 32, "bold"), text_color="black", bg_color=MATCHA_GREEN)
label_word_kr.pack(pady=(0,10))

label_eng = ctk.CTkLabel(frame, text=word_en, font=("Consolas", 24, "bold"), text_color="black", bg_color=MATCHA_GREEN)
label_eng.pack(pady=(0, 20))

example_label = ctk.CTkLabel(frame, text=f"📘 Example: {example}", font=("Consolas", 16, "bold"), text_color=TEXT_COLOR, bg_color=MATCHA_GREEN)
example_label.pack(pady=(0, 20))



def mark_as_learned():
    icon_label.configure(image=glasses_img)
    learned = get_learned_words()
    learned.append(word_data)
    with open("learned_words.json", "w", encoding="utf-8") as f:
        json.dump(learned, f, ensure_ascii=False, indent=2)
        
def open_time_panel():
    time_window = ctk.CTkToplevel(app)
    time_window.title("Set Notification Time")
    time_window.geometry("300x200")
    time_window.configure(fg_color=MATCHA_GREEN)
    ctk.CTkLabel(time_window, text="Set Time", font= ("Consolas", 14, "bold"), text_color=TEXT_COLOR).pack(pady=(10,5))

    hour_var = ctk.StringVar(value="08")
    minute_var = ctk.StringVar(value="00")
    
    hour_entry = ctk.CTkEntry(time_window, textvariable=hour_var, width=50)
    hour_entry.pack(pady=5)
    minute_entry = ctk.CTkEntry(time_window, textvariable=minute_var, width=50)
    minute_entry.pack(pady=5)
    
    def save_time():
        notif_time = {"hour": int(hour_var.get()), "minute": int(minute_var.get())}
        with open("notif_time.json", "w", encoding="utf-8") as file:
            json.dump(notif_time, file)
        time_window.destroy()
    
    save_btn = ctk.CTkButton(time_window, text="Save", command=save_time, fg_color=STRAWBERRY_PINK)
    save_btn.pack(pady=10)



learned_btn = ctk.CTkButton(frame, text="✅ Mark as Learned", command=mark_as_learned, fg_color=STRAWBERRY_PINK, hover_color=PETAL_PINK, text_color=TEXT_COLOR, font=("Consolas", 16, "bold"))
learned_btn.pack(pady=20)

time_btn = ctk.CTkButton(frame, text="⏰ Set Daily Time", command=open_time_panel, fg_color=PETAL_PINK, text_color=TEXT_COLOR)
time_btn.pack(pady=(10, 5))

app.mainloop()
