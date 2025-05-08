from tkinter import *
from random import choice
from tkinter import messagebox
import json
from PIL import Image, ImageTk
import pygame

# Initialisation de la musique avec pygame
pygame.mixer.init()
pygame.mixer.music.load("assets/images/epreuve_sagesse/fond.mp3")
pygame.mixer.music.play(-1)

son_perdu = pygame.mixer.Sound("assets/bande_son/epreuve_sagesse/perdu.mp3")
son_un_de_plus = pygame.mixer.Sound("assets/bande_son/epreuve_sagesse/un_de_plus.mp3")
son_gagne = pygame.mixer.Sound("assets/images/epreuve_sagesse/gagne.mp3")

# Interface
root = Tk()
root.title("L'épreuve de la sagesse : Démineur")
root.attributes('-fullscreen', True)

# Chargement des images (introduction)
images = {
    "cutscene": PhotoImage(file="assets/images/epreuve_sagesse/pixelated_blended_image.png"),
    "start": PhotoImage(file="assets/images/epreuve_sagesse/Mario.png")
}

# Fonction pour afficher du texte avec un effet d'écriture
def afficher_texte_avec_effet(label, texte, i=0):
    if i < len(texte):
        label.config(text=texte[:i + 1])
        root.after(40, lambda: afficher_texte_avec_effet(label, texte, i + 1))

# ----------------- Intro du jeu -------------- #
def intro():
    for widget in root.winfo_children():
        widget.destroy()
    root.config(bg="black")
    img = images["cutscene"]
    canvas = Canvas(root, width=img.width(), height=img.height(), highlightthickness=0, bd=0)
    canvas.pack()
    canvas.create_image(0, 0, image=img, anchor="nw")
    texte = "Pas mal pas mal !\n MAIS il te manque un \n morceau de la triforce !"
    texte_id = canvas.create_text(660, 180, text="", font=("Helvetica", 20, "bold"), fill="black", anchor="n", justify="center")
    def taper_le_texte(i=0):
        if i <= len(texte):
            canvas.itemconfig(texte_id, text=texte[:i])
            root.after(35, lambda: taper_le_texte(i + 1))
    taper_le_texte()
    root.bind("<Button-1>", lambda e: intro_demineur())

def intro_demineur():
    root.unbind("<Button-1>")
    for widget in root.winfo_children():
        widget.destroy()
    root.config(bg="#2e2e2e")
    frame = Frame(root, bg="#2e2e2e")
    frame.pack(expand=True)

    Label(frame, image=images["start"], bg="#2e2e2e").pack(pady=30)

    texte_intro = " Il te faut maintenant réussir l'épreuve de la sagesse... On m'a dit qu'il fallait éviter les monstres..."
    label_texte = Label(frame, text="", font=("Helvetica", 18), bg="#2e2e2e", wraplength=400, justify="center", fg="white")
    label_texte.pack(pady=10)

    def bouton_start():
        Button(frame, text="Commencer", font=("Helvetica", 16), bg="#64b5f6", fg="white", activebackground="#42a5f5",
               command=lancer_jeu).pack(pady=20)

    afficher_texte_avec_effet(label_texte, texte_intro)
    root.after(len(texte_intro) * 55, bouton_start)

# ----------------- Lancer le Jeu -------------- #
def lancer_jeu():
    for widget in root.winfo_children():
        widget.destroy()

    global monstre_image, background_image, canvas
    Sauvegarde["etat"] = "en cours"

# images jeu
    monstre_image = PhotoImage(file="assets/images/epreuve_sagesse/monstre_demineur.png").subsample(8, 8)

    img = Image.open("assets/images/epreuve_sagesse/background.png")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    img = img.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
    background_image = ImageTk.PhotoImage(img)

    background = Label(root, image=background_image)
    background.place(relwidth=1, relheight=1)
 #canvas du jeu
    canvas = Canvas(root, width=500, height=500, highlightthickness=0)
    canvas.pack(expand=True)

    bouton_sauvegarde = Button(root, text="💾 Sauvegarder", font=("Arial", 14), command=sauvegarde)
    bouton_sauvegarde.pack(pady=10)

    bouton_chargement = Button(root, text="🔄 Chargement (dernière sauvegarde)", font=("Arial", 14), command=chargement)
    bouton_chargement.pack(pady=10)

    canvas.bind("<Button-1>", quand_clique)
    dessiner_terrain()

# ----------------- Sauvegarde -------------- #
Sauvegarde = {"etat": None, "score": 0, "Coordonnes_monstres": [], "rectangles_noir": [], "cases_non_cliquee": []}

def sauvegarde():
    with open("Sauvegarde_demineur.json", "w") as fichier:
        json.dump(Sauvegarde, fichier, indent=5)

def chargement():
    try:
        with open("Sauvegarde_demineur.json", 'r') as fichier:
            data = json.load(fichier)
            Sauvegarde.update(data)
            rafraichir_canvas()
    except FileNotFoundError:
        pass

def rafraichir_canvas():
    canvas.delete("all")
    dessiner_terrain()
    for z in Sauvegarde["rectangles_noir"]:
        coordonnees, nbr = z
        canvas.create_rectangle(coordonnees, width=2, fill="black")
        canvas.create_text(coordonnees[0] + 25, coordonnees[1] + 25, text=nbr, fill="white", font='poppins')

    if Sauvegarde["etat"] == "perdu":
        for i in Sauvegarde["Coordonnes_monstres"]:
            canvas.create_rectangle(i, width=2, fill="#b34700")
            canvas.create_image(i[0] + 25, i[1] + 25, image=monstre_image)

    if Sauvegarde["etat"] == "gagné":
        for i in Sauvegarde["Coordonnes_monstres"]:
            canvas.create_rectangle(i, width=2, fill="#b34700")

# ----------------- Initialisation du terrain -------------- #
if not Sauvegarde["cases_non_cliquee"]:
    Sauvegarde["cases_non_cliquee"] = [[50 * i, 50 * j, 50 + 50 * i, 50 + 50 * j] for j in range(10) for i in range(10)]

if not Sauvegarde["Coordonnes_monstres"]:
    for _ in range(10):
        a = choice(Sauvegarde["cases_non_cliquee"])
        Sauvegarde["Coordonnes_monstres"].append(a)
        Sauvegarde["cases_non_cliquee"].remove(a)

def dessiner_terrain():
    for i in range(10):
        for j in range(10):
            canvas.create_rectangle(50 * i, 50 * j, 50 + 50 * i, 50 + 50 * j, width=2, fill="#2e2e2e")

def quand_clique(event):
    if Sauvegarde["etat"] == "perdu":
        messagebox.showinfo("Résultat", f"GAME OVER ! Tu vas devoir recommencer ! Votre score est de: {Sauvegarde['score']}")
        root.destroy()
    elif Sauvegarde["etat"] == "gagné":
        messagebox.showinfo("Résultat", "Félicitations, vous avez trouvé tous les carrés non minés !")
        root.destroy()
    else:
        carre(event.x, event.y)

def carre(x, y):
    nbr_bombes = 0
    for i in Sauvegarde["Coordonnes_monstres"]:
        if i[0] <= x <= i[2] and i[1] <= y <= i[3]:
            canvas.create_rectangle(i, width=2, fill="#b34700")
            canvas.create_image(i[0] + 25, i[1] + 25, image=monstre_image)
            Sauvegarde["etat"] = "perdu"
            son_perdu.play()
            rafraichir_canvas()
            return

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

# ----------------- Lancement ----------------- #
intro()
root.mainloop()
