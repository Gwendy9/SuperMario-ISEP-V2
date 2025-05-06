from tkinter import *

sauvegarde = {"etat": 1}

root = Tk()
root.title("SuperMario ISEP")
root.configure(bg="white")

# Charger les images
image_mario = PhotoImage(file="assets/images/Autres/Mario.png")
image_mario = image_mario.subsample(2, 2)

titre_jeu = PhotoImage(file="assets/images/Autres/OIP.png")
titre_jeu = titre_jeu.subsample(2,2)

# Cadrer les boutons
cadrer_boutons = Frame(root, bg="white")
cadrer_boutons.place(relx=0.5, rely=0.5, anchor="center")

label_titre = Label(cadrer_boutons, image=titre_jeu, bg="white")
label_titre.pack(pady=20)

# Bouton commencer
bouton_commencer = Button(cadrer_boutons, text="Commencer", font=("Poppins", 14))
bouton_commencer.pack(pady=10)

# Bouton reprendre (si sauvegarde existe)
if sauvegarde["etat"] is not None:
    bouton_reprendre = Button(cadrer_boutons, text="Reprendre", font=("Poppins", 14))
    bouton_reprendre.pack(pady=10)

# Image sous les boutons
label_image = Label(cadrer_boutons, image=image_mario, bg="white")
label_image.pack(pady=30)

root.mainloop()
