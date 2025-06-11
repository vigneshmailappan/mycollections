import random
import tkinter as tk
from tkinter import ttk, messagebox

# Tamil letter categories
uyir_letters = ['அ', 'ஆ', 'இ', 'ஈ', 'உ', 'ஊ', 'எ', 'ஏ', 'ஐ', 'ஒ', 'ஓ', 'ஔ']
mei_base_letters = ['க', 'ங', 'ச', 'ஞ', 'ட', 'ண', 'த', 'ந', 'ப', 'ம',
                    'ய', 'ர', 'ல', 'வ', 'ழ', 'ள', 'ற', 'ன']
mei_letters = [mei + '்' for mei in mei_base_letters]
vowel_signs = ['', 'ா', 'ி', 'ீ', 'ு', 'ூ', 'ெ', 'ே', 'ை', 'ொ', 'ோ', 'ௌ']
uyirmei_letters = {mei: [mei + sign for sign in vowel_signs if sign] for mei in mei_base_letters}

# Combine all letters for the "All" category
all_letters = uyir_letters + mei_letters + [letter for sublist in uyirmei_letters.values() for letter in sublist]

right_score = 0
wrong_score = 0

# Category-specific shown letters
shown_letters_by_category = {
    "Uyir": set(),
    "Mei": set(),
    "UyirMei": {mei: set() for mei in mei_base_letters},
    "All": set()
}

# Function to show a random letter
def show_random_letter():
    global current_letter
    category = category_var.get()

    if category == "Uyir":
        available = [l for l in uyir_letters if l not in shown_letters_by_category["Uyir"]]
        if not available:
            shown_letters_by_category["Uyir"].clear()
            available = uyir_letters
        current_letter = random.choice(available)
        shown_letters_by_category["Uyir"].add(current_letter)

    elif category == "Mei":
        available = [l for l in mei_letters if l not in shown_letters_by_category["Mei"]]
        if not available:
            shown_letters_by_category["Mei"].clear()
            available = mei_letters
        current_letter = random.choice(available)
        shown_letters_by_category["Mei"].add(current_letter)

    elif category == "UyirMei":
        consonant = consonant_var.get()
        available = [l for l in uyirmei_letters[consonant] if l not in shown_letters_by_category["UyirMei"][consonant]]
        if not available:
            shown_letters_by_category["UyirMei"][consonant].clear()
            available = uyirmei_letters[consonant]
        current_letter = random.choice(available)
        shown_letters_by_category["UyirMei"][consonant].add(current_letter)

    else:  # All
        available = [l for l in all_letters if l not in shown_letters_by_category["All"]]
        if not available:
            shown_letters_by_category["All"].clear()
            available = all_letters
        current_letter = random.choice(available)
        shown_letters_by_category["All"].add(current_letter)

    label.config(text=current_letter)

# Function to update scores
def update_score(is_right):
    global right_score, wrong_score
    if is_right:
        right_score += 1
        right_label.config(text=f"Right ✅: {right_score}")
    else:
        wrong_score += 1
        wrong_label.config(text=f"Wrong ❌: {wrong_score}")

    if right_score >= 10:
        messagebox.showinfo("Victory!", "🎉 You won! Great job!")
        reset_game()
    elif wrong_score >= 10:
        messagebox.showinfo("Game Over", "😢 You lost. Try again!")
        reset_game()
    else:
        show_random_letter()

# Function to reset the game
def reset_game():
    global right_score, wrong_score
    right_score = 0
    wrong_score = 0
    right_label.config(text="Right ✅: 0")
    wrong_label.config(text="Wrong ❌: 0")
    for key in shown_letters_by_category:
        if isinstance(shown_letters_by_category[key], dict):
            for subkey in shown_letters_by_category[key]:
                shown_letters_by_category[key][subkey].clear()
        else:
            shown_letters_by_category[key].clear()
    show_random_letter()
    enable_buttons()

# Disable buttons after game ends
def disable_buttons():
    right_button.config(state="disabled")
    wrong_button.config(state="disabled")

# Enable buttons for new game
def enable_buttons():
    right_button.config(state="normal")
    wrong_button.config(state="normal")

# Enable/disable consonant dropdown based on category
def update_consonant_dropdown(*args):
    if category_var.get() == "UyirMei":
        consonant_menu.config(state="readonly")
        consonant_menu.pack(pady=20)
    else:
        consonant_menu.config(state="disabled")
        consonant_menu.pack_forget()

# GUI setup
root = tk.Tk()
root.title("Tamil Letter for Kids")

category_var = tk.StringVar(value="All")
category_var.trace("w", update_consonant_dropdown)
category_menu = ttk.Combobox(root, textvariable=category_var, values=["All", "Uyir", "Mei", "UyirMei"],
                             font=("Arial", 24))
category_menu.pack(pady=20)

consonant_var = tk.StringVar(value=mei_base_letters[0])
consonant_menu = ttk.Combobox(root, textvariable=consonant_var, values=mei_base_letters, font=("Arial", 24),
                              state="disabled")

label = tk.Label(root, text="", font=("Arial", 200))
label.pack(pady=30)

score_frame = tk.Frame(root)
score_frame.pack()

right_label = tk.Label(score_frame, text="Right ✅: 0", font=("Arial", 20), fg="green")
right_label.grid(row=0, column=0, padx=20)

wrong_label = tk.Label(score_frame, text="Wrong ❌: 0", font=("Arial", 20), fg="red")
wrong_label.grid(row=0, column=1, padx=20)

button_frame = tk.Frame(root)
button_frame.pack(pady=20)

right_button = tk.Button(button_frame, text="Right ✅", font=("Arial", 20), command=lambda: update_score(True),
                         bg="lightgreen")
right_button.grid(row=0, column=0, padx=10)

wrong_button = tk.Button(button_frame, text="Wrong ❌", font=("Arial", 20), command=lambda: update_score(False),
                         bg="tomato")
wrong_button.grid(row=0, column=1, padx=10)

reset_button = tk.Button(root, text="Reset 🔄", font=("Arial", 24), command=reset_game)
reset_button.pack(pady=10)

show_random_letter()
root.mainloop()
