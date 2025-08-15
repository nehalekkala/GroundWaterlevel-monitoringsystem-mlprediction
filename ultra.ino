#define trigPin1  5 
#define echoPin1 4  
#define trigPin3 0  
#define echoPin3 2  
// Function to measure water level using ultrasonic sensor
float measureDistance(int trigPin, int echoPin) {  
    digitalWrite(trigPin, LOW);  
    delayMicroseconds(2);  
    digitalWrite(trigPin, HIGH);  
    delayMicroseconds(10);  
    digitalWrite(trigPin, LOW);  

    long duration = pulseIn(echoPin, HIGH);  
    return duration * 0.034 / 2;  // Convert to cm
}  
void setup() {  
    Serial.begin(115200);  // Start Serial Monitor
    pinMode(trigPin1, OUTPUT);  
    pinMode(echoPin1, INPUT);  
    pinMode(trigPin3, OUTPUT);  
    pinMode(echoPin3, INPUT);  
    // Print CSV Header
    Serial.println("Timestamp,Water_Level_1 (cm),Water_Level_3 (cm)");  
}  
void loop() {  
    float level1 = measureDistance(trigPin1, echoPin1);  
    float level3 = measureDistance(trigPin3, echoPin3);  
    Serial.print(millis());  // Timestamp  
    Serial.print(",");  
    Serial.print(level1);  
    Serial.print(",");  
    Serial.println(level3);  
    delay(5000);  // Collect data every 5 seconds  
}
