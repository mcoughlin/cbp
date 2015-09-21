#include <Wire.h>
#include <Adafruit_ADS1015.h>
 
Adafruit_ADS1115 ads1115_1(0x48);
Adafruit_ADS1115 ads1115_2(0x49);	// construct an ads1115 at address 0x49
 
int16_t adc01, adc23;

void setup(void)
{
  Serial.begin(9600);
  //Serial.println("Hello!");
  
  //Serial.println("Getting single-ended readings from AIN0..3");
  //Serial.println("ADC Range: +/- 6.144V (1 bit = 3mV)");
  ads1115_1.begin();
  //ads1115_2.begin();
  
  //ads1115.setGain(GAIN_TWOTHIRDS);  // 2/3x gain +/- 6.144V  1 bit = 3mV (default)
  ads1115_1.setGain(GAIN_ONE);     // 1x gain   +/- 4.096V  1 bit = 2mV
  //ads1115_2.setGain(GAIN_ONE);     // 1x gain   +/- 4.096V  1 bit = 2mV 
 
  //adsGain_t gain = ads1115.getGain();
  //Serial.println(gain);
 
  // ads1015.setGain(GAIN_ONE);     // 1x gain   +/- 4.096V  1 bit = 2mV
  // ads1015.setGain(GAIN_TWO);     // 2x gain   +/- 2.048V  1 bit = 1mV
  // ads1015.setGain(GAIN_FOUR);    // 4x gain   +/- 1.024V  1 bit = 0.5mV
  // ads1015.setGain(GAIN_EIGHT);   // 8x gain   +/- 0.512V  1 bit = 0.25mV
  // ads1015.setGain(GAIN_SIXTEEN); // 16x gain  +/- 0.256V  1 bit = 0.125mV

  // Take a measurement but do not print it
  adc01 = ads1115_1.readADC_Differential_0_1();
  adc23 = ads1115_1.readADC_Differential_2_3();
  delay(1000);

}
 
void loop(void)
{
  adc01 = ads1115_1.readADC_Differential_0_1();
  Serial.print(adc01);
  Serial.print(" ");
  adc23 = ads1115_1.readADC_Differential_2_3();
  //adc23 = ads1115_2.readADC_Differential_0_1();
  Serial.println(adc23);
  
  delay(1000);
}
