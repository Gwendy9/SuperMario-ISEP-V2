#bouton quitter


from tkinter import *

sauvegarde = {"etat" : None}

root = Tk() #temporaire

#créer une grille pour placer les boutons et l'image de Mario

root.title("SuperMario ISEP")
bouton_commencer = Button(root, text="Commencer", font=("Poppins", 14))
bouton_commencer.pack(pady=10)

if sauvegarde["etat"]!=None:
    bouton_recommencer = Button(root, text="Recommencer", font=("Poppins", 14))
    bouton_recommencer.pack(pady=10)
#demander confrirmer


root.mainloop()