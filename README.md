
# ROGAS CHASSE

**ROGAS CHASSE** est un script Python permettant de mener une attaque ARP Spoofing sur un réseau local en utilisant des outils comme `arpspoof` et `nmap`. Ce programme est conçu pour détecter automatiquement les cibles et effectuer des attaques sur des appareils connectés à un réseau.

## Fonctionnalités

- Vérification et installation des dépendances manquantes (arpspoof, nmap).
- Détection automatique de la passerelle et des interfaces réseau disponibles.
- Scanner le réseau local pour détecter les appareils connectés.
- Mener une attaque ARP Spoofing sur les cibles spécifiées ou détectées automatiquement.
- Restaurer les connexions des cibles après l'attaque.

## Bibliothèques et Outils Requis

Avant de lancer le script, vous devez installer certaines dépendances :

- **Python 3.x** : Ce script nécessite Python 3.
- **arpspoof** : Utilisé pour effectuer l'attaque ARP Spoofing.
- **nmap** : Utilisé pour scanner le réseau et détecter les appareils connectés.

### Installation des Dépendances

#### Installer Python 3.x

Si Python 3 n'est pas installé, vous pouvez l'installer via les commandes suivantes :

- Sur Ubuntu/Debian :
  ```bash
  sudo apt-get update
  sudo apt-get install python3











######Depandance neccessair 
sudo apt-get install dsniff nmap

###executon du pogramme


python3 rogas_chasse.py