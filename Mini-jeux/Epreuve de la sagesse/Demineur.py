from tkinter import *
from random import choice
from tkinter import messagebox
import json
from PIL import Image, ImageTk
import pygame

# bande_son
pygame.mixer.init()

pygame.mixer.music.load("bande_son/fond.mp3")
pygame.mixer.music.play(-1)

son_perdu = pygame.mixer.Sound("bande_son/perdu.mp3")
son_un_de_plus = pygame.mixer.Sound("bande_son/un_de_plus.mp3")
son_gagne = pygame.mixer.Sound("bande_son/gagne.mp3")

#interface

root = Tk()
root.title("L'épreuve de la sagesse : Démineur")
root.attributes('-fullscreen', True)

   #images
monstre_image = PhotoImage(file="images/monstre_demineur.png").subsample(8, 8)

      # background
img = Image.open("images/background.png")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

img = img.resize((screen_width, screen_height),  Image.Resampling.LANCZOS)
background_image = ImageTk.PhotoImage(img)

background = Label(root, image=background_image)
background.place(relwidth=1, relheight=1)

       # Canvas au centre, au-dessus du fond
canvas = Canvas(root, width=500, height=500,  highlightthickness=0)
canvas.pack(expand=True)

Sauvegarde = { "etat": None, "score": 0, "Coordonnes_monstres": [], "rectangles_noir": [], "cases_non_cliquee": []}

def sauvegarde():
    with open("Sauvegarde.json", "w") as fichier:
        json.dump(Sauvegarde, fichier, indent=5)

def chargement():
    global Sauvegarde
    try:
        with open("Sauvegarde.json", 'r') as fichier:
            Sauvegarde = json.load(fichier)
            rafraichir_canvas()
    except FileNotFoundError:
        pass

def rafraichir_canvas():
    canvas.delete("all")
    dessiner_terrain()
    for z in Sauvegarde["rectangles_noir"]:
        coordonnees = z[0]
        nbr = z[1]
        canvas.create_rectangle(coordonnees, width=2, fill="black")
        canvas.create_text(coordonnees[0] + 25, coordonnees[1] + 25, text=nbr, fill="white", font='poppins')

    if Sauvegarde["etat"] == "perdu" :
        for i in Sauvegarde["Coordonnes_monstres"]:
            canvas.create_rectangle(i, width=2, fill="#b34700")
            canvas.create_image(i[0] + 25, i[1] + 25, image=monstre_image)

    if Sauvegarde["etat"] == "gagné" :
        for i in Sauvegarde["Coordonnes_monstres"]:
            canvas.create_rectangle(i, width=2, fill="#b34700")


# Initialisation des cases
if Sauvegarde["cases_non_cliquee"]== []:
    Sauvegarde["cases_non_cliquee"] = [[50 * i, 50 * j, 50 + 50 * i, 50 + 50 * j] for j in range(10) for i in range(10)]

if Sauvegarde["Coordonnes_monstres"]==[]:
    for _ in range(10):
        a = choice(Sauvegarde["cases_non_cliquee"])
        Sauvegarde["Coordonnes_monstres"].append(a)
        Sauvegarde["cases_non_cliquee"].remove(a)

def dessiner_terrain():
    canvas.create_image(0, 0, image=background_image, anchor=NW)
    for i in range(10):
        for j in range(10):
            canvas.create_rectangle(50 * i, 50 * j, 50 + 50 * i, 50 + 50 * j, width=2, fill="#2e2e2e")

def quand_clique(event):
    if Sauvegarde["etat"] == "perdu":
        messagebox.showinfo("Résultat", f"GAME OVER ! Votre score est de: {Sauvegarde['score']}")
        root.destroy()

    elif Sauvegarde["etat"] == "gagné":
        messagebox.showinfo("Résultat", "Félicitations, vous avez trouvé tous les carrés non minés !")
        root.destroy()
    else:
        carre(event.x, event.y)

def carre(x, y):
    nbr_bombes = 0

    # Si clic sur une bombe
    for i in Sauvegarde["Coordonnes_monstres"]:
        if i[0] <= x <= i[2] and i[1] <= y <= i[3]:
            canvas.create_rectangle(i, width=2, fill="#b34700")
            canvas.create_image(i[0] + 25, i[1] + 25, image=monstre_image)
            Sauvegarde["etat"] = "perdu"

            son_perdu.play()

            rafraichir_canvas()
            return

    # Si clic sur une case sans bombe
    for j in Sauvegarde["cases_non_cliquee"]:
        if j[0] <= x <= j[2] and j[1] <= y <= j[3]:
            for n in Sauvegarde["Coordonnes_monstres"]:
                if (n[0] >= j[0] - 50 and n[0] <= j[0] + 50) and (n[1] >= j[1] - 50 and n[1] <= j[1] + 50):
                    nbr_bombes += 1
            Sauvegarde["rectangles_noir"].append([j, nbr_bombes])
            Sauvegarde["cases_non_cliquee"].remove(j)
            Sauvegarde["score"] += 1

            son_un_de_plus.play()

            if Sauvegarde["score"] == 90:
                Sauvegarde["etat"] = "gagné"

                son_gagne.play()

            rafraichir_canvas()
            return

# Boutons
bouton_sauvegarde = Button(root, text="💾 Sauvegarder", font=("Arial", 14), command=sauvegarde)
bouton_sauvegarde.pack(pady=10)

bouton_chargement = Button(root, text="🔄 Chargement (dernière sauvegarde)", font=("Arial", 14), command=chargement)
bouton_chargement.pack(pady=10)

Sauvegarde["etat"] = "en cours"
canvas.bind("<Button-1>", quand_clique)
dessiner_terrain()

root.mainloop()
