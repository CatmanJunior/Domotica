#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>

#include <Adafruit_NeoPixel.h>
#include <ArduinoOTA.h>
const char* ssid = "test";
const char* password = "testtest";

ESP8266WebServer server(80);

const byte relais = 5;
const byte led = 4;
const byte ldrA = 14;
const byte ldrB = 12;
const byte ldrC = 13;
const byte analog = A0;
Adafruit_NeoPixel leda = Adafruit_NeoPixel(1, led, NEO_GRB + NEO_KHZ800);

int state = 0;

int brightness = 0;    // how bright the LED is
int fadeAmount = 50;   // how many points to fade the LED by
const long interval = 1000;

String serialString = "hello from esp8266!\n";

String bl = "\n";

void handleRoot() {

  server.send(200, "text/plain", serialString);


}

void handleNotFound() {

  String message = "File Not Found\n\n";
  message += "URI: ";
  message += server.uri();
  message += "\nMethod: ";
  message += (server.method() == HTTP_GET) ? "GET" : "POST";
  message += "\nArguments: ";
  message += server.args();
  message += "\n";
  for (uint8_t i = 0; i < server.args(); i++) {
    message += " " + server.argName(i) + ": " + server.arg(i) + "\n";
  }
  server.send(404, "text/plain", message);

}
void connectWifi() {
  WiFi.begin(ssid, password);
  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    leda.setPixelColor(0, leda.Color(0, 5, 0)); // Moderately bright green color.

    leda.show(); // This sends the updated pixel color to the hardware.
    delay(100);
    Serial.print(".");

    leda.setPixelColor(0, leda.Color(0, 0, 0)); // Moderately bright green color.

    leda.show(); // This sends the updated pixel color to the hardware.
    delay(100);
  }

  leda.setPixelColor(0, leda.Color(15, 0, 0)); // Moderately bright green color.

  leda.show(); // This sends the updated pixel color to the hardware.

  Serial.println("");
  serialString += bl + "Connected to: " + ssid;
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  String a = WiFi.localIP().toString();
  serialString += bl + a;

  Serial.println(WiFi.localIP());

}

void setup(void) {
  pinMode(relais, OUTPUT);
  leda.begin(); // This initializes the NeoPixel library.
  pinMode(ldrA, OUTPUT);
  pinMode(ldrB, OUTPUT);
  pinMode(ldrC, OUTPUT);
  digitalWrite(A0, INPUT_PULLUP);  // set pullup on analog pin 0
  digitalWrite(relais, 0);
  Serial.begin(115200);
  connectWifi();
  ArduinoOTA.begin();
  Serial.println("");




  if (MDNS.begin("esp8266")) {
    Serial.println("MDNS responder started");
  }

  server.on("/", handleRoot);

  server.on("/inline", []() {
    server.send(200, "text/plain", "this works as well");
  });

  server.on("/on", []() {
    server.send(200, "text/plain", "off");
    digitalWrite(relais, 1);
  });

  server.on("/off", []() {
    server.send(200, "text/plain", "on");
    digitalWrite(relais, 0);
  });


  server.on("/who", []() {
    server.send(200, "text/plain", "ldr");
  });


  server.on("/state", []() {
    server.send(200, "text/plain", String(state));
  });

  server.onNotFound(handleNotFound);

  server.begin();
  Serial.println("HTTP server started");
}

void loop(void) {
  server.handleClient();
  ArduinoOTA.handle();
  int highest = 0;

  digitalWrite(ldrA, HIGH);
  delay(10);
  int  sensorValue = analogRead(analog);
  highest = sensorValue;
  state = 0;
  digitalWrite(ldrA, LOW);
  Serial.print("1:");
  Serial.println(sensorValue);
  digitalWrite(ldrB, HIGH);
  delay(10);
  sensorValue = analogRead(analog);
  if (sensorValue >= highest) {
    highest = sensorValue;
    state = 1;

  }
  digitalWrite(ldrB, LOW);
  Serial.print("2:");
  Serial.println(sensorValue);
  digitalWrite(ldrC, HIGH);
  delay(10);
  sensorValue = analogRead(analog);
  if (sensorValue >= highest)
  { highest = sensorValue;
    state = 2;
  }
  digitalWrite(ldrC, LOW);
  Serial.print("3:");
  Serial.println(sensorValue);

  delay(5);
}
