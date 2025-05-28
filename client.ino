#include <SPI.h>
#include <Ethernet.h>

const int led = 5;
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
char serverName[] = "www.arduino.php5.sk";
IPAddress ip(192, 168, 2, 40);
EthernetClient client;
String readString;
int x = 0;
char lf = 10;

void setup() {
  pinMode(led, OUTPUT);
  if (Ethernet.begin(mac) == 0) {
    Serial.println("DHCP 실패, 정적 IP로 시도 중...");
    Ethernet.begin(mac, ip);
  }
  Serial.begin(9600);
}

void loop() {
  if (client.connect(serverName, 80)) {
    Serial.println("서버에 연결됨");
    client.println("GET /PHP_en/translations.txt HTTP/1.1");
    client.println("Host: www.arduino.php5.sk");
    client.println("Connection: close");
    client.println();
  } else {
    Serial.println("서버 연결 실패");
  }

  while (client.connected() && !client.available()) delay(1);

  while (client.available()) {
    char c = client.read();
    Serial.print(c);
    if (c == lf) x++;
    else if (x == 12) readString += c;
  }

  if (readString == "Turn on") {
    digitalWrite(led, HIGH);
  } else if (readString == "Turn off") {
    digitalWrite(led, LOW);
  } else {
    Serial.println("지원하지 않는 명령: " + readString);
  }

  readString = "";
  x = 0;
  client.stop();
  delay(5000);
}
