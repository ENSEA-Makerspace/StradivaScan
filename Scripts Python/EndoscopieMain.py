##################### Script principal ###################
import serial
import time
from PlacementClavier import positionnement, ser
from Mouvement import send_gcode_command, endoscopie, stop_command, stop_sending_commands

###################### Au lancement du script : ######################

# Homing
input("Appuyez sur entrer pour lancer le homing (vérifiez que rien n'est sur le chemin)")
send_gcode_command("G28 Y")
send_gcode_command("G28 X")
send_gcode_command("G01 X50 F5000")

while True :
    # Positionnement de l'imprimante "avec le clavier"
    try :
        print("-----------Positionnement--------------")
        print("Flèches dirrectionnelles : Bouger le chariot")
        print("Espace : changer de pas (en mm, 100 par défaut)")
        print("ctrl+c : finir le positionnement")
        print("retour arrière (backspace) : désactiver les moteurs (pour bouger manuellement, les flèches les réactive automatiquement")
        positionnement()
    except KeyboardInterrupt :
        print("Positionnement fini.")
        
    # Endoscopie
    try :
        print("----------Début des série de photos, choisir les paramètres : ----------- ")
        print("ctrl+c : arret de la série en cours ert retour au positionnement")
        endoscopie()
    except KeyboardInterrupt :
        stop_command()
        print("Retour au positionnement")
    stop_sending_commands = False

        

