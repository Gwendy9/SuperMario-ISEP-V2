from tkinter import *
import pygame
import subprocess
from PIL import Image, ImageTk

# Dictionnaire de sauvegarde fictif
sauvegarde = {"etat": None}

# Création de la fenêtre
root = Tk()
root.title("SuperMario ISEP")
root.attributes("-fullscreen", True)
root.configure(bg="white")

# Initialisation de la musique avec pygame
pygame.mixer.init()
pygame.mixer.music.load("assets/bande_son/menu/menu.mp3")
pygame.mixer.music.play(-1)

son_impact = pygame.mixer.Sound("assets/bande_son/menu/impact.mp3")
son_start = pygame.mixer.Sound("assets/bande_son/menu/start.mp3")
son_mario = pygame.mixer.Sound("assets/bande_son/menu/mario.mp3")

# === Chargement des images ===
image_mario = PhotoImage(file="assets/images/Mario.png").subsample(2, 2)
titre_jeu = PhotoImage(file="assets/images/menu/OIP.png").subsample(2, 2)

# Image d'arrière-plan pour le menu
image_fond_pil = Image.open("assets/images/menu/image_menu.png")  #
image_fond_pil = image_fond_pil.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
image_fond = ImageTk.PhotoImage(image_fond_pil)

# === MENU PRINCIPAL ===

# Arrière-plan du menu
background_label = Label(root, image=image_fond)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Cadre du menu
cadrer_boutons = Frame(root, bg="white")
cadrer_boutons.place(relx=0.5, rely=0.5, anchor="center")

label_titre = Label(cadrer_boutons, image=titre_jeu, bg="white")
label_titre.pack(pady=20)

# === Effet de texte progressif ===
def afficher_texte_avec_effet(label, texte, i=0):
    if i < len(texte):
        label.config(text=texte[:i + 1])
        root.after(40, lambda: afficher_texte_avec_effet(label, texte, i + 1))

# === Intro  ===
def intro_debut():
    pygame.mixer.music.load("assets/bande_son/menu/dialogue.mp3")
    pygame.mixer.music.play(-1)

    for widget in root.winfo_children():
        widget.destroy()

    root.config(bg="#2e2e2e")
    frame = Frame(root, bg="#2e2e2e")
    frame.pack(expand=True)

    Label(frame, image=image_mario, bg="#2e2e2e").pack(pady=30)

    texte_intro = [
        "? : Qui est là ?",
        "? : Mario, c'est toi ? Je suis un allié, j'ai moi aussi été capturé par Bowser. Tu es connu par ici.",
        "? : Il fait noir n'est ce pas ?",
        "? : Je vis ici depuis des années, je connais tous les secrets du chateau mais je suis trop faible pour m'enfuir.",
        "? : Pourquoi es-tu là ?",
        "? : Quoi ? Peach a été enlevée ?! Encore ?!",
        "? : Je vais t'aider ! En échange, aide moi à m'enfuir.",
        "? : Pour battre Bowser, il te faudra récupérer les 4 morceaux de la Triforce. Je peux te mettre en contact avec les gardiens.",
        "? : Tu es prêt ?"
    ]

    label_texte = Label(frame, text="", font=("Helvetica", 18), bg="#2e2e2e",
                        wraplength=600, justify="center", fg="white")
    label_texte.pack(pady=10)

    index = [0]

    def next_line():
        if index[0] < len(texte_intro):
            afficher_texte_avec_effet(label_texte, texte_intro[index[0]])
            index[0] += 1
            if index[0] == len(texte_intro):
                bouton_suivant.pack_forget()
                bouton_oui.pack(pady=20)

    def continuer():
        son_start.play()
        son_mario.play()
        root.destroy()
        subprocess.Popen(["python", "tir_a_la_corde.py"])



    bouton_suivant = Button(frame, text="Suivant", font=("Poppins", 14), command=next_line)
    bouton_suivant.pack(pady=20)

    bouton_oui = Button(frame, text="Oui !", font=("Poppins", 14), command=continuer)

    next_line()

# === Démarrer le jeu ===
def lancer_jeu():
    son_impact.play()
    intro_debut()

# === Boutons ===
bouton_commencer = Button(cadrer_boutons, text="Commencer", font=("Poppins", 14), command=lancer_jeu)
bouton_commencer.pack(pady=10)

if sauvegarde["etat"] is not None:
    bouton_reprendre = Button(cadrer_boutons, text="Reprendre", font=("Poppins", 14), command=lancer_jeu)
    bouton_reprendre.pack(pady=10)


label_image = Label(cadrer_boutons, image=image_mario, bg="white")
label_image.pack(pady=30)


root.mainloop()
