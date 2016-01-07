#define redPin      9
#define grnPin     10
#define bluPin     11

int r, g, b;

void setup()
{
  pinMode(redPin, OUTPUT);
  pinMode(grnPin, OUTPUT);
  pinMode(bluPin, OUTPUT);
  r = g = b = 0;
  
  Serial.begin(115200);
}

void loop()
{
  if(Serial.available() >= 3)
  {
    r = Serial.read();
    g = Serial.read();
    b = Serial.read();
    Serial.write('1'); // Sync
  }
  analogWrite(redPin, r);
  analogWrite(grnPin, g);
  analogWrite(bluPin, b);
}


