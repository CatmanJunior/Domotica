#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>

#include <Adafruit_NeoPixel.h>
#include <ArduinoOTA.h>
const char* ssid = "Ziggo78F5D45";
const char* password = "Sx7phx8fnkeP";

ESP8266WebServer server(80);

const byte relais = 5;
const byte led = 4;
const byte ledp = 12;
const byte sensorp = A0;

Adafruit_NeoPixel leda = Adafruit_NeoPixel(1, led, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel ledb = Adafruit_NeoPixel(1, ledp, NEO_GRB + NEO_KHZ800);

bool state = 0;

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

  leda.setPixelColor(0, leda.Color(5, 0, 0)); // Moderately bright green color.

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
  ledb.begin(); // This initializes the NeoPixel library.
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
    state = true;
  });

  server.on("/off", []() {
    server.send(200, "text/plain", "on");
    digitalWrite(relais, 0);
    state = false;
  });


  server.on("/who", []() {
    server.send(200, "text/plain", "plant");
  });

  
  server.on("/state", []() {
    if (state == true) server.send(200, "text/plain", "true");
    if (state == false) server.send(200, "text/plain", "false");
  });

  server.onNotFound(handleNotFound);

  server.begin();
  Serial.println("HTTP server started");
}

void loop(void) {
  server.handleClient();
  ArduinoOTA.handle();

  int  sensorValue = analogRead(sensorp);
  Serial.println(sensorValue);
  if (sensorValue < 30) ledb.setPixelColor(0, leda.Color(255,0,0)); // Moderately bright green color.
else   if (sensorValue < 50) ledb.setPixelColor(0, leda.Color(170,0,100)); // Moderately bright green color.
else   if (sensorValue <100) ledb.setPixelColor(0, leda.Color(0,0,255)); // Moderately bright green color.



  ledb.show(); // This sends the updated pixel color to the hardware.

  delay(5);
}
