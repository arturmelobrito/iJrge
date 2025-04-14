#include <WiFi.h>
#include <ESP32Servo.h>

const char *ssid = "TorresDeSimoneMESH";
const char *password = "Brasil01";

WiFiServer server(80);
String header;

String statePin16 = "off";
String statePin17 = "off";
const int ledPin16 = 16;
const int ledPin17 = 17;

unsigned long currentTime = millis();
unsigned long previousTime = 0;
const long timeoutTime = 2000;

const int servoPin = 13;
Servo mainServo;
String valueString = String(5);
int pos1 = 0;
int pos2 = 0;

const char htmlTemplate[] PROGMEM = R"rawliteral(
<!DOCTYPE html><html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,">
  <style>
    html { font-family: monospace; display: inline-block; margin: 0px auto; text-align: center;}
    .button { background-color: yellowgreen; border: none; color: white; padding: 16px 40px;
              text-decoration: none; font-size: 32px; margin: 2px; cursor: pointer; }
    .button2 { background-color: gray; }
    .slider { width: 300px; }
  </style>
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
</head>
<body>
  <h1>ESP32 Web Server</h1>
  <p>Control LED State</p>
  <p><a href="/16/%STATE_16_LINK%"><button class="button %STATE_16_STYLE%">%STATE_16_TEXT%</button></a></p>
  <p><a href="/17/%STATE_17_LINK%"><button class="button %STATE_17_STYLE%">%STATE_17_TEXT%</button></a></p>
  <p>Position: <span id="servoPos"></span></p>
  <input type="range" min="0" max="180" class="slider" id="servoSlider" onchange="servo(this.value)" value="%VALUE%">
  <script>
    var slider = document.getElementById("servoSlider");
    var servoP = document.getElementById("servoPos");
    servoP.innerHTML = slider.value;
    slider.oninput = function() {
      slider.value = this.value;
      servoP.innerHTML = this.value;
    };
    $.ajaxSetup({timeout:1000});
    function servo(pos) {
      $.get("/?value=" + pos + "&");
    }
  </script>
</body>
</html>
)rawliteral";

void setup() {
  Serial.begin(115200);

  pinMode(ledPin16, OUTPUT);
  digitalWrite(ledPin16, LOW);
  pinMode(ledPin17, OUTPUT);
  digitalWrite(ledPin17, LOW);
  mainServo.attach(servoPin);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }

  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  server.begin();
}

void loop() {
  WiFiClient client = server.available();

  if (client) {
    currentTime = millis();
    previousTime = currentTime;
    Serial.println("New Client.");
    String currentLine = "";

    while (client.connected() && currentTime - previousTime <= timeoutTime) {
      currentTime = millis();
      if (client.available()) {
        char c = client.read();
        Serial.write(c);
        header += c;
        if (c == '\n') {
          if (currentLine.length() == 0) {
            client.println("HTTP/1.1 200 OK");
            client.println("Content-type:text/html");
            client.println("Connection: close");
            client.println();

            if (header.indexOf("GET /16/on") >= 0) {
              statePin16 = "on";
              digitalWrite(ledPin16, HIGH);
            } else if (header.indexOf("GET /16/off") >= 0) {
              statePin16 = "off";
              digitalWrite(ledPin16, LOW);
            }

            if (header.indexOf("GET /17/on") >= 0) {
              statePin17 = "on";
              digitalWrite(ledPin17, HIGH);
            } else if (header.indexOf("GET /17/off") >= 0) {
              statePin17 = "off";
              digitalWrite(ledPin17, LOW);
            }

            if(header.indexOf("GET /?value=")>=0) {
              pos1 = header.indexOf('=');
              pos2 = header.indexOf('&');
              valueString = header.substring(pos1+1, pos2);
              
              //Rotate the servo
              mainServo.write(valueString.toInt());
              Serial.println(valueString); 
            }

            String html = htmlTemplate;

            // Substituições para pin 16
            html.replace("%STATE_16_LINK%", statePin16 == "off" ? "on" : "off");
            html.replace("%STATE_16_TEXT%", statePin16 == "off" ? "ON" : "OFF");
            html.replace("%STATE_16_STYLE%", statePin16 == "off" ? "" : "button2");

            // Substituições para pin 17
            html.replace("%STATE_17_LINK%", statePin17 == "off" ? "on" : "off");
            html.replace("%STATE_17_TEXT%", statePin17 == "off" ? "ON" : "OFF");
            html.replace("%STATE_17_STYLE%", statePin17 == "off" ? "" : "button2");
            html.replace("%VALUE%", valueString);

            client.print(html);
            client.println();
            break;
          } else {
            currentLine = "";
          }
        } else if (c != '\r') {
          currentLine += c;
        }
      }
    }
    header = "";
    client.stop();
    Serial.println("Client disconnected.");
    Serial.println("");
  }
}
