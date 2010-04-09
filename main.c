#ifndef F_CPU
#define F_CPU 8000000L
#endif
#include <avr/io.h>
#include <util/delay.h>
#include <stdio.h>
#define RAND_MAX 6
#include <stdlib.h>

// TODO : remove this temporary workaround
//#define CONFIG_H
#include "quadm.h"
#include "uart.h"


#define SCROLLRATE      0


unsigned char bigbuffer[QM_BUFFER_SIZE];
//unsigned char bigbuffer[QM_X_PIXELS][QM_Y_PIXELS];
//unsigned char bigbuffer2[QM_BUFFER_SIZE];


int main (void)
{
	uint8_t scroll = 0;

	_delay_ms(400);
	PORTA = 0x00;
	DDRA = 0b11111111;
	PORTB = 0;
	DDRB = 0xFF;

	DDRD = 0xFF;
	//TCCR2 = 0b00010001;
	//OCR2 = 0x00;
	//
	unsigned char rxbuff[30];
	unsigned char txbuff[30];
	

	unsigned char randseed = 0;
	uint8_t x = 0;


	init_matrix();

#define L_OF 2
#define B_END QM_BUFFER_SIZE

	srand(42);

	

	while(1)
	{

		/*
		uart_init(0, rxbuff, 0, 0, txbuff);
		uart_transmit_string_block("Enter byte to use as seed\r\n > ");
		randseed = uart_receive_byte_block();
		uart_transmit_byte_block(randseed);
		uart_transmit_string_block("\r\n");
		*/

		//srand(randseed);


		for(x = 0; x < QM_BUFFER_SIZE-L_OF; x++)
		{
			bigbuffer[x] = rand() & rand() ;
		}

		_delay_ms(8);

		write_array_to_board(bigbuffer,scroll,QM_BUFFER_SIZE-1);


		if (scroll > QM_BUFFER_SIZE || scroll == 0) 	
		{	
			scroll = 0;			// start again at the end of the array
			//_delay_ms(5000);	// and pause to show the first panel
		}
		
		_delay_ms(75); 	// scroll interval 
		scroll += SCROLLRATE;	// 1 vertical line = 2 bytes


	}
}



