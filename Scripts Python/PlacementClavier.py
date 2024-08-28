###### Script pour placer la guitare avant lancement d'une série ############
import serial
import keyboard
import time

# Fonctions pour les mouvements 
def send_gcode(command):
    ser.write((command + '\n').encode())


# Fonctions de commande par clavier
def move_y(direction):
    if direction == 'left':
        send_gcode("G91")  
        send_gcode(f"G01 Y{step}")
        send_gcode("G90")
        time.sleep(0.5)
    elif direction == 'right':
        send_gcode("G91")  
        send_gcode(f"G01 Y{-step}")
        send_gcode("G90")
        time.sleep(0.5)

# Définition des variables
step = 10
printer_port = str(input("Port COM de l'imprimante : ")).strip().upper()
ser = serial.Serial(printer_port, 115200, timeout=1)

########## Fonction appelée dans le script principal ###########

def positionnement() :
    global step
    step = 100
    trigger = True
    while True:
        if keyboard.is_pressed('left'):
            if not trigger :
                trigger = True
                print("Moteurs réactivés")
                step = 1
                time.sleep(2)
            move_y('left')
        elif keyboard.is_pressed('right'):
            if not trigger :
                trigger = True
                print("Moteurs réactivés")
                step = 1
                time.sleep(2)
            move_y('right')
        elif keyboard.is_pressed('space'):
            step = int(input('Nouveau pas de mouvement : '))
        elif keyboard.is_pressed('backspace'):
            print("Moteurs désactivés")
            trigger = False
            send_gcode("M84")
            time.sleep(0.5)



if __name__ == "__main__":
    positionnement()


