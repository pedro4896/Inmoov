import cvzone
import cv2
import serial
from cvzone.HandTrackingModule import HandDetector
import time

detector = HandDetector(maxHands=1, detectionCon=0.7)
gestos_bloqueados = ["$00100", "$10100"]

try:
    mySerial = serial.Serial("COM4", 9600, timeout=1)
    time.sleep(2)
except serial.SerialException as e:
    print(f"Erro ao abrir a porta serial: {e}")
    exit()

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Erro: Não foi possível acessar a câmera.")
    exit()

# Janela em tela cheia
cv2.namedWindow("Image", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

prev_fingers_str = ""
last_send_time = 0
send_interval = 0.1  # segundos (100 ms)

try:
    while True:
        success, img = cap.read()
        if not success:
            print("Erro ao capturar frame.")
            break

        hands, img = detector.findHands(img, draw=True) #habilita desenho na mão

        if hands:
            hand = hands[0]
            fingers = detector.fingersUp(hand)
            fingers_str = "$" + "".join(map(str, fingers))

            if fingers_str in gestos_bloqueados:
                print(f"Gesto bloqueado detectado: {fingers_str} - envio cancelado.")
            else:
                current_time = time.time()
                if fingers_str != prev_fingers_str and (current_time - last_send_time) > send_interval:
                    try:
                        mySerial.write(fingers_str.encode())
                        prev_fingers_str = fingers_str
                        last_send_time = current_time
                        print(f"Enviado: {fingers_str}")
                    except serial.SerialException as e:
                        print(f"Erro ao enviar dados: {e}")

            # Ler todo buffer disponível para evitar travamento
            while mySerial.in_waiting > 0:
                try:
                    data = mySerial.readline().decode('utf-8').strip()
                    if data:
                        print(f"Recebido: {data}")
                except Exception as e:
                    print(f"Erro ao ler dados: {e}")

        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
    mySerial.close()
    print("Programa finalizado.")
