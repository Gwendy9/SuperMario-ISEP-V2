
from tkinter import *

sauvegarde = {"etat" : None}

root = Tk() #temporaire
root.title("SuperMario ISEP")
root.configure(bg="black")

# cadrer les boutons
cadrer_boutons = Frame(root, bg="black")
cadrer_boutons.place(relx=0.5, rely=0.5, anchor="center")

#bouton commencer
bouton_commencer = Button(cadrer_boutons, text="Commencer", font=("Poppins", 14))
bouton_commencer.pack(pady=10)

#boutons recommencer et reprendre
if sauvegarde["etat"]!=None:
    bouton_reprendre = Button(cadrer_boutons, text="Reprendre", font=("Poppins", 14))
    bouton_reprendre.pack(pady=10)




root.mainloop()