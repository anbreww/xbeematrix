#ifndef F_CPU
#define F_CPU 8000000UL
#endif
#include <avr/io.h>
#include <util/delay.h>
#include <stdio.h>
#define RAND_MAX 6
#include <stdlib.h>

//#define CONFIG_H
#include "quadm.h"
#define BAUD 38400
#include "uart.h"


#define SCROLLRATE      0


unsigned char bigbuffer[QM_BUFFER_SIZE];
//unsigned char bigbuffer[QM_X_PIXELS][QM_Y_PIXELS];
//unsigned char bigbuffer2[QM_BUFFER_SIZE];


int main (void)
{
	uint8_t scroll = 0;

	_delay_ms(300);
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

	uart_init(0, rxbuff, 0, 0, txbuff);
	_delay_ms(300);
	//uart_transmit_string_block("Ready for input. Please enter command as follows:\r\n ");
	//uart_transmit_string_block("<delimiter:\\x73><payload-size>payload\r\n ");
	//randseed = uart_receive_byte_block();
	//uart_transmit_byte_block(randseed);
	//uart_transmit_string_block("\r\n");
	//
#define READY_FOR_INPUT		'R'
#define ACCEPTED_DELIMITER 	'K'
#define END_OF_FILE		'E'
#define put(x)	uart_transmit_byte_block(x)


	

	while(1)
	{
		//uart_transmit_string_block("Ready for input. Please enter command as follows:\r\n ");
		//uart_transmit_string_block("<delimiter:\\x73><payload-size>payload\r\n ");
		put(READY_FOR_INPUT);

		// listen for input on uart
		unsigned char rxchar = 0;
		unsigned char nops = 0;
		while (rxchar != 0x73)
		{
			rxchar = uart_receive_byte_block();

			nops++;
			// so I don't have to keep pressing reset :)
			if (nops==0)
				put(READY_FOR_INPUT); 
		}

		put(ACCEPTED_DELIMITER);
		// read array size from next char (low, high)
		unsigned char size_l = uart_receive_byte_block();
		//unsigned char size_h = uart_receive_byte_block(); //unimplemented
		// verify size
		//uart_send_dec((int)size_l);
		//
		int i = 0;
		for (i = 0; i < size_l; i++)
		{
			bigbuffer[i] = uart_receive_byte_block();
		}

		//put(END_OF_FILE);
		//put('\r');
		//put('\n');


		// display new info on board



		//srand(randseed);



		//_delay_ms(8);

		//write_array_to_board(bigbuffer,scroll,QM_BUFFER_SIZE-1);
		write_array_to_board(bigbuffer,scroll,QM_BUFFER_SIZE-1);


		if (scroll > QM_BUFFER_SIZE || scroll == 0) 	
		{	
			scroll = 0;			// start again at the end of the array
			//_delay_ms(5000);	// and pause to show the first panel
		}
		
		//_delay_ms(75); 	// scroll interval 
		scroll += SCROLLRATE;	// 1 vertical line = 2 bytes


	}
}



