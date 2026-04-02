# 🎮 Morpion — Jeu Pyxel

Un morpion en deux joueurs développé avec [Pyxel](https://github.com/kitao/pyxel), le moteur de jeux rétro en Python. Ce projet inclut une règle maison qui pimente la partie : chaque joueur ne peut avoir que **3 pièces sur le plateau à la fois** — la plus ancienne disparaît automatiquement à la pose de la quatrième !

---

## ✨ Fonctionnalités

- **Mode 2 joueurs** en local (même clavier / souris)
- **Règle des 3 pièces** : si vous posez une 4ème pièce, la première placée est retirée
- **Système de score** sur plusieurs manches — premier à 3 victoires gagne
- **Musique et effets sonores** (avec option de coupure)
- **Animations** : écran de chargement, transition de manches, écran de victoire
- **Conseils trolls** aléatoires au chargement
- **Écran des règles** et **menu des réglages** intégrés

---

## Prérequis

- Python 3.8 ou supérieur
- [Pyxel](https://github.com/kitao/pyxel) `>= 2.0`

```bash
pip install pyxel
```

---

## Lancement

```bash
python morpion.py
```

> Le fichier de ressources `res.pyxres` doit se trouver dans le même dossier que `morpion.py`.

---

## 🗂️ Structure du projet

```
morpion/
├── morpion.py      # Code source principal
├── res.pyxres      # Ressources Pyxel (sprites, sons, tilemap)
├── LICENCE     # Licence
└── README.md
```

---

## Comment jouer

| Action | Contrôle |
|---|---|
| Naviguer dans les menus | Clic gauche |
| Placer une pièce | Clic gauche sur une case |
| Couper / activer la musique | Menu Réglages |
| Quitter | `Échap` ou bouton quitter |

### Règle des 3 pièces

Chaque joueur ne peut avoir que **3 pièces simultanément** sur la grille. Dès qu'il en place une 4ème, sa première pièce posée est automatiquement retirée. Anticipez vos coups !

### Victoire

- Alignez **3 symboles** en ligne, colonne ou diagonale pour remporter une manche.
- Le premier joueur à atteindre **3 manches gagnées** remporte la partie.
- En cas de grille pleine sans vainqueur : **égalité**, la manche est rejouée.

---

## Développeurs

Développé par **LE GULUDEC ARTHUR**.

---

## 📄 Licence

Ce projet est distribué sous licence **MIT**. Voir le fichier [LICENSE](LICENSE) pour plus d'informations.
