# Controle de Braço Robótico com Detecção de Mãos

Este projeto consiste no desenvolvimento de um braço robótico controlado em tempo real por meio da detecção de movimentos da mão do usuário. Ele é baseado no robô humanoide **InMoov** e combina programação em Python e Arduino para integrar a captura de movimentos com o controle dos motores que movimentam o braço.

---

## 1. Hardware Utilizado
- **Braço robótico** baseado no design do InMoov.
- **Arduino** para controle dos motores servo que movimentam os dedos do braço.
- **Módulos servo** para controlar os dedos individualmente.
- **Câmera** para capturar os movimentos da mão.

---

## 2. Funcionamento do Sistema
O sistema é dividido em duas partes principais: **processamento de imagem** no computador e **controle dos motores** no Arduino.

### **Parte 1: Detecção de Movimentos com Python**
- A biblioteca **cvzone** e seu módulo **HandDetector** são usados para detectar a mão do usuário a partir da imagem capturada pela câmera.
- A posição dos dedos é analisada e convertida em um formato binário. Cada dedo é representado por um valor:  
  - **1**: Dedo levantado.  
  - **0**: Dedo abaixado.  
- Os dados são enviados para o Arduino via comunicação serial no formato `"$XXXXX"`, onde cada **X** corresponde ao estado de um dedo (polegar, indicador, médio, anelar, mínimo).

### **Parte 2: Controle do Braço Robótico com Arduino**
- No Arduino, os valores recebidos controlam diretamente os motores servo. Cada motor é responsável por um dedo do braço robótico.
- Quando o valor recebido para um dedo é **1**, o motor correspondente posiciona o dedo na posição "levantada". Para o valor **0**, o dedo é abaixado.
- Essa lógica replica os movimentos da mão do usuário no braço robótico.

---

## 3. Código Python
O código Python utiliza uma câmera para capturar a mão do usuário e processa os dados em tempo real:
- Detecta os dedos levantados com o auxílio da biblioteca **cvzone**.
- Converte os dados para o formato apropriado e os envia ao Arduino via **serial**.
- Mostra os dados recebidos de volta do Arduino para verificação.

---

## 4. Código Arduino
O código Arduino é responsável por:
- Interpretar os comandos recebidos do Python via comunicação serial.
- Controlar os motores servo para movimentar os dedos do braço robótico.
- Inicializar cada motor servo e configurar as posições iniciais dos dedos.

---

## 5. Integração e Operação
1. O usuário posiciona a mão em frente à câmera.
2. O Python detecta os dedos levantados, converte as informações e as envia para o Arduino.
3. O Arduino processa os dados e movimenta os dedos do braço robótico, reproduzindo fielmente os movimentos da mão.

---

## Conclusão
Este projeto demonstra como a integração entre visão computacional e hardware pode ser usada para criar sistemas interativos. Ele destaca a eficiência do uso de Python para processamento de imagem e do Arduino para controle de motores, proporcionando uma solução criativa para o controle em tempo real de dispositivos robóticos.
