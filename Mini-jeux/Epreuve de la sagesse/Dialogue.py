#rajouter un "clique pour passer à la suite" en bas)

from tkinter import *

root = Tk() #temporaire
root.attributes('-fullscreen', True)

canvas2 = Canvas(root, width=1000,height=200, bg="gray")
canvas2.pack()

textes = [
    "Bien le bonjour Mario, haha",
    "Tu es venu chercher la triforce de la sagesse, n'est-ce pas ?",
    "Tu ne l'auras pas si facilement"
]

dialogue = canvas2.create_text(500, 100, text=textes[0], font=("Poppins", 15), width=900)

def clic_canvas2(event):
        for texte in textes :
            canvas2.itemconfig(dialogue, text=texte)
            textes.remove(texte)

canvas2.bind("<Button-1>", clic_canvas2)

root.mainloop()