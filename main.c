#include <avr/io.h>

#include "config.h"

#include <util/delay.h>
#include <stdio.h>
#define RAND_MAX 6
#include <stdlib.h>

#include "quadm.h"
#include "uart.h"


#define SCROLLRATE      0
#define READY_FOR_INPUT		'R'
#define ACCEPTED_DELIMITER 	'K'
#define END_OF_FILE		'E'
#define START_BYTE		0x73 // 's'
#define put(x)	uart_transmit_byte_block(x)

#define L_OF 2
#define B_END QM_BUFFER_SIZE

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
	
	unsigned char rxbuff[30];
	unsigned char txbuff[30];

	init_matrix();

	uart_init(0, rxbuff, 0, 0, txbuff);
	_delay_ms(300);


	while(1)
	{
		put(READY_FOR_INPUT);

		// listen for input on uart
		unsigned char rxchar = 0;
		unsigned char nops;
		nops = 0;
		while (rxchar != START_BYTE)
		{
			rxchar = uart_receive_byte_block();

			nops++;
			// so I don't have to keep pressing reset :)
			if (nops%128==0)
				put(READY_FOR_INPUT); 
		}

		put(ACCEPTED_DELIMITER);

		// read array size from next char (low, high)
		unsigned char size_l = uart_receive_byte_block();
		//unsigned char size_h = uart_receive_byte_block(); //unimplemented
		
		// verify size
		//uart_send_dec((int)size_l);
		
		int i = 0;
		for (i = 0; i < size_l; i++)
		{
			bigbuffer[i] = uart_receive_byte_block();
		}

		write_array_to_board(bigbuffer,scroll,QM_BUFFER_SIZE-1);


		if (scroll > QM_BUFFER_SIZE || scroll == 0) 	
		{	
			scroll = 0;			// start again at the end of the array
			//_delay_ms(5000);	// and pause to show the first panel
		}
		
		scroll += SCROLLRATE;	// 1 vertical line = 2 bytes


	}
}



