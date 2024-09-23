int ledPin = 2;      
int pwmPin = 16;     
int potPin = 34;     

void setup() {
  Serial.begin(115200);          
  pinMode(ledPin, OUTPUT);       
  pinMode(pwmPin, OUTPUT);       
  analogWrite(pwmPin, 0);        
}

void loop() {
  if (Serial.available() > 0) {
    String comando = Serial.readStringUntil('\n');

    if (comando.startsWith("SET_BAUD")) {
      int baudRate = comando.substring(9).toInt();  
      Serial.end();  
      Serial.begin(baudRate);  
      Serial.println("Velocidad establecida a: " + String(baudRate));
      return;  
    }

    if (comando == "LED_ON") {
      digitalWrite(ledPin, HIGH);  
      Serial.println("LED Encendido");
    } 
    else if (comando == "LED_OFF") {
      digitalWrite(ledPin, LOW);   
      Serial.println("LED Apagado");
    } 
    else if (comando.startsWith("TAREA_3,")) {
      int valorPWM = comando.substring(8).toInt();  
      if (valorPWM <= 255 && valorPWM >= 1) {
        analogWrite(pwmPin, valorPWM);  
        Serial.println("Intensidad ajustada a: " + String(valorPWM));
      } else {
        Serial.println("Error: Valor fuera de rango (1-255)");
      }
    } 
    else if (comando.startsWith("TAREA_1")) {
      String numStr = comando.substring(7);  
      int numero = numStr.toInt();  
      if (numStr.length() > 0 || numero == 0) {  
        int resultado = numero + 1;  
        Serial.println(resultado);  
      } else {
        Serial.println("Error: Número inválido");
      }
    }
    else if (comando == "TAREA_2") {
      int valorAnalogico = analogRead(potPin);  
      Serial.println(valorAnalogico);  
    }
  }
}
