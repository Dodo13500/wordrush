# World Rush v0.3

World Rush est un jeu d'association d'idées rapide et compétitif codé en Python. Jouez en local ou en ligne, défiez vos amis et testez votre rapidité !

##  Prérequis Importants

Ce projet nécessite une version ancienne de Python pour fonctionner correctement.

*   **Python 3.13** (Requis)
*   Bibliothèque **pygame**

## Installation

1.  Téléchargez et installez Python 3.13 depuis [python.org](https://www.python.org/).
2.  Ouvrez un terminal (ou invite de commande) et installez la dépendance graphique :
    ```bash
    pip install pygame
    ```

## Comment lancer le jeu

Exécutez simplement le fichier principal :

```bash
python "wordrush.py"
```

## Fonctionnalités

*   **Multijoueur** : Local (même PC) ou En Ligne (TCP/IP).
*   **Réseau** : Système de Lobby, Chat intégré et tentative UPnP automatique pour l'hébergement.
*   **Gameplay** : Chronomètre stressant, validation de mots, et système de contestation.
*   **Personnalisation** : Choix des thèmes, du temps et du score.

## Contrôles

*   **Entrée** : Valider un mot / Envoyer un message.
*   **Maj (Shift)** : Contester une réponse (Configurable).
*   **Espace** : Passer au tour suivant (Mode Vocal).
