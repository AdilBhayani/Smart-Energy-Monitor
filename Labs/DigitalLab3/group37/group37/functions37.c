/*
 * functions37.c
 *
 * Created: 10/08/2016 9:26:53 PM
 * Author: mark_ ft adil
 */ 
 #include <avr/io.h>
 #include "prototypes37.h"
 #define F_CPU 16000000UL
 #include <util/delay.h>

 //Initializes the UART
 void uart_init() {
	UBRR0H = 0;
	UBRR0L = 103;
	UCSR0B|= (1<<TXEN0);	//Sets the Transmit Enable to 1
	UCSR0C|= (1<<UCSZ00)|(1<<UCSZ01);	//Sets an 8-bit character
 }

 //Transmits the data
 void uart_transmit(uint8_t data) {
	while(!((1<<UDRE0) && UCSR0A));	//When UDRE0 is empty, put data value into buffer to be sent
	UDR0 = data;
 }

 //Initializes the timer
 void timer1_init() {
	OCR1A = 0x3D09;
	TCCR1B |= (1<<CS12)|(1<<CS10)|(1<<WGM12); //Prescaler of 1024
	TIMSK1 |= (1<<OCIE1A);	
 }
 
 //Finds the decimal place in the float
 unsigned int find_decimal(float data) {
	if (data < 10) { return 0; }
	if (data < 100) { return 1; }
	if (data < 1000) { return 2; }
	return 3;
 }

 //Converts our parameters into the value to send
 unsigned int wololo(uint8_t input, uint8_t position, uint8_t decimal) {
	unsigned int output = input;
	if (decimal == 1) { output += 16; }
	if (position == 0) { output += 96; }
	if (position == 1) { output += 64; }
	if (position == 2) { output += 32; }
	return output;
 }

 //Calculates power from a voltage array and a current array
 float calcPower(float (*voltage)[20], float (*current)[20]) {
	float power = 0;
	float newVoltage[39];
	float newCurrent[39];
	for (int i=0;i<39;i++) { //Creating 2 arrays of 39 elements for voltage and current
		if (i%2 == 0) {
			newVoltage[i] = (*voltage)[i/2];
			if ((i == 0) || (i == 38)) {
				newCurrent[i] = (*current)[i/2];
			} else {
				newCurrent[i] = linearApproximate((*current)[((i+1)/2)-1], (*current)[((i+1)/2)-2]); //For even numbered elements, current is approximated
			}
		} else {
			newVoltage[i] = linearApproximate((*voltage)[(i+1)/2], (*voltage)[((i+1)/2)-1]); //For odd numbered elements, voltage is approximated
			newCurrent[i] = (*current)[(i-1)/2];
		}
	}
	for (int i=0;i<39;i++) { //Sum the product of current and voltage for each time step
		power = power + newVoltage[i]*newCurrent[i];
	}
	power = power / 39; //Divide by the number of elements
	return power;
 }

 //Approximates a data value based on the two nearest data points
 float linearApproximate(float higher, float lower) {
	float approximation = (higher + lower) / 2;
	return approximation;
 }

 //Initialises the ADC
 void adc_init() {
	DDRC = 0x00; //Set port c as input
	ADCSRA |= (1<<ADPS0)|(1<<ADPS1)|(1<<ADPS2)|(1<<ADEN)|(1<<ADIE); //Set Prescaler to 128 and enable the ADC 
	ADMUX |= (1<<REFS0); //Set reference voltage to VCC
 }

 //Reads from ADC and returns and integer between 0 and 1023 inclusive
 unsigned int adc_read_1() {
	ADCSRA |= (1<<ADSC); //Start conversion
	while (1); 
 }

 ISR(ADC_vect) {
	adc_value = ADC;
 }

 //Reads from C0 and C2 alternately
 void adc_read_2(unsigned int* adcValue1, unsigned int* adcValue2) {
	ADMUX &= ~(1<<MUX1);
	ADCSRA |= (1<<ADSC); //Start conversion
	while ((ADCSRA & (1<<ADIF)) == 0); //Poll the ADIF bit
	(*adcValue1) = ADC;
	ADMUX |= (1<<MUX1);
	ADCSRA |= (1<<ADSC); //Start conversion
	while ((ADCSRA & (1<<ADIF)) == 0); //Poll the ADIF bit
	(*adcValue2) = ADC;
 }

 //Converts an ADC integer into the actual voltage measured by the ADC pin
 float adc_calculation(unsigned int adcValue) {
	float calculatedValue;
	calculatedValue = ((float)adcValue / 1023) * 5;
	return calculatedValue; 
 }
 
 /*
 This function figures out what the actual voltage being measured was based on reversing the process 
 that the signal went through. Option 0 for voltage, 1 for regular current, 2 for high gain current
 */
 signed int voltage_real(unsigned int adcValue, unsigned int option) {
	if (option == 0) {
		return -(adcValue - 1.7) * 98;
	} else if (option == 1) {
		return -(adcValue - 1.63) / 5.7;
	} else {
		return -(adcValue - 1.64) / 32.93;
	}
 }