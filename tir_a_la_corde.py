import tkinter as tk
from PIL import Image, ImageTk
import subprocess

root = tk.Tk()
root.title("Tir à la Corde")

canvas = tk.Canvas(root, width=800, height=400)
canvas.pack()

background_image = Image.open("assets/images/epreuve_force/background.png")
background_photo = ImageTk.PhotoImage(background_image)
canvas.create_image(0, 0, image=background_photo, anchor=tk.NW)

# Position centrale de la corde
rope_position = 400

# Dimensions réglables de la corde (en pixels)
rope_width = 300
rope_height = 20

# Compteurs de clics
player_clicks = 0
robot_clicks = 0

# Référence au rectangle de corde
rope_rect = None

def create_rope():
    global rope_rect
    x0 = rope_position - rope_width // 2
    y0 = 200 - rope_height // 2
    x1 = rope_position + rope_width // 2
    y1 = 200 + rope_height // 2
    rope_rect = canvas.create_rectangle(x0, y0, x1, y1, fill="brown")

def player_click(event):
    global player_clicks
    if event.x < 400:  # Partie gauche de l'écran
        player_clicks += 1

def robot_click():
    global robot_clicks
    robot_clicks += 1
    root.after(600, robot_click)

def update_sprites():
    player_effort = min(2, max(0, int((400 - rope_position) / 84)))
    robot_effort = min(2, max(0, int((rope_position - 400) / 84)))

    canvas.itemconfig(player1, image=player1_images[player_effort])
    canvas.itemconfig(player2, image=player2_images[robot_effort])

def update_game():
    global rope_position, player_clicks, robot_clicks

    if player_clicks > 0:
        rope_position -= 5
        player_clicks -= 1

    if robot_clicks > 0:
        rope_position += 5
        robot_clicks -= 1

    if rope_position <= 150:
        rope_position = 150
        update_sprites()
        show_winner("Tu as gagné THUNG THUNG SHUR !")
        subprocess.Popen(["python", "pendu.py"])
        root.destroy()
        return
    elif rope_position >= 650:
        rope_position = 650
        update_sprites()
        show_winner("Bouh tu as perdu THUNG THUNG SHUR !")

        return

    # Mettre à jour la position du rectangle de la corde
    x0 = rope_position - rope_width // 2
    y0 = 200 - rope_height // 2
    x1 = rope_position + rope_width // 2
    y1 = 200 + rope_height // 2
    canvas.coords(rope_rect, x0, y0, x1, y1)

    update_sprites()
    root.after(50, update_game)

def show_winner(message):
    canvas.create_text(400, 275, text=message, font=("Arial", 18), fill="black")

# --- Initialisation du jeu ---
create_rope()

player1_images = [tk.PhotoImage(file=f"assets/images/epreuve_force/Mario_tir_{i}.png") for i in range(1, 4)]
player2_images = [tk.PhotoImage(file=f"assets/images/epreuve_force/player2_effort_{i}.png") for i in range(1, 4)]

player1 = canvas.create_image(100, 175, image=player1_images[0])
player2 = canvas.create_image(700, 175, image=player2_images[0])

canvas.bind("<Button-1>", player_click)  # Clic sur la partie gauche

update_game()
robot_click()

root.mainloop()
