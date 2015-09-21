
#include <Cmd.h>

//Generates pulse train of specified pulse number, frequency, and duty cycle
//Pin 7 output 
int analogPinBrightness = 3;   // potentiometer connected to analog pin 3
int analogPinOnOff = 5;   // potentiometer connected to analog pin 3
int bright = -1;         // variable to store the read value
int onoff = 1;
char str[80];

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

  if (bright > -1) {
     runmain();
  }
  //check();
}

void runmain() {

  analogWrite(analogPinBrightness, bright);
  analogWrite(analogPinOnOff, LOW);          // set outPin pin as output

  if (onoff==0) 
  {
        analogWrite(analogPinOnOff, HIGH);       // set Pin high

  }
  else if (onoff==1)
  {
        analogWrite(analogPinOnOff, LOW);       // set Pin high
  }

}  

void arg_display(int arg_cnt, char **args)
{
  Serial.println(arg_cnt);
  if (arg_cnt==3) {
     bright = cmdStr2Num(args[1], 10);
     onoff = cmdStr2Num(args[2], 10);
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
