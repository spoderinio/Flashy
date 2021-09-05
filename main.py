from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"

def choose_languages():
    KNOWN_LANGUAGE = ""
    LEARNING_LANGUAGE = ""


    def button_click():
        global LEARNING_LANGUAGE
        global KNOWN_LANGUAGE
        LEARNING_LANGUAGE = len_to_learn.get()
        KNOWN_LANGUAGE = know_len.get()
        with open("./data/usr_len.txt", mode="w") as usr_len:
            usr_len.write(F"{LEARNING_LANGUAGE}\n{KNOWN_LANGUAGE}")


    def close_window():
        window.destroy()

    window = Tk()
    window.title("Choose languages")
    window.minsize(width=300, height=100)
    window.config(padx=20, pady=20)

    len_to_learn = Entry(width=20)
    len_to_learn.grid(column=1, row=1)

    know_len = Entry(width=20)
    know_len.grid(column=1,row=2)
    know_len.insert(0, "Български")

    len_to_learn_lable = Label(text="Learning language")
    len_to_learn_lable.grid(column=0, row=1)

    known_len_lable = Label(text="Known language")
    known_len_lable.grid(column=0, row=2)

    enter_button = Button(text="Enter", command=lambda:[button_click(), close_window()])
    enter_button.grid(column=2, row=2)

    langueges = Label(text="Available languages: English, Deutsch, Norwegian, French, Български")
    langueges.grid(row=0, column=0, columnspan=2)


    window.mainloop()

    return LEARNING_LANGUAGE, KNOWN_LANGUAGE



# ---------------------------- FLASHCARD SETUP ------------------------------- #
try:
    word_df = pandas.read_csv("./data/words_to_learn.csv")
    with open("./data/usr_len.txt", "r") as data:
        mylines = []
        for myline in data:
            mylines.append(myline)
        LEARNING_LANGUAGE = mylines[0].strip("\n")
        KNOWN_LANGUAGE = mylines[1]
except FileNotFoundError:
    choose_languages()
    word_df = pandas.read_csv("./data/words.csv")

to_learn = word_df.to_dict(orient="records")
current_card = {}


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text=LEARNING_LANGUAGE,fill="black")
    canvas.itemconfig(card_word, text=current_card[LEARNING_LANGUAGE], fill="black")
    canvas.itemconfig(canvas_img, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(canvas_img, image=card_back_img)
    canvas.itemconfig(card_title, text=KNOWN_LANGUAGE, fill="white")
    canvas.itemconfig(card_word, text=current_card[KNOWN_LANGUAGE], fill="white")


def remove_from_list():
    global current_card
    to_learn.remove(current_card)
    to_learn_df = pandas.DataFrame(to_learn)
    to_learn_df.to_csv("./data/words_to_learn.csv", index=False)

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, flip_card)

canvas = Canvas(height=530, width=800, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="./images/card_front.png")
card_back_img = PhotoImage(file="./images/card_back.png")
canvas_img = canvas.create_image(400, 265, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)


#Buttons
known_image = PhotoImage(file="./images/right.png")
known_button = Button(image=known_image, highlightthickness=0, command=lambda:[next_card(), remove_from_list()])
known_button.grid(row=1, column=1)

cross_image = PhotoImage(file="./images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

next_card()

print(len(to_learn))












window.mainloop()
