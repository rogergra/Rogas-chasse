# Projet de Déconnexion et Blocage de Cibles sur Réseau

## Description
Cet outil permet de déconnecter des cibles spécifiques sur un réseau en utilisant une attaque ARP Spoofing. Une fois déconnectées, les cibles sont ajoutées à une liste noire pour empêcher leur reconnexion pendant une période définie (30 minutes à 2 heures).

## Installation
1. Clonez ce repository.
2. Installez les outils nécessaires (`arpspoof` et autres dépendances).
3. Exécutez les scripts depuis le dossier `/scripts`.

## Utilisation

### `deauth.py`
Ce script déconnecte les cibles spécifiées en utilisant ARP Spoofing. Vous devez spécifier les adresses IP cibles et l'adresse IP de la passerelle.

### `block_reconnect.py`
Ce script bloque la reconnexion des adresses MAC déconnectées pendant un temps défini (30 minutes).

### `attack_log.txt`
Un fichier de log qui enregistre chaque attaque effectuée.

## Avertissement
Ce projet est destiné uniquement à des fins d'apprentissage et ne doit pas être utilisé pour des activités malveillantes.
