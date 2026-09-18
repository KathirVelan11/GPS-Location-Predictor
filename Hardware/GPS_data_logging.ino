#include <SPI.h>
#include <SD.h>
#include <SoftwareSerial.h>

File dataFile;
const int chipSelect = 10;
SoftwareSerial gpsSerial(0, 1);
float latitude;
String latitudeDirection;
float longitude;
String longitudeDirection;
String filename = "data.csv";

int istHour;
int istMinute;
int istSecond;
int day;
int month;
int year;

void setup() {
  Serial.begin(9600);
  gpsSerial.begin(9600);
  while (!Serial) {
    ;
  }

  if (!SD.begin(chipSelect)) {
    Serial.println("Error initializing SD card.");
    return;
  }
  Serial.println("SD card initialized.");
}

void loop() {
  if (gpsSerial.available()) {
    String data = gpsSerial.readStringUntil('\n');
    if (data.startsWith("$GNGGA")) 
    {
      processGNGGA(data);
      //Serial.println("GPS DATA WRITTEN");
    } else if (data.startsWith("$GNZDA")) {
      processGNZDA(data);
    }
  }
}

void processGNGGA(String data) {
  int index = 0;
  String values[15];
  while (data.length() > 0) {
    int pos = data.indexOf(',');
    if (pos == -1) {
      values[index] = data;
      break;
    }
    values[index] = data.substring(0, pos);
    data = data.substring(pos + 1);
    index++;
  }

  if (values[2] != "" && values[4] != "") {
    float latitudeDegrees = values[2].substring(0, 2).toFloat();
    float latitudeMinutes = values[2].substring(2).toFloat();
    float longitudeDegrees = values[4].substring(0, 3).toFloat();
    float longitudeMinutes = values[4].substring(3).toFloat();

    latitude = latitudeDegrees + latitudeMinutes / 60.0;
    longitude = longitudeDegrees + longitudeMinutes / 60.0;
    latitudeDirection = values[3];
    longitudeDirection = values[5];
    //if(latitude = 0)
    //{
    //  Serial.println("GPS DATA WRITTEN");
    //}
    printToExcel();
  }
}

void processGNZDA(String data) {
  int hour = data.substring(7, 9).toInt();
  int minute = data.substring(9, 11).toInt();
  int second = data.substring(11, 13).toInt();
  day = data.substring(18, 20).toInt();
  month = data.substring(21, 23).toInt();
  year = data.substring(24, 28).toInt();

  hour += 5;
  minute += 30;

  if (minute >= 60) {
    hour += 1;
    minute -= 60;
  }

  if (hour >= 24) {
    hour -= 24;

    day += 1;
  }

  int daysInMonth[] = { 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 };
  bool isLeapYear = ((year % 4 == 0 && year % 100 != 0) || (year % 400 == 0));

  if (isLeapYear && month == 2) {
    daysInMonth[1] = 29;
  }

  if (day > daysInMonth[month - 1]) {
    day = 1;
    month += 1;
    if (month > 12) {
      month = 1;
      year += 1;
    }
  }

  istHour = hour;
  istMinute = minute;
  istSecond = second;

  printToExcel();
}

void printToExcel() {
  dataFile = SD.open(filename, FILE_WRITE);
  if (dataFile) {
    dataFile.print(latitude, 7);
    dataFile.print(",");
    dataFile.print(latitudeDirection);
    dataFile.print(",");
    dataFile.print(longitude, 7);
    dataFile.print(",");
    dataFile.print(longitudeDirection);
    dataFile.print(",");
    dataFile.print(day);
    dataFile.print("/");
    dataFile.print(month);
    dataFile.print("/");
    dataFile.print(year);
    dataFile.print(",");
    dataFile.print(istHour);
    dataFile.print(":");
    if (istMinute < 10) dataFile.print("0");
    dataFile.print(istMinute);
    dataFile.print(":");
    if (istSecond < 10) dataFile.print("0");
    dataFile.println(istSecond);
    Serial.println("GPS DATA WRITTEN IN FILE");
    dataFile.close();
  } else {
    Serial.println("Error opening file.");
  }
}
