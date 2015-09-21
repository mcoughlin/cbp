
int inPin1 = A0;   // pushbutton connected to digital pin 7
int val1 = 0;     // variable to store the read value
int inPin2 = A1;   // pushbutton connected to digital pin 7
int val2 = 0;     // variable to store the read value
int val = 0;

void setup()
{
  Serial.begin(9600);
  pinMode(inPin1, INPUT);      // sets the digital pin 7 as input
  pinMode(inPin2, INPUT);      // sets the digital pin 7 as input
}

void loop()
{
  val1 = analogRead(inPin1);   // read the input pin
  val2 = analogRead(inPin2);   // read the input pin
  val = val2 - val1;
  Serial.println(val);

}

