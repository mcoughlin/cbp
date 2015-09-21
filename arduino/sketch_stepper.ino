
#include <Cmd.h>

//Generates pulse train of specified pulse number, frequency, and duty cycle
//Pin 7 output 
int outPinMinus1 = 7;
int outPinPlus1 = 6;                 // digital pin 8
int reversePinPlus1 = 4;                 // digital pin 8
int reversePinMinus1 = 5;

int outPinMinus2 = 13;
int outPinPlus2 = 12;                 // digital pin 8
int reversePinPlus2 = 10;                 // digital pin 8
int reversePinMinus2 = 11;

int pulseNumber = 25000;          // Number of pulses in pulse train                 
double frequency = 1000;            //frequency in Hz 
double dutyCycle = 0.5;          //duty cycle 

unsigned long seconds = 0;        //delay between pulse sets                         
double period = (1 / frequency) * 1000000;  
int on = dutyCycle * period;
int off = period * (1-dutyCycle); 

float angle_passed = 0.0;
float angle;

char str[80];

byte byteRead;
double numSteps = 0.0;
int direction = 0;
int motorNum = 0;

#define fastWrite(_pin_, _state_) ( _pin_ < 8 ? (_state_ ?  PORTD |= 1 << _pin_ : PORTD &= ~(1 << _pin_ )) : (_state_ ?  PORTB |= 1 << (_pin_ -8) : PORTB &= ~(1 << (_pin_ -8)  )))
// the macro sets or clears the appropriate bit in port D if the pin is less than 8 or port B if between 8 and 13

void setup()
{
  // init the command line and set it for a speed of 57600
  cmdInit(57600);

  // add the commands to the command table. These functions must
  // already exist in the sketch. See the functions below.
  // The functions need to have the format:
  //
  // void func_name(int arg_cnt, char **args)
  //
  // arg_cnt is the number of arguments typed into the command line
  // args is a list of argument strings that were typed into the command line
  cmdAdd("args", arg_display);
}

void loop()
{
  cmdPoll();

  if (numSteps > 0) {
     runmain();
     numSteps = 0;
     direction = 0;
     motorNum = 0;
  }
  //check();
}

void runmain() {
  angle = numSteps;

  pinMode(outPinPlus1, OUTPUT);          // set outPin pin as output
  pinMode(outPinMinus1, OUTPUT);          // set outPin pin as output
  pinMode(reversePinPlus1, OUTPUT);          // set outPin pin as output
  pinMode(reversePinMinus1, OUTPUT);

  pinMode(outPinPlus2, OUTPUT);          // set outPin pin as output
  pinMode(outPinMinus2, OUTPUT);          // set outPin pin as output
  pinMode(reversePinPlus2, OUTPUT);          // set outPin pin as output
  pinMode(reversePinMinus2, OUTPUT);

  if (direction==1) 
  {
        fastWrite(reversePinPlus1, HIGH);       // set Pin high
        fastWrite(reversePinMinus1, LOW);       // set Pin high
        fastWrite(outPinPlus1, LOW);       // set Pin high
        fastWrite(outPinMinus1, LOW);       // set Pin high

        fastWrite(reversePinPlus2, HIGH);       // set Pin high
        fastWrite(reversePinMinus2, LOW);       // set Pin high
        fastWrite(outPinPlus2, LOW);       // set Pin high 
        fastWrite(outPinMinus2, LOW);       // set Pin high

  }
  else if (direction==2)
  {
        fastWrite(reversePinPlus1, LOW);       // set Pin high
        fastWrite(reversePinMinus1, HIGH);       // set Pin high
        fastWrite(outPinPlus1, LOW);       // set Pin high
        fastWrite(outPinMinus1, LOW);       // set Pin high

        fastWrite(reversePinPlus2, LOW);       // set Pin high
        fastWrite(reversePinMinus2, HIGH);       // set Pin high
        fastWrite(outPinPlus2, LOW);       // set Pin high
        fastWrite(outPinMinus2, LOW);       // set Pin high

  }

  while(angle_passed < angle) {
     if (motorNum==1)
     {
     Pulse1(on, off);       // set Pin high
     }
     else if (motorNum==2)
     {
     Pulse2(on, off);
     }
     angle_passed = angle_passed + 1;
     Serial.println(angle_passed);
  } 
 
}  

void Pulse1(int on, int off) {
  fastWrite(outPinMinus1, HIGH);       // set Pin high
  delayMicroseconds(on);      // waits "on" microseconds
  fastWrite(outPinMinus1, LOW);        // set pin low
  delayMicroseconds(off);      //wait "off" microseconds
}

void Pulse2(int on, int off) {
  fastWrite(outPinMinus2, HIGH);       // set Pin high
  delayMicroseconds(on);      // waits "on" microseconds
  fastWrite(outPinMinus2, LOW);        // set pin low
  delayMicroseconds(off);      //wait "off" microseconds
}

void arg_display(int arg_cnt, char **args)
{
  Serial.println(arg_cnt);
  if (arg_cnt==4) {
     numSteps = cmdStr2Num(args[1], 10);
     //Serial.println(numSteps)
     direction = cmdStr2Num(args[2], 10);
     motorNum = cmdStr2Num(args[3], 10);
  }

  //for (int i=0; i<arg_cnt; i++)
  //{
    //Serial.print("Arg ");
    //Serial.print(i);
    //Serial.print(": ");

    //if (i == 1)
    //{
    //   Serial.println(args[i]);
   // }
    
    //if (i == 2)
   // {
   //    Serial.println(args[i]);
    //}    
    
  //}
}
