# Laboratoire 3 - Streaming WebRTC

## Description
Ce projet implémente un service de streaming vidéo en temps réel utilisant WebRTC pour transmettre le flux d'une webcam entre deux ordinateurs.

## Structure
-server.py: Serveur WebRTC qui capture la webcam et transmet le flux
-client.py: Client WebRTC qui reçoit et affiche le flux vidéo
- environmental.yaml: Fichier de configuration de l'environnement conda

## Installation

1. Cloner le dépôt :
  
   git clone https://github.com/serine-4/labo3-webrtc.git
   cd labo3-webrtc

2.Créer l'environnement conda :

conda env create -f environment.yaml
conda activate webrtc

3.Utilisation
3.1.Démarrer le serveur (sur la machine avec webcam) :

python server_main.py

3.2.Démarrer le client (sur la même machine ou une autre) :

python client_main.py
Pour quitter : Appuyer sur 'q' dans la fenêtre vidéo ou Ctrl+C dans le terminal

Auteur: SERINE AIT DJOUDI
