import tkinter as tk
import random


class JeuPendu:
    def __init__(self, fenetre):
        self.fenetre = fenetre
        self.fenetre.title("Jeu du Pendu")

        self.mots = ["ordinateur", "restaurant", "chocolaterie", "bibliothèque", "formidable", "invisible",
                     "incroyable", "magnifique", "véritable", "important", "tradition", "expression", "présidente",
                     "circulaire", "difficile", "confiance", "réflexion", "impossible", "éducation", "électricité",
                     "réservation", "interdiction", "construction", "gouvernement", "développement", "manifestation",
                     "organisation", "architecture", "technologie", "conversation", "expérience", "inspiration",
                     "transmission", "observation", "information", "application", "fonctionnel", "indépendant",
                     "communication", "révolution", "constitution", "responsable", "vérification", "génération",
                     "récupération", "préparation", "automatique", "particulaire", "circonstance", "intervention",
                     "multiplicité", "exploitation", "accomplissement", "collaboration", "recommandation",
                     "représentation", "considération", "identification", "détermination", "adaptabilité",
                     "respectueuse", "proportionnel", "concentration", "perpétuation", "soumission"]
        self.mot = random.choice(self.mots)
        self.lettres_trouvees = []
        self.essais = 6

        self.canvas = tk.Canvas(self.fenetre, width=300, height=300)
        self.canvas.pack()

        self.canvas.create_line(50, 250, 250, 250)  # base
        self.canvas.create_line(100, 250, 100, 50)  # poteau vertical
        self.canvas.create_line(100, 50, 140, 50)  # barre horizontale
        self.canvas.create_line(140, 50, 140, 70)  # corde

        self.etiquette_mot = tk.Label(self.fenetre, text="", font=("Helvetica", 18))
        self.etiquette_mot.pack(pady=20)

        self.entree = tk.Entry(self.fenetre)
        self.entree.pack()

        self.bouton_verifier = tk.Button(self.fenetre, text="Vérifier", command=self.verifier_lettre)
        self.bouton_verifier.pack(pady=10)

        self.etiquette_resultat = tk.Label(self.fenetre, text="", font=("Helvetica", 16))
        self.etiquette_resultat.pack(pady=10)

        self.afficher_mot()

    def dessiner_pendu(self):
        if self.essais == 5:
            self.canvas.create_oval(120, 50, 160, 90)  # tête
        elif self.essais == 4:
            self.canvas.create_line(140, 90, 140, 150)  # corps
        elif self.essais == 3:
            self.canvas.create_line(140, 110, 110, 130)  # bras gauche
        elif self.essais == 2:
            self.canvas.create_line(140, 110, 170, 130)  # bras droit
        elif self.essais == 1:
            self.canvas.create_line(140, 150, 110, 190)  # jambe gauche
        elif self.essais == 0:
            self.canvas.create_line(140, 150, 170, 190)  # jambe droite

    def verifier_lettre(self):
        lettre = self.entree.get().lower()
        self.entree.delete(0, tk.END)

        if lettre in self.mot and lettre not in self.lettres_trouvees:
            self.lettres_trouvees.append(lettre)
        else:
            self.essais -= 1
            self.dessiner_pendu()

        self.afficher_mot()

        if self.essais == 0:
            self.etiquette_resultat.config(text=f"Perdu ! Le mot était : {self.mot}")
            self.bouton_verifier.config(state=tk.DISABLED)
        elif all(l in self.lettres_trouvees for l in self.mot):
            self.etiquette_resultat.config(text="Félicitations ! Vous avez gagné !")
            self.bouton_verifier.config(state=tk.DISABLED)

    def afficher_mot(self):
        affichage = ''
        for lettre in self.mot:
            if lettre in self.lettres_trouvees:
                affichage += lettre + ' '
            else:
                affichage += '_ '
        self.etiquette_mot.config(text=affichage)


# Lancer le jeu
fenetre = tk.Tk()
jeu = JeuPendu(fenetre)
fenetre.mainloop()