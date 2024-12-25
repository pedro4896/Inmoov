import cvzone
import cv2
import serial
from cvzone.HandTrackingModule import HandDetector

# Configuração do detector de mãos
detector = HandDetector(maxHands=1, detectionCon=0.7)

# Iniciar comunicação serial com Arduino (COM#)
mySerial = serial.Serial("COM4", 9600)  # Usando pyserial para comunicação serial

# Iniciar captura de vídeo
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erro: Não foi possível acessar a câmera.")
    exit()

# Definir o tamanho da janela (largura, altura)
window_width = 1280
window_height = 720

# Criar uma janela com o nome especificado
cv2.namedWindow("Image", cv2.WINDOW_NORMAL)

# Redimensionar a janela para o tamanho desejado
cv2.resizeWindow("Image", window_width, window_height)

while True:
    success, img = cap.read()

    if not success:
        print("Erro: Não foi possível capturar o frame da câmera.")
        break

    # Detectar mãos
    hands, img = detector.findHands(img, draw=True)  # Detecta mãos e desenha a detecção

    if hands:
        # Acessa a primeira mão detectada
        hand = hands[0]
        lmList = hand['lmList']  # Lista de marcos da mão (landmarks)
        bbox = hand['bbox']  # Caixa delimitadora

        # Verificar os dedos levantados, passando a mão detectada como argumento
        fingers = detector.fingersUp(hand)  # Passa a mão detectada
        print(fingers)

        # Enviar os dados de 'fingers' para o Arduino (convertido para string)
        # Converter a lista fingers para o formato "$00000"
        fingers_str = "$" + "".join(map(str, fingers))  # Exemplo: [1, 0, 1, 0, 1] -> "$10101"
        mySerial.write(fingers_str.encode())

        if mySerial.in_waiting > 0:  # Verifique se há dados disponíveis para leitura
            data = mySerial.readline().decode('utf-8').strip()  # Leia uma linha de dados
            print(f"Recebido: {data}")  # Exibe os dados recebidos

    # Mostrar o vídeo com as mãos detectadas
    cv2.imshow("Image", img)

    # Pressione 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
