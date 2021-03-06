/*
 * prototypes37.h
 *
 * Created: 10/08/2016 9:26:42 PM
 * Author: mark
 */
#include <avr/io.h> 
#ifndef PROTOTYPES37_H_
#define PROTOTYPES37_H_

void uart_init();
void uart_transmit(uint8_t data);
void timer0_init();
void timer1_init();
void int_init();
unsigned int find_decimal(float data); 
unsigned int wololo(uint8_t input, uint8_t position, uint8_t decimal);
float calcPower(float (*voltage)[10], float (*current)[10]);
float calcVoltageRMS(float (*voltage)[10]);
float calcCurrentRMS(float (*current)[10]); 
float calcCurrentPeak(float (*current)[10]);
float linearApproximate(float higher, float lower);
void adc_init();
unsigned int adc_read_voltage();
unsigned int adc_read_current(unsigned int highLow);
float adc_calculation(unsigned int adcValue);
float voltage_real(float adcValue, unsigned int option);

#endif /* PROTOTYPES37_H_ */