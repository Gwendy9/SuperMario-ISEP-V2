from tkinter import *
from random import *
from tkinter import messagebox


root = Tk()
root.attributes('-fullscreen', True)
canvas = Canvas(root, width=500, height=500)
canvas.pack(expand=True)

# placer les bombes

bombes = []
C = [[50 * i, 50 * j, 50 + 50 * i, 50 + 50 * j] for j in range(10) for i in range(10)]
for n in range(10):
    a = choice(C)
    bombes.append(a)
    C.remove(a)


# dessiner le terrain

def dessiner_terrain():
    for i in range(10):
        for j in range(10):
            carre_id = canvas.create_rectangle(50 * i, 50 * j, 50 + 50 * i, 50 + 50 * j, width=2, fill="green")
        canvas.tag_bind(carre_id, "<Button-1>", carre)


# événements

dernierX, dernierY = 0, 0
score = 0
resultat = "en cours"


def enregistrer_position(event):
    global dernierX, dernierY
    dernierX = event.x
    dernierY = event.y
    return dernierX, dernierY


def quand_clique(event):
    enregistrer_position(event)
    if resultat == "perdu" or resultat == "gagné":
        root.destroy()  # fin de la partie
    else:
        carre(event)


def carre(event):
    global score
    global resultat
    nbr_bombes = 0
    for i in bombes:
        if i[0] <= dernierX <= i[2] and i[1] <= dernierY <= i[3]:
            canvas.create_rectangle(i, width=2, fill="red")
            resultat = "perdu"
            message = f"GAME OVER ! Votre score est de: {score}"
            messagebox.showinfo("résultat", message)
            return
    for j in C:
        if j[0] <= dernierX <= j[2] and j[1] <= dernierY <= j[3]:
            for n in bombes:
                if j[0] - 50 <= n[0] <= j[2] + 50 and j[0] - 50 <= n[2] <= j[2] + 50 and j[1] - 50 <= n[1] <= j[
                    3] + 50 and j[1] - 50 <= n[3] <= j[3] + 50:
                    nbr_bombes = nbr_bombes + 1
            canvas.create_rectangle(j, width=2, fill="saddlebrown")
            canvas.create_text(j[0] + 25, j[1] + 25, text=nbr_bombes, fill="black", font=('poppins'))
            if score == 89:
                resultat = "gagné"
                message = "Félicitations, vous avez trouvé tous les carrés non minés !"
                messagebox.showinfo("résultat", message)
            else:
                score = score + 1
                C.remove(j)
                return score


canvas.bind("<Button-1>", quand_clique)
dessiner_terrain()

root.mainloop()
lll