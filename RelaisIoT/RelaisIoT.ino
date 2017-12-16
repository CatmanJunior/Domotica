#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>

#include <ArduinoOTA.h>
const char* ssid = "test";
const char* password = "testtest";

ESP8266WebServer server(80);

const byte relais = 16;
const byte led = 0;


int brightness = 0;    // how bright the LED is
int fadeAmount =50;    // how many points to fade the LED by
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
void connectWifi(){
  WiFi.begin(ssid, password);
  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    digitalWrite(led,0);
    delay(100);
    Serial.print(".");
    digitalWrite(led,1);
    delay(100);
  }
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
  pinMode(led, OUTPUT);
  digitalWrite(relais,0);
  digitalWrite(led, 0);
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
    digitalWrite(led,255);
//    analogWrite(led, 255);

  });

  server.on("/off", []() {
    server.send(200, "text/plain", "on");
    digitalWrite(relais, 0);
//    analogWrite(led, 0);
digitalWrite(led,0);
  });


  server.onNotFound(handleNotFound);

  server.begin();
  Serial.println("HTTP server started");
}

void loop(void) {
  server.handleClient();
  ArduinoOTA.handle();


  delay(5);
}
