
#include <Cmd.h>

int outPin = 10; //output pin
int timeDelay = 0;

void setup(){

  pinMode(outPin,OUTPUT);
  digitalWrite(outPin,LOW);

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

  //Serial.begin(9600);//setup serial communication
  
}

void loop()
{
  cmdPoll();

  if (timeDelay > 0) {

    digitalWrite(outPin,HIGH);
    delay(timeDelay);
    digitalWrite(outPin,LOW);
    timeDelay = 0;
  }
  else if (timeDelay < 0)
  {
    digitalWrite(outPin,HIGH);
  }
}

void arg_display(int arg_cnt, char **args)
{
  //Serial.println(arg_cnt);
  if (arg_cnt==2) {
     timeDelay = cmdStr2Num(args[1], 10);
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
