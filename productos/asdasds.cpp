#include <Wire.h>
#include <LiquidCrystal_I2C.h>
// Definiciones
#define VENTILADOR 3
#define BOMBA 4
#define BOTON_EMERGENCIA 5
const int sensorHumedadPin = A0;
// Umbrales
const float TEMP_MAX = 30.0;    // 30°C
const float HUM_MIN = 40.0;     // 40%

// Inicialización

LiquidCrystal_I2C lcd(0x27, 16, 2); // Dirección I2C común 0x27 o 0x3F

// Variables
bool emergencia = false;
unsigned long ultimaLectura = 0;

void setup() {
  pinMode(sensorHumedadPin, OUTPUT);
  pinMode(VENTILADOR, OUTPUT);
  pinMode(BOMBA, OUTPUT);
  pinMode(BOTON_EMERGENCIA, INPUT);
  
  digitalWrite(VENTILADOR, HIGH);  // Relés activos en LOW
  digitalWrite(BOMBA, HIGH);
  
  Serial.begin(9600);
  lcd.init();
  lcd.backlight();
  lcd.print("Iniciando...");
  delay(2000);
}

void loop() {
  
  // Parada de emergencia
  if (digitalRead(BOTON_EMERGENCIA) == HIGH) {
    emergencia = !emergencia;
    if (emergencia) {
      apagarTodo();
      lcd.clear();
      lcd.print("!EMERGENCIA!");
      lcd.setCursor(0, 1);
      lcd.print("Sistema detenido");
    }
    delay(500); // Anti-rebote
    while (digitalRead(BOTON_EMERGENCIA) == HIGH); // Espera a soltar botón
  }

  if (!emergencia) {
    // Lectura cada 2 segundos
    if (millis() - ultimaLectura > 2000) {
      float humedad = analogRead(sensorHumedadPin);  
      float temperatura = analogRead(A3);
      
      if (isnan(humedad) || isnan(temperatura)) {
        Serial.println("Error sensor!");
        return;
      }

      // Control automático
      if (temperatura > TEMP_MAX) {
        digitalWrite(VENTILADOR, LOW); // Enciende ventilador
      } else {
        digitalWrite(VENTILADOR, HIGH);
      }

      if (humedad < HUM_MIN) {
        digitalWrite(BOMBA, LOW); // Enciende bomba
        delay(5000); // Riego por 5 segundos
        digitalWrite(BOMBA, HIGH);
      }

      // Mostrar datos
      mostrarDatos(temperatura, humedad);
      ultimaLectura = millis();
    }
  }
}

void apagarTodo() {
  digitalWrite(VENTILADOR, HIGH);
  digitalWrite(BOMBA, HIGH);
}

void mostrarDatos(float temp, float hum) {
  // Monitor Serial
  Serial.print("Temp: ");
  Serial.print(temp);
  Serial.print("°C | Hum: ");
  Serial.print(hum);
  Serial.print("% | Vent: ");
  Serial.print(digitalRead(VENTILADOR) == LOW ? "ON" : "OFF");
  Serial.print(" | Bomba: ");
  Serial.println(digitalRead(BOMBA) == LOW ? "ON" : "OFF");

  // LCD
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("T:");
  lcd.print(temp, 1);
  lcd.print("C H:");
  lcd.print(hum, 0);
  lcd.print("%");

  lcd.setCursor(0, 1);
  lcd.print("V:");
  lcd.print(digitalRead(VENTILADOR) == LOW ? "ON " : "OFF");
  lcd.print(" B:");
  lcd.print(digitalRead(BOMBA) == LOW ? "ON" : "OFF");
}