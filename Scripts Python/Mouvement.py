import serial
import time
from PlacementClavier import ser

# Fonctions pour les mouvements
def send_gcode_command(command):
    global stop_sending_commands
    wait_for_completion()
    if stop_sending_commands :
        return
    ser.write((command + '\n').encode())
    while True:
        response = ser.readline().decode().strip()
        if response == "ok":
            break
        print(response)
    return

#Fonctions pour pouvoir arreter à tout moment

stop_sending_commands = False

def wait_for_completion():
    ser.write(b'M400\n')
    time.sleep(0.1)
    while True:
        response = ser.readline().decode().strip()
        if response == "ok":
            break
    return

def stop_command():
    global stop_sending_commands
    stop_sending_commands = True
    print("Arret d'envoie des commandes")
    
# Fonctions pour l'endoscopie

def photo():
    send_gcode_command("G01 X0 F5000")
    time.sleep(0.2)
    send_gcode_command("G01 X20 F5000")

def avance_Pas(pas,vitesse):
    send_gcode_command("G91")
    send_gcode_command(f"G01 Y-{pas} F{vitesse}")
    send_gcode_command("G90")

def serie_photos(TempsPause, Pas, nbPhotos,vitesse) :
    """ S'arrete <nbPhotoss> fois
        Tout les <Pas> cm
        A <vitesse> mm/min 
        Pendant <TempsPause> secondes
    """
    print("---------Début de la série-------------")
    print("Arrêt d'envoie de g code : ctrl+c")
    for i in range(nbPhotos-1):
        photo()
        time.sleep(TempsPause)
        avance_Pas(Pas,vitesse)
    photo()
    time.sleep(TempsPause)
    send_gcode_command("G91")
    send_gcode_command(f"G01 Y{Pas*(nbPhotos-1)} F{vitesse}")
    send_gcode_command("G90")

params = {} #Variable qui enregistre les précédents paramètres

######## Fonction appelée dans le script principal ##########"
def endoscopie():
    global params
    stop_sending_commands = False
    while True :
        if params :
            rep = input("Voulez vous utilisez les précédents paramètres (o/n)? ").strip().lower()
            if rep == 'n' :
                vitesse = int(input("Vitesse de la translation (mm/min, [1,5000]) : "))
                nbPhotos = int(input('Nombre de photos voulus : '))
                Pas = int(input("Pas d'avance de la guitare (mm) : "))
                TempsPause = float(input("Temps de pause (s) entre chaques photos : "))
            else :
                vitesse = params['vitesse']
                nbPhotos = params['nbPhotos']
                Pas = params['Pas']
                TempsPause = params['TempsPause']
        else :
            vitesse = int(input("Vitesse de la translation (mm/min, [1,5000]) : "))
            nbPhotos = int(input('Nombre de photos voulus : '))
            Pas = int(input("Pas d'avance de la guitare (mm) : "))
            TempsPause = float(input("Temps de pause (s) entre chaques photos (prévoir plus que le temps d'exposition pour le traitement) : "))
        params = {
            'vitesse' : vitesse,
            'nbPhotos' : nbPhotos,
            'Pas' : Pas,
            'TempsPause' : TempsPause,
            }
        serie_photos(TempsPause, Pas, nbPhotos, vitesse)
        wait_for_completion()

if __name__=="__main__":
    endoscopie()
