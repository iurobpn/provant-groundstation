void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
}

// the loop routine runs over and over again forever:
int patrick=0;
void loop() {
  // read the input on analog pin 0:
  patrick++;
  // print out the value you read:
  Serial.write('A');
  Serial.write(patrick);
  Serial.write('B');
  delay(1);        // delay in between reads for stability
}
