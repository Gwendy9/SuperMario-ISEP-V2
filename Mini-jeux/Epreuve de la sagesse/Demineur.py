from tkinter import *
from random import *
from tkinter import messagebox
import json


root = Tk() #temporaire
root.attributes('-fullscreen', True)

#canvas du démineur

canvas = Canvas(root, width=500, height=500)
canvas.pack(expand=True)

#sauvegarde

Sauvegarde = { "etat" : None, "score" : 0, "Coordonnes_bombes" : [], "rectangles_marron" : []}

def sauvegarde():
    with open("Sauvegarde.json", "w") as fichier:
        json.dump(Sauvegarde, fichier, indent=4)

def chargement():
    try:
        with open("Sauvegarde.json", 'r') as fichier:
            Sauvegarde = json.load(fichier)
    except FileNotFoundError:
        return []


# placer les bombes

C = [[50 * i, 50 * j, 50 + 50 * i, 50 + 50 * j] for j in range(10) for i in range(10)] #coordonnées de toutes les cases

if Sauvegarde["Coordonnes_bombes"]==[] :
    for n in range(10):
        a = choice(C)
        Sauvegarde["Coordonnes_bombes"].append(a)
        C.remove(a)


# dessiner le terrain

def dessiner_terrain():
    for i in range(10):
        for j in range(10):
            carre_id = canvas.create_rectangle(50 * i, 50 * j, 50 + 50 * i, 50 + 50 * j, width=2, fill="green")
        canvas.tag_bind(carre_id, "<Button-1>", carre)


# événements

dernierX, dernierY = 0, 0
Sauvegarde["etat"] = "en cours"


def enregistrer_position(event):
    global dernierX, dernierY
    dernierX = event.x
    dernierY = event.y
    return dernierX, dernierY


def quand_clique(event):
    enregistrer_position(event)
    if Sauvegarde["etat"] == "gagné" or Sauvegarde["etat"] == "perdu" :
        root.destroy()
    else :
        carre(event)

def carre(event):
    nbr_bombes = 0
    for i in Sauvegarde["Coordonnes_bombes"]:
        if i[0] <= dernierX <= i[2] and i[1] <= dernierY<= i[3]:
            canvas.create_rectangle(i, width=2, fill="red")
            Sauvegarde["etat"] = "perdu"
            message = f"GAME OVER ! Votre score est de: {Sauvegarde['score']}"
            messagebox.showinfo("Résultat", message)
            return
    for j in C: #on parcourt toutes les cases de la matrices
        if j[0] <= dernierX <= j[2] and j[1] <= dernierY <= j[3]:
            for n in Sauvegarde["Coordonnes_bombes"]:
                if j[0] - 50 <= n[0] <= j[2] + 50 and j[0] - 50 <= n[2] <= j[2] + 50 and j[1] - 50 <= n[1] <= j[
                    3] + 50 and j[1] - 50 <= n[3] <= j[3] + 50:
                    nbr_bombes = nbr_bombes + 1
            canvas.create_rectangle(j, width=2, fill="saddlebrown")
            Sauvegarde["rectangles_marron"].append(j)
            canvas.create_text(j[0] + 25, j[1] + 25, text=nbr_bombes, fill="black", font='poppins')
            if Sauvegarde["score"] == 89:
                Sauvegarde["Etat"] = "gagné"
                message = "Félicitations, vous avez trouvé tous les carrés non minés !"
                messagebox.showinfo("résultat", message)
            else:
                Sauvegarde["score"] += 1
                C.remove(j)
                return Sauvegarde["score"]

bouton_sauvegarde = Button(root, text="💾 Sauvegarder", font=("Arial", 14), command=sauvegarde)
bouton_sauvegarde.pack(pady=10)

bouton_chargement = Button(root, text="🔄 Chargement (dernière sauvegarde)", font=("Arial", 14), command=chargement)
bouton_chargement.pack(pady=10)

canvas.bind("<Button-1>", quand_clique)

dessiner_terrain()

root.mainloop()

