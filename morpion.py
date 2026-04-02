import pyxel
from random import randint

class Jeu:
    def __init__(self):
        """Initialisation de l'écran"""
        pyxel.init(128, 128, title = "Morpion", fps = 120, quit_key = pyxel.KEY_ESCAPE)
        #Affichage de la souris
        pyxel.mouse(visible = True)
        #Importation des médias
        pyxel.load("res.pyxres")
        #Initialisation des plans
        self.num_plan = 0
        # Gestion des pièces
        self.position_piece = []
        self.case_occupe = {i:None for i in range(1,10)}
        #Gestion des tours
        self.num_joueur = 0
        #Gestion musique 
        self.son_coupe = False
        #Gestion du chargement 
        self.decompte_chargement = 100
        # Gestion des de l'interface manche
        self.decompte_manche = 150
        # Gestion des de l'interface de victoire
        self.decompte_victoire = 130
        self.decompte_victoire_anime1 = 100
        self.decompte_victoire_anime2 = 90
        self.flag_can_touch = True
        self.flash = (False, None)
        #Liste des conseilles troll
        self.liste_conseil = ["Pour gagner essayez d'aligner\n3 memes jetons !", "N'oubliez pas, les Bretons\nsont les meilleurs", "Les perdants aux Morpions\nsont des Pov Con", "Essayez de cracher sur\nvotre adversaire pour\nle deconcentrer", "Si votre adversaire met\ntrop de temps a jouer, ce jeu\nvous autorise a bruler sa maison", "Il faut cliquer sur les cases\npour placer un symbole\n(c'est logique en meme temps)","Ce jeu ne fait evidement\npas allusion aux pou du\npubis..."]
        self.num_conseil = randint(0,6)
        
        # Gestion du Jeu
        self.point_j1 = 0
        self.point_j2 = 0
        # Gestion des manches
        self.num_manche = 1
        
        #Démarrage du Jeu
        pyxel.run(self.update, self.draw)
        
    def changement_plan(self):
        
        if self.num_plan == 0 and 30 <= pyxel.mouse_x <= 94 and 61 <= pyxel.mouse_y <= 93 and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            pyxel.play(3, 5)
            self.num_plan = 4
            self.num_conseil = randint(0,6)
        
        elif self.num_plan in (0,3) and 0 <= pyxel.mouse_x <= 16 and 112 <= pyxel.mouse_y <= 128 and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            pyxel.play(3, 5)
            self.num_plan = 2
            
        elif self.num_plan in (1,2,3) and 35 <= pyxel.mouse_x <= 52 and 13 <= pyxel.mouse_y <= 24 and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            pyxel.play(3, 8)
            self.num_plan = 0
            self.position_piece = []
            self.case_occupe = {i:None for i in range(1,10)}
            self.decompte_chargement = 100
            self.decompte_manche = 150
            self.decompte_victoire = 130
            self.num_manche = 1
            self.point_j1 = 0
            self.point_j2 = 0
            
        elif self.num_plan in (0,2) and 112 <= pyxel.mouse_x <= 128 and 112 <= pyxel.mouse_y <= 128 and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            pyxel.play(3, 5)
            self.num_plan = 3
            
        elif self.num_plan == 4:
            self.decompte_chargement -= 1
            if self.decompte_chargement <= 1:
                self.num_plan = 5
                
        elif self.num_plan in (5, 8):
            self.decompte_manche -= 1
            if self.decompte_manche <= 0:
                self.num_plan = 1
                
        elif self.num_plan in (6, 7):
            self.decompte_victoire -= 1
            if self.decompte_victoire <= 1:
                self.num_plan = 0
            
    def condition_de_victoire(self):
        fin_manche = False
        combinaisons = [
            (1,2,3), (4,5,6), (7,8,9),
            (1,4,7), (2,5,8), (3,6,9),
            (1,5,9), (3,5,7)
        ]

        for joueur in range(2):
            for combo in combinaisons:
                if all(self.case_occupe[pos] == joueur for pos in combo):
                    # Début de l'animation de victoire
                    if self.flag_can_touch:
                        self.flag_can_touch = False
                        if joueur == 0:
                            self.point_j1 += 1
                        else:
                            self.point_j2 += 1
                        pyxel.play(3, 9)
                        self.flash = (True, joueur)
    
                    # Animation compteur
                    self.decompte_victoire_anime1 -= 1
                    if self.decompte_victoire_anime1 <= 0:
                        self.decompte_victoire_anime2 -= 1
                        if self.decompte_victoire_anime2 <= 0:
                            # Réinitialisation pour la prochaine manche
                            fin_manche = True
                    break  # sortie dès qu'une victoire détectée
    
        if fin_manche:
            self.reset_manche()
            self.num_plan = 5 if max(self.point_j1, self.point_j2) < 3 else 6 if self.point_j1 > self.point_j2 else 7
    
        # Egalité
        if all(self.case_occupe[i] is not None for i in range(1,10)) and self.flag_can_touch:
            self.num_plan = 8
            self.reset_manche()

    def reset_manche(self):
        self.position_piece = []
        self.case_occupe = {i:None for i in range(1,10)}
        self.decompte_manche = 150
        self.num_manche += 1
        self.decompte_chargement = 100
        self.decompte_victoire = 130
        self.decompte_victoire_anime1 = 100
        self.decompte_victoire_anime2 = 90
        self.flag_can_touch = True
        self.flash = (False, None)

            
    def musique(self):
        # Vérifie que tous les canaux sont libres
        rien_ne_joue = all(pyxel.play_pos(i) is None for i in (0,1,2))
    
        if self.num_plan in (0, 1, 2, 3, 4, 5) and rien_ne_joue and not self.son_coupe:
            pyxel.playm(0)
            
        elif self.num_plan == 2 and 35 <= pyxel.mouse_x <= 51 and 30 <= pyxel.mouse_y <= 46 and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            pyxel.play(3, 5)
            self.son_coupe = not self.son_coupe
            
        elif self.num_plan in (6, 7) and pyxel.play_pos(3) == None:
            pyxel.play(3, 4)
    
    def placement_pieces(self):
        """Gestion du placement des pièces"""
        dico_placement = {
            1: [((30,46),(40,56)), (30,40)],
            2: [((54,70),(40,56)), (54,40)],
            3: [((78,94),(40,56)), (78,40)],
            4: [((30,46),(64,80)), (30,64)],
            5: [((54,70),(64,80)), (54,64)],
            6: [((78,94),(64,80)), (78,64)],
            7: [((30,46),(88,104)), (30,88)],
            8: [((54,70),(88,104)), (54,88)],
            9: [((78,94),(88,104)), (78,88)]
            }
        for i in range(1,10):
            if dico_placement[i][0][0][0] <= pyxel.mouse_x <= dico_placement[i][0][0][1] and dico_placement[i][0][1][0] <= pyxel.mouse_y <= dico_placement[i][0][1][1] and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and self.case_occupe[i] == None and self.flag_can_touch:
                pyxel.play(3, 2)
                self.position_piece.append((dico_placement[i][1],self.num_joueur))
                self.case_occupe[i] = self.num_joueur
                self.num_joueur = (self.num_joueur + 1 ) % 2
                
    def arret_programme(self):
        if self.num_plan == 0 and 120 <= pyxel.mouse_x <= 128 and 0 <= pyxel.mouse_y <= 8 and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            pyxel.play(3, 5)
            pyxel.quit()
    
    def update(self):
        """Mise a jour de l'interface et des interaction utilisateur"""
        self.changement_plan()
        self.musique()
        if self.num_plan == 1:
            self.placement_pieces()
            self.condition_de_victoire()
        self.arret_programme()
            
    
    def draw(self):
        """Mise à jour de l'écran chaque plusieurs fois chaque seconde"""
        pyxel.cls(0)
        pyxel.rect(0,0,128,128,11)
        if self.num_plan == 0:
            pyxel.blt(15, 6, 0, 0, 0, 32, 32, colkey = 0)
            pyxel.blt(55, 15, 0, 64, 0, 16, 16, colkey = 15)
            pyxel.blt(80, 6, 0, 32, 0, 32, 32, colkey = 0) #symbole
            pyxel.blt(30, 60, 0, 0, 32, 64, 32, colkey = 14)  #jouer
            pyxel.blt(0, 112, 1, 48, 0, 16, 16, colkey = 15)  #réglage
            pyxel.blt(112, 112, 1, 48, 16, 16, 16, colkey = 15) #Explication
            pyxel.blt(120, 0, 1, 16, 16, 8, 8, colkey = 15) #Arret
            pyxel.text(19, 115, "Jeu developpe par un\nBreton et un joueur LOL", 0)
            
        elif self.num_plan == 1:
            pyxel.bltm(30, 40, 0, 0, 0, 64, 64, colkey = 15)  #grille
            pyxel.blt(35, 11, 0, 64, 176, 32, 16, colkey = 15) #retour
            for piece in self.position_piece:
                if piece[1] == 0:
                    if self.flash[0] and self.flash[1] == 0:
                        pyxel.blt(piece[0][0], piece[0][1], 1, 0, 32, 16, 16, colkey = 0)
                    else:
                        pyxel.blt(piece[0][0], piece[0][1], 1, 0, 0, 16, 16, colkey = 0)
                elif piece[1] == 1:
                    if self.flash and self.flash[1] == 1:
                        pyxel.blt(piece[0][0], piece[0][1], 1, 16, 32, 16, 16, colkey = 0)
                    else:
                        pyxel.blt(piece[0][0], piece[0][1], 1, 16, 0, 16, 16, colkey = 0)
                        
            pyxel.text(3, 110, f"Score Joueur 1 : {self.point_j1}", 0)
            pyxel.text(3, 120, f"Score Joueur 2 : {self.point_j2}", 0)
            pyxel.text(5, 30, f"Au tour de joueur {self.num_joueur + 1} !", 8)
            
        elif self.num_plan == 2:
            pyxel.blt(15, 6, 0, 0, 0, 32, 32, colkey = 0)
            pyxel.blt(55, 15, 0, 64, 0, 16, 16, colkey = 15)
            pyxel.blt(80, 6, 0, 32, 0, 32, 32, colkey = 0) #symbole
            pyxel.text(19, 115, "Jeu developpe par un\nBreton et un joueur LOL", 0)
            pyxel.blt(30, 10, 0, 64, 64, 64, 112)  # interface
            pyxel.blt(35, 11, 0, 64, 176, 32, 16, colkey = 15)  #retour
            pyxel.blt(0, 112, 1, 48, 0, 16, 16, colkey = 15)  #réglage
            pyxel.blt(112, 112, 1, 48, 16, 16, 16, colkey = 15) #Explication
            pyxel.blt(120, 0, 1, 16, 16, 8, 8, colkey = 15) #Arret
            if self.son_coupe:
                pyxel.blt(35, 30, 1, 32, 16, 16, 16, colkey = 15)
            else:
                pyxel.blt(35, 30, 1, 32, 0, 16, 16, colkey = 15)  #couper son
                
        elif self.num_plan == 3:
            pyxel.blt(15, 6, 0, 0, 0, 32, 32, colkey = 0)
            pyxel.blt(55, 15, 0, 64, 0, 16, 16, colkey = 15)
            pyxel.blt(80, 6, 0, 32, 0, 32, 32, colkey = 0) #symbole
            pyxel.text(19, 115, "Jeu developpe par un\nBreton et un joueur LOL", 0)
            pyxel.blt(30, 10, 0, 128, 64, 64, 112)  # interface
            pyxel.text(33, 31, "Regles du JEU :\n\nCe JEU est un\nmorpion mais\navec une regle\nen plus vous\nne pouvez poser\nque 3 pieces\nmaximum si vous\nposez une piece\nsupplementaire\nla premiere\nplacee\ndisparaitra !", 0)
            pyxel.blt(35, 11, 0, 64, 176, 32, 16, colkey = 15)  #retour
            pyxel.blt(0, 112, 1, 48, 0, 16, 16, colkey = 15)  #réglage
            pyxel.blt(112, 112, 1, 48, 16, 16, 16, colkey = 15) #Explication
            pyxel.blt(120, 0, 1, 16, 16, 8, 8, colkey = 15) #Arret
        
        elif self.num_plan == 4:
            pyxel.bltm(0, 0, 0, 64, 0, 128, 128) 
            pyxel.text(20, 40, "CHARGEMENT...", 0)
            if self.decompte_chargement < 100:
                pyxel.rect(8, 88, 32, 8, 7)
            if self.decompte_chargement < 75:
                pyxel.rect(40, 88, 32, 8, 7)
            if self.decompte_chargement < 50:
                pyxel.rect(72, 88, 32, 8, 7)
            if self.decompte_chargement < 25:
                pyxel.rect(104, 88, 16, 8, 7)
            pyxel.text(3, 105, self.liste_conseil[self.num_conseil], 1)
        
        elif self.num_plan == 5:
            pyxel.bltm(0, 0, 0, 192, 0, 128, 128)
            pyxel.text(50, 60, f"Manche {self.num_manche}", 0)
            
        elif self.num_plan == 6:
            pyxel.bltm(0, 0, 0, 320, 0, 128, 128)
            pyxel.text(27, 60, f"VICTOIRE DE JOUEUR 1", 0)
            
        elif self.num_plan == 7:
            pyxel.bltm(0, 0, 0, 448, 0, 128, 128)
            pyxel.text(27, 60, f"VICTOIRE DE JOUEUR 2", 0)
            
        elif self.num_plan == 8:
            pyxel.bltm(0, 0, 0, 192, 0, 128, 128)
            pyxel.text(50, 60, "EGALITE ...", 0)
            
Jeu()
