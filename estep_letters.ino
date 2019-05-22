#include <AccelStepper.h>
#define HALFSTEP 8

// Define two steppers and the pins they will use
AccelStepper stepL(AccelStepper::DRIVER, 3, 2);
AccelStepper stepR(AccelStepper::DRIVER, 5, 4);

//number of steps per rotation
const int spr = 4096;

//how long each letter is displayed
int letterdelay = 1000;

//an array which determines the letter positions, scaled to number of steps
const int Letters[][3] = 
{{spr/8, 0, 'A'}, {spr/4, 0, 'B'}, {(spr * 3)/8, 0, 'C'}, {spr/2, 0, 'D'}, {0, (spr * 5)/8, 'E'}, {0, (spr * 3)/4, 'F'}, {0, (spr * 7)/8, 'G'}, {spr/4,spr/8, 'H'}, {(spr * 3)/8, spr/8, 'I'}, {spr/2, (spr * 3)/4, 'J'}, //ABCDEFGHIJ 
{spr/8, spr/2, 'K'}, {spr/8, (spr * 5)/8, 'L'}, {spr/8, (spr * 3)/4, 'M'}, {spr/8, (spr * 7)/8, 'N'}, {spr/4, (spr * 3)/8, 'O'}, {spr/4, spr/2, 'P'}, {spr/4, (spr * 5)/8, 'Q'}, {spr/4 , (spr * 3)/4, 'R'}, {spr/4, (spr * 7)/8, 'S'}, //KLMNOPQRS
{(spr * 3)/8, spr/2, 'T'}, {(spr * 3)/8, (spr * 5)/8, 'U'}, {spr/2, (spr * 7)/8, 'V'}, {(spr * 5)/8, (spr * 3)/4, 'W'}, {(spr * 5)/8, (spr*7)/8, 'X'}, {(spr *3)/8, (spr * 3)/4, 'Y'}, {(spr * 7)/8, (spr * 3)/4, 'Z'}, {0, 0, ' '}};

//keep track of which letter positons should be implemented
int nextL = 0;
int nextR = 0; 

void setup()
{  
  //set left motor properties
  stepL.setMaxSpeed(8000.0);
  stepL.setAcceleration(4000.0);
  stepL.setSpeed(8000.0);

  //set right motor properties
  stepR.setMaxSpeed(8000.0);
  stepR.setAcceleration(4000.0);
  stepR.setSpeed(8000.0);

  //move to zero, should be here already
  stepL.moveTo(0);
  stepR.moveTo(0);

  //start serial
  Serial.begin(115200);

  establishContact();
}

/*******************************************************************************************
 * 
 * TO DO 
 *   ADD MESSAGE COMING IN FROM SERIAL
 *   BUTTON OR SENSOR CALIBRATION PER MOTOR TO SET A ZERO POINT

********************************************************************************************/
void loop()
{
  //wave the flags to get attention
  alert();

  //display the message
  message("EAT THIS CAKE");
//  if (Serial.available() > 0){
//    
//  }
}

void demo(){
  //for each letter in the alphabet and the space character
  for(int i = 0; i < 27; i++){
    //determine what rotation to send the letter
    letter(i);

    //set each motor to move to its position
    stepL.moveTo(-nextL);
    stepR.moveTo(-nextR);

    //if the motor is not there yet, keep the motor moving
    while((stepL.distanceToGo() != 0) || (stepR.distanceToGo() != 0)){
      stepL.run();
      stepR.run();
    }

    //leave the letter displayed for some time
    delay(letterdelay);
  }
  
}

void alert(){
  for (int i = 0; i < 3; i++){
    cautionwave();
  }
  nextLetterMove(0, 0);
  delay(letterdelay);
}

void cautionwave(){
  //run motion
  nextLetterMove(-(spr * 3)/8, (spr*3)/8);
  delay(20);
  //run motion
  nextLetterMove(-spr/8, spr/8);
  delay(20);
}

void letter(int i){
  //grab the next rotation position from the array
  int l = Letters[i][0];
  int r = Letters[i][1];

  nextL = l;
  nextR = r;
}


void nextLetterMove(int l, int k){
  stepL.moveTo(l);
  stepR.moveTo(k);

  //if the motor is not there yet, keep the motor moving
  while((stepL.distanceToGo() != 0) || (stepR.distanceToGo() != 0)){
      stepL.run();
      stepR.run();  
  }
  //delay(letterdelay);
}

void message(String s){
  //for each letter in the message
  for (int j = 0; j < s.length(); j++){
    for (int i = 0; i < 27; i++){
      //check which letter it is
      if (Letters[i][2] == s[j]){
        //Serial.print(Letters[i][2]);
        letter(i);
        nextLetterMove(-nextL, -nextR);
      }
    }
  }
  
  //add a pause at the end of the message
  letter(26);
  nextLetterMove(-nextL, -nextR);
  delay(letterdelay * 3);
}

void establishContact() {
  while (Serial.available() <= 0) {
    Serial.println("A");   // send an initial string
    delay(300);
  }
}
