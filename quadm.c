#include <avr/io.h>
#include "config.h"
#include <util/delay.h>

#include "quadm.h"


void matrix_clear(void)
{
	uint8_t i, b;

	for(b=1;b<=QM_NUM_BOARDS;b++)
		enable_write(b);

	for(i=0;i<48;i++)
	{
		write_byte_to_board(0);
	}

	for(b=1;b<=QM_NUM_BOARDS;b++)
		release_board(b);
}

void write_byte_to_board(uint8_t byte)
{
	// this function just shifts out one byte (doesn't touch CS)
	uint8_t i;
	for(i=0;i<8;i++)
	{
		CLOCK_LOW
		if(byte & 0x80)
			DATA_HIGH
		else
			DATA_LOW
		CLOCK_HIGH
		byte <<= 1;
	}
}

// output an array to the whole LED matrix
void write_array_to_board(unsigned char *a, uint8_t index, uint8_t buf_len)
{
	uint8_t i, b;

        for(b=1;b<=4;b++) // loop for each device on plank
        {
            enable_write(b);

            for(i=0;i<48;i++) // loop for each of 48 columns
            {
                    if(index>buf_len) index = 0; // loop around array
                    //if(index % 2)
                            write_byte_to_board(a[index]);
                    //else
                            //write_byte_to_board(a[index]>>2); 
                            // just a trick to bring the top line down
                            // so the text is centered...
                    index++;
                    
            }

            release_board(b);
        }

}


// enable chip select on a given board
void select_board (int board_number)
{

    switch (board_number)
    {
        case 1:
            CS1_HIGH;
            CS1_LOW;
        break;
        case 2:
            CS2_HIGH;
            CS2_LOW;
        break;
        case 3:
            CS3_HIGH;
            CS3_LOW;
        break;
        case 4:
            CS4_HIGH;
            CS4_LOW;
        break;
    }
}



// prefix before we can write data to board
void enable_write (int board_number)
{
    select_board(board_number);

	PUT_1	// COMMAND (101)
	PUT_0
	PUT_1

	PUT_0	// 7 bit ADDRESS (0000000)
	PUT_0
	PUT_0
	PUT_0
	PUT_0
	PUT_0
	PUT_0
}


// release chip select
void release_board(int board_number)
{
    switch (board_number)
    {
        case 1:
            CS1_HIGH;
            break;
        case 2:
            CS2_HIGH;
            break;
        case 3:
            CS3_HIGH;
            break;
        case 4:
            CS4_HIGH;
            break;
    }
}

// send an initialisation command to every board
void init_command(unsigned int command_data)
{
	uint8_t i, b;
	unsigned int data = command_data;

        for(b=1; b<=4; b++)
        {
            command_data = data;
            command_data &= 0xFFF; // commands are 3 nibbles long
            //command_data <<= 4;

            select_board(b);

            for (i=0;i<12;i++)
            {
                    CLOCK_LOW
                    if ((command_data & 0x800)) // if left-most bit is set
                            DATA_HIGH
                    else
                            DATA_LOW
                    command_data <<= 1;
                    CLOCK_HIGH
            }
            release_board(b);
        }

	return;
}
	

// send initialisation sequence
void init_matrix(void)
{
	init_command(0b100000000010); 	// sys en
	init_command(0b100000000110); 	// led on
	//init_command(0b100000010010);	// blink on
	init_command(0b100000010000); // blink off
	init_command(0b100000101110); 	// master mode
	init_command(0b100000110110); 	// internal RC
	init_command(0b100001011110); 	// commons option (24*16 matrix)
	init_command(0b100101111110);	// PWM Duty Cycle (16/16)
	matrix_clear();
}
