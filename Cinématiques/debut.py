import tkinter as tk

def lancer_cinematique():
    cinematique_fenetre = tk.Toplevel()
    cinematique_fenetre.title("Cinématique")
    cinematique_fenetre.geometry("800x600")

    label = tk.Label(cinematique_fenetre, text="", font=("Arial", 24))
    label.pack(expand=True)

    textes = [
        "Il était une fois, dans un monde lointain...",
        "Un héros se leva contre les ténèbres.",
        "Son voyage allait changer le destin de tous.",
        "Mais ce n'était que le début..."
    ]

    def afficher_texte(index):
        if index < len(textes):
            label.config(text=textes[index])
            # Affiche la phrase suivante après 2 secondes
            cinematique_fenetre.after(2000, afficher_texte, index + 1)
        else:
            cinematique_fenetre.destroy()  # Ferme la fenêtre à la fin

    afficher_texte(0)