import tkinter as tk
from PIL import Image, ImageTk
root = tk.Tk()
root.title("L'épreuve de la force : Tir à la Corde")
root.attributes('-fullscreen', True)

canvas = tk.Canvas(root, width=800, height=400)
canvas.pack()
background_image = Image.open("background.png")
background_photo = ImageTk.PhotoImage(background_image)
canvas.create_image(0, 0, image=background_photo)


rope_position = 400
player_clicks = 0
robot_clicks = 0

rope_segments = []
segment_length = 30
num_segments = 11

def create_rope():
    for i in range(num_segments):
        x = 150 + i * segment_length
        segment = canvas.create_line(x, 200, x + segment_length, 200, width=15, fill="brown")
        rope_segments.append(segment)
        canvas.tag_bind(segment, "<Button-1>", player_click)

def player_click(event):
    global player_clicks
    player_clicks += 1

def robot_click():
    global robot_clicks
    robot_clicks += 1
    root.after(250, robot_click)

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
        show_winner("Mario gagne !")
        return
    elif rope_position >= 650:
        rope_position = 650
        update_sprites()
        show_winner("Le gardien gagne !")
        return

    for i, segment in enumerate(rope_segments):
        x = 150 + i * segment_length + (rope_position - 400)
        canvas.coords(segment, x, 200, x + segment_length, 200)

    update_sprites()
    root.after(50, update_game)

def show_winner(message):
    canvas.create_text(400, 300, text=message, font=("Arial", 24), fill="green")

create_rope()

player1_images = [tk.PhotoImage(file=f"Mario_tir_{i}.png") for i in range(1, 4)]
player2_images = [tk.PhotoImage(file=f"player2_effort_{i}.png") for i in range(1, 4)]
player1 = canvas.create_image(100, 175, image=player1_images[0])
player2 = canvas.create_image(700, 175, image=player2_images[0])

update_game()
robot_click()

root.mainloop()
