import grille_base as gb
from random import randint
import pygame

#remplacer 3 nombres identiques successives ou plus en lignes et en colonnes par des 0

class GestionGrilles:
    "classe qui prend en paramètre les dimensions de la grille souhaite"

    def __init__(self, n, m):
        self.tab_original = gb.create_alea(n, m, 1, 5)
        self.score_lig = 0
        self.score_col = 0
        self.score = 0

    def remplissage(self, tab):
        "on remplit aleatoirement la grille de 1,2,3,4 qui correspondent aux id des gems"
        for l in range(4):
            for i in range (len(tab)-1, 0, -1):
                for j in range (len(tab[0])-1, -1, -1):
                    if tab[i][j] == 0 :
                        for k in range (i, 0, -1):
                            tab[k][j] = tab[k-1][j]
                            tab[k-1][j] = 0
            print(gb.to_str(tab))
        for i in range (len(tab)):
            for j in range (len(tab[0])):
                if tab[i][j] == 0 :
                    tab[i][j] = randint(1,4)
        print(gb.to_str(tab))
        return tab


    def eliminerLignes(self, tab):
        "fonction qui permet d'eliminer l'endroit d'en la ligne ou il y a 3 meme chiffres a la suite"
        newtab_index = gb.create(len(tab), len(tab[0]), 0)
        for i in range (len(tab)):
            soustab_lig = gb.line(tab, i)
            for j in range (0, len(soustab_lig)-2):
                if (soustab_lig[j]==soustab_lig[j+1]==soustab_lig[j+2]):
                    newtab_index[i][j] = 1
                    newtab_index[i][j+1] = 1
                    newtab_index[i][j+2] = 1
                    if soustab_lig[j]==1:
                        self.score_lig += 10
                    if soustab_lig[j]==2:
                        self.score_lig += 20
                    if soustab_lig[j]==3:
                        self.score_lig += 30
                    if soustab_lig[j]==4:
                        self.score_lig += 40
        for i in range (len(tab)):
            for j in range (len(tab[0])):
                if newtab_index[i][j] == 1:
                    tab[i][j] = 0
        return tab, self.score_lig


    def eliminerColonnes(self, tab):
        "fonction qui permet d'eliminer l'endroit d'en la colonne ou il y a 3 meme chiffre a la suite"
        newtab_index = gb.create(len(tab), len(tab[0]), 0)
        for i in range (len(tab[0])):
            soustab_col = gb.column(tab, i)
            for j in range (0, len(soustab_col)-2):
                if (soustab_col[j]==soustab_col[j+1]==soustab_col[j+2]):
                    newtab_index[i][j] = 1
                    newtab_index[i][j+1] = 1
                    newtab_index[i][j+2] = 1
                    if soustab_col[j]==1:
                        self.score_col += 10
                    if soustab_col[j]==2:
                        self.score_col += 20
                    if soustab_col[j]==3:
                        self.score_col += 30
                    if soustab_col[j]==4:
                        self.score_col += 40
        for i in range (len(tab)):
            for j in range (len(tab[0])):
                if newtab_index[i][j] == 1:
                    tab[j][i] = 0
        return tab, self.score_col


    def eliminerLignesColonnes(self, tab):
        "fonction qui elimine 3 meme chiffre qui sont a la suite"
        ntab1=self.eliminerLignes(tab)[0]
        ntab2=self.eliminerColonnes(tab)[0]
        self.score = self.eliminerLignes(tab)[1] + self.eliminerColonnes(tab)[1]
        for l in range (len(tab)):
             for k in range (len(tab[l])):
                 if ntab1[l][k]==0 or ntab2[l][k]==0:
                    tab[l][k]=0
        print(gb.to_str(tab))
        return tab, self.score
    
    def count_zero(self, tab):
        for i in range (len(tab)):
            for j in range (len(tab[0])):
                if tab[i][j]==0:
                    return True
        return False

    def newtab(self, tab):
        "fonction qui renvoie une nouvelle grille ou on a enlever les match"
        grille = self.eliminerLignesColonnes(tab)[0]
        self.score = self.eliminerLignesColonnes(tab)[1]
        self.remplissage(grille)
        self.eliminerLignesColonnes(grille)
        while self.count_zero(grille):
            self.remplissage(grille)
            self.eliminerLignesColonnes(grille)[0]
        print(gb.to_str(grille))
        return grille, self.score

    
    def recup_case(self, level, x, y):
        "fonction qui permet de recuperer les coordonnes de la case dans la quelle on vient de cliquer"
        if level ==  2 :
            return (((y-150)//50),(x-450)//50)
        else:
            return (((y-250)//50),(x-450)//50)
            
    
    def permut(self, tab, click1, click2):
        "fonction quib permet d'echanger des cases si elles sont a cotes"
        if click1!=click2 :
            if (click1[0] == click2[0] and (click1[1] == click2[1]+1 or click1[1] == click2[1]-1)) or (click1[1] == click2[1] and (click1[0] == click2[0]+1 or click1[0] == click2[0]-1)):
                a = tab[click1[0]][click1[1]]
                tab[click1[0]][click1[1]] = tab[click2[0]][click2[1]]
                tab[click2[0]][click2[1]] = a
                print(gb.to_str(tab))
        return tab

def afficher_temps(font, screen, temps_de_partie, accueil):
    """fonction qui prend en paramètre le style d'ecriture, l'ecran, le temps que doit durer la partie
    et le fond d'ecran.
    Cette fonction permet d'afficher et de calculer le temps restant de la partie """
    screen.blit(accueil, (0,0))
    temps = (temps_de_partie - pygame.time.get_ticks()) // 1000
    affichageTemps = font.render("Temps : ", 1, (10, 10, 10))
    screen.blit(affichageTemps, (1091,120))
        
    temps_surface = font.render(str(temps), 1, (10, 10, 10))
    screen.blit(temps_surface, (1160,120))
    
    return temps
    