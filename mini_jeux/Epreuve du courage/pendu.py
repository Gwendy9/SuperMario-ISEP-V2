import tkinter as tk
from PIL import Image, ImageTk
import random

# ------------ Configuration ------------ #
image_paths = {
    "cutscene": "images\pixelated_blended_image.png",
    "start": "images\Mario.png",
    "step0": "images\Mario.png",
    "step1": "images\Mario_pendu_1.png",
    "step2": "images\Mario_pendu_2.png",
    "step3": "images\Mario_pendu_3.png",
    "step4": "images\Mario_pendu_4.png",
    "gameover": "images\mouhahahaha.png"
}

words_easy = ["chat", "papa", "nez", "lait", "feu", "main", "eau", "clé", "sac", "jour"]
words_medium = ["maison", "camion", "fenêtre", "histoire", "chaise", "gâteau", "chaussure", "plafond", "matelas", "voiture"]

# ------------ Globals ------------ #
mot = ""
lettres_trouvees = []
essais_restants = 5
images = {}
etape_image = 0
niveau_actuel = "easy"

fenetre = tk.Tk()
fenetre.title("🎮 Jeu du Pendu")
fenetre.attributes("-fullscreen", True)
fenetre.config(bg="#fff8dc")
fenetre.geometry("800x600")
fenetre.bind("<Escape>", lambda e: fenetre.attributes("-fullscreen", False))

# ------------ Utils ------------ #
def afficher_texte_avec_effet(label, texte, i=0):
    if i < len(texte):
        label.config(text=texte[:i+1])
        fenetre.after(40, lambda: afficher_texte_avec_effet(label, texte, i+1))

def afficher_mot_partiel():
    return ' '.join([lettre if lettre in lettres_trouvees else '_' for lettre in mot])

# ------------ Cutscene ------------ #
def intro():
    for widget in fenetre.winfo_children():
        widget.destroy()
    fenetre.config(bg="black")
    img = images.get("cutscene")
    canvas = tk.Canvas(fenetre, width=img.width(), height=img.height(), highlightthickness=0, bd=0)
    canvas.pack()
    canvas.create_image(0, 0, image=img, anchor="nw")
    texte = "Ne t’emballe pas trop…\nc’est à moi de jouer maintenant."
    texte_id = canvas.create_text(660, 180, text="", font=("Helvetica", 20, "bold"), fill="black", anchor="n", justify="center")
    def taper_le_texte(i=0):
        if i <= len(texte):
            canvas.itemconfig(texte_id, text=texte[:i])
            fenetre.after(35, lambda: taper_le_texte(i + 1))
    taper_le_texte()
    fenetre.bind("<Button-1>", lambda e: intro_marche())

def intro_marche():
    fenetre.unbind("<Button-1>")
    for widget in fenetre.winfo_children():
        widget.destroy()
    fenetre.config(bg="#fff8dc")
    frame = tk.Frame(fenetre, bg="#fff8dc")
    frame.pack(expand=True)
    image_intro = images.get("start")
    tk.Label(frame, image=image_intro, bg="#fff8dc").pack(pady=30)
    texte_intro = "Bienvenue dans l’aventure ! Le premier jeu est... Le Pendu 🎯"
    label_texte = tk.Label(frame, text="", font=("Helvetica", 18), bg="#fff8dc", wraplength=400, justify="center")
    label_texte.pack(pady=10)
    def bouton_start():
        tk.Button(frame, text="Commencer", font=("Helvetica", 16), bg="#64b5f6", fg="white",
                  activebackground="#42a5f5", command=lambda: lancer_jeu("easy")).pack(pady=20)
    afficher_texte_avec_effet(label_texte, texte_intro)
    fenetre.after(len(texte_intro) * 55, bouton_start)

# ------------ Game Logic ------------ #
def lancer_jeu(niveau):
    global mot, lettres_trouvees, essais_restants, etape_image, niveau_actuel
    niveau_actuel = niveau
    mot = random.choice(words_easy if niveau == "easy" else words_medium)
    lettres_trouvees = []
    essais_restants = 5
    etape_image = 0
    for widget in fenetre.winfo_children():
        widget.destroy()
    afficher_interface_jeu()
    afficher_mot()
    maj_image()

def afficher_interface_jeu():
    global image_label, etiquette_mot, entree, bouton_verifier, etiquette_resultat
    image_label = tk.Label(fenetre, bg="#fff8dc")
    image_label.pack(pady=10)
    etiquette_mot = tk.Label(fenetre, text="", font=("Courier", 24), bg="#fff8dc")
    etiquette_mot.pack(pady=10)
    entree = tk.Entry(fenetre, font=("Helvetica", 16), justify="center")
    entree.pack()
    bouton_verifier = tk.Button(fenetre, text="Vérifier", font=("Helvetica", 16), bg="#e57373", fg="white",
                                activebackground="#ef5350", command=verifier_lettre)
    bouton_verifier.pack(pady=10)
    etiquette_resultat = tk.Label(fenetre, text="", font=("Helvetica", 18, "bold"), bg="#fff8dc", justify="center")
    etiquette_resultat.pack(pady=30)

def afficher_mot():
    etiquette_mot.config(text=afficher_mot_partiel())

def maj_image():
    image = images.get(f"step{etape_image}")
    image_label.config(image=image)
    image_label.image = image

def verifier_lettre():
    global essais_restants, etape_image
    lettre = entree.get().lower()
    entree.delete(0, tk.END)
    if lettre in mot and lettre not in lettres_trouvees:
        lettres_trouvees.append(lettre)
    else:
        if lettre not in lettres_trouvees:
            essais_restants -= 1
            etape_image += 1
    afficher_mot()
    maj_image()
    if essais_restants == 0:
        bouton_verifier.config(state=tk.DISABLED)
        fenetre.after(2000, afficher_echec_animé)
    elif all(l in lettres_trouvees for l in mot):
        bouton_verifier.config(state=tk.DISABLED)
        if niveau_actuel == "easy":
            transition_vers_niveau("Oh, tu as gagné… hmm... essaye celui-ci alors 😏", "medium")
        else:
            afficher_victoire_finale()

# ------------ Transitions ------------ #
def transition_vers_niveau(message, niveau_suivant):
    for widget in fenetre.winfo_children():
        widget.destroy()
    fenetre.config(bg="#fffde7")
    tk.Label(fenetre, text=message, font=("Helvetica", 18, "italic"), bg="#fffde7",
             wraplength=400, justify="center").pack(pady=100)
    fenetre.after(2500, lambda: lancer_jeu(niveau_suivant))

def afficher_victoire_finale():
    for widget in fenetre.winfo_children():
        widget.destroy()
    fenetre.config(bg="#dcedc8")
    tk.Label(fenetre, text="🎉 Bravo ! Tu as terminé tous les niveaux ! 🎉",
             font=("Helvetica", 20, "bold"), bg="#dcedc8", fg="#2e7d32").pack(pady=40)
    canvas = tk.Canvas(fenetre, width=200, height=200, bg="#dcedc8", highlightthickness=0)
    canvas.pack()
    canvas.create_oval(50, 50, 150, 150, fill="yellow", outline="black", width=2)
    canvas.create_oval(75, 80, 85, 90, fill="black")
    canvas.create_oval(115, 80, 125, 90, fill="black")
    canvas.create_arc(75, 100, 125, 140, start=0, extent=-180, style=tk.ARC, width=2)
    tk.Button(fenetre, text="Rejouer", font=("Helvetica", 14), bg="#64b5f6", fg="white", command=intro).pack(pady=20)

# ------------ Perte avec animation ------------ #
def afficher_echec_animé():
    for widget in fenetre.winfo_children():
        widget.destroy()
    try:
        image = Image.open(image_paths["gameover"]).resize((800, 600))
        bg = ImageTk.PhotoImage(image)
    except Exception as e:
        print("Erreur chargement image :", e)
        return
    canvas = tk.Canvas(fenetre, width=800, height=600, highlightthickness=0, bd=0)
    canvas.pack()
    canvas.bg = bg
    canvas.create_image(0, 0, image=bg, anchor="nw")
    texte = "Je le savais... tu allais perdre. 😈"
    texte_id = canvas.create_text(400, 520, text="", font=("Helvetica", 20, "bold"), fill="black", anchor="n")
    def taper_le_texte(i=0):
        if i <= len(texte):
            canvas.itemconfig(texte_id, text=texte[:i])
            fenetre.after(50, lambda: taper_le_texte(i + 1))
    taper_le_texte()

# ------------ Load Images ------------ #
def charger_images():
    for key, path in image_paths.items():
        try:
            img = Image.open(path)
            images[key] = ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"[ERREUR] Chargement image {key} : {e}")

# ------------ Lancement ------------ #
charger_images()
intro()
fenetre.mainloop()