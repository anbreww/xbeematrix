#define F_CPU 8000000UL

#include <avr/io.h>
#include <util/delay.h>
#include <stdio.h>
#include <avr/interrupt.h>
#include <avr/wdt.h>

#include "uart.h"
#include "uart1.h"

#define MATRIX_DDR 	DDRA
#define MATRIX_PORT 	PORTA
#define M_CS1 	7
#define M_CS2	6
#define M_CS3	5
#define M_CS4	4
#define M_WR 	3
#define M_DATA 	1

#define CLOCK_HIGH	MATRIX_PORT |= 	(1 << M_WR);
#define CLOCK_LOW	MATRIX_PORT &= ~(1 << M_WR);
#define DATA_HIGH	MATRIX_PORT |= 	(1 << M_DATA);
#define DATA_LOW	MATRIX_PORT &= ~(1 << M_DATA);
#define CS1_HIGH	MATRIX_PORT |= 	(1 << M_CS1);
#define CS1_LOW		MATRIX_PORT &= ~(1 << M_CS1);
#define CS2_HIGH	MATRIX_PORT |= 	(1 << M_CS2);
#define CS2_LOW		MATRIX_PORT &= ~(1 << M_CS2);
#define CS3_HIGH	MATRIX_PORT |= 	(1 << M_CS3);
#define CS3_LOW		MATRIX_PORT &= ~(1 << M_CS3);
#define CS4_HIGH	MATRIX_PORT |= 	(1 << M_CS4);
#define CS4_LOW		MATRIX_PORT &= ~(1 << M_CS4);
#define WAIT		_delay_us(2);
#define PUT_1		CLOCK_LOW	 WAIT	DATA_HIGH	WAIT	CLOCK_HIGH	WAIT;
#define PUT_0		CLOCK_LOW	 WAIT	DATA_LOW	WAIT	CLOCK_HIGH	WAIT;


#define SCROLLRATE      0


const int numbers_count = 10;
const unsigned char numbers_5x7[10][5] = {
  {0x3e, 0x45, 0x49, 0x51, 0x3e},
  {0x00, 0x10, 0x20, 0x7f, 0x00},
  {0x47, 0x49, 0x49, 0x49, 0x31},
  {0x42, 0x49, 0x59, 0x69, 0x46},
  {0x08, 0x18, 0x28, 0x7f, 0x08},
  {0x71, 0x49, 0x49, 0x49, 0x46},
  {0x3e, 0x49, 0x49, 0x49, 0x06},
  {0x40, 0x47, 0x48, 0x50, 0x60},
  {0x36, 0x49, 0x49, 0x49, 0x36},
  {0x30, 0x49, 0x49, 0x49, 0x3e}
};

const unsigned char letters_5x7[26][5] = {
  {0x3f, 0x48, 0x48, 0x48, 0x3f},
  {0x7f, 0x49, 0x49, 0x49, 0x36},
  {0x3e, 0x41, 0x41, 0x41, 0x22},
  {0x7f, 0x41, 0x41, 0x22, 0x1c},
  {0x7f, 0x49, 0x49, 0x49, 0x41},
  {0x7f, 0x48, 0x48, 0x48, 0x40},
  {0x3e, 0x41, 0x49, 0x49, 0x2e},
  {0x7f, 0x08, 0x08, 0x08, 0x7f},
  {0x00, 0x41, 0x7f, 0x41, 0x00},
  {0x06, 0x01, 0x01, 0x01, 0x7e},
  {0x7f, 0x08, 0x14, 0x22, 0x41},
  {0x7f, 0x01, 0x01, 0x01, 0x01},
  {0x7f, 0x20, 0x10, 0x20, 0x7f},
  {0x7f, 0x10, 0x08, 0x04, 0x7f},
  {0x3e, 0x41, 0x41, 0x41, 0x3e},
  {0x7f, 0x48, 0x48, 0x48, 0x30},
  {0x3e, 0x41, 0x45, 0x42, 0x3d},
  {0x7f, 0x48, 0x4c, 0x4a, 0x31},
  {0x31, 0x49, 0x49, 0x49, 0x46},
  {0x40, 0x40, 0x7f, 0x40, 0x40},
  {0x7e, 0x01, 0x01, 0x01, 0x7e},
  {0x7c, 0x02, 0x01, 0x02, 0x7c},
  {0x7f, 0x02, 0x04, 0x02, 0x7f},
  {0x63, 0x14, 0x08, 0x14, 0x63},
  {0x60, 0x10, 0x0f, 0x10, 0x60},
  {0x43, 0x45, 0x49, 0x51, 0x61}
};

/*
unsigned char Fireday[] ={ 		// "Fireday UNO"
		0xF8,0x00,0xA0,0x7C,0x80,0x7E,0x00,0x06,	
		0xF8,0x06,0x00,0x7E,0xF8,0x7C,0xA0,0x00,

		0x58,0x00,0x00,0x7E,0xF8,0x7E,0xA8,0x38,
		0x00,0x1C,0xF8,0x7E,0x88,0x7E,0x70,0x00,

		0x00,0x00,0x78,0x3C,0xA0,0x7E,0x78,0x66,
		0x00,0x66,0xC0,0x7E,0x38,0x3C,0xC0,0x00,

		0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
		0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,

//		};
//unsigned char Samedi[] = {	// "Samedi 29 NOV"
		0xE8,0x26,0xA8,0x4a,0xB8,0x52,0x00,0x22,
		0x78,0x00,0xa0,0x72,0xa0,0x54,0x78,0x78,

		0x00,0x00,0xf8,0x7e,0x40,0x30,0x20,0x18,
		0x40,0x7e,0xF8,0x00,0x00,0x3c,0xf8,0x42,

		0xa8,0x42,0x88,0x3c,0x00,0x00,0xf8,0x78,
		0x88,0x04,0x70,0x02,0x00,0x04,0xf8,0x78,

		0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
		0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
};
*/

void init_matrix(void);
// issues all the init commands

void init_command(unsigned int command_data);
// for sending init command

void write_array_to_board(unsigned char *a, uint8_t index);
// *a is array, index is start value

void write_byte_to_board(uint8_t byte);	
// use this only after write sequence has begun (101 + address)

void select_board (int board_number);
// select board number before writing data to it.

void enable_write(int board_number);
// enable chip select on board

void release_board(int board_number);
// release chip select on board (always use this after writing to a board!)

void write_number(uint8_t number,uint8_t offset,uint8_t digits);
void write_spaces(uint8_t num_spaces);
void write_letter(uint8_t letter,uint8_t offset);
void flash_board(unsigned int n_times, unsigned int delayms);
void write_string(char *string, uint8_t length);
void reset_mcu(void); // use WDT to hardware reset

// TODO : FUNCTIONS TO BE WRITTEN

// write data to whole matrix (automatically switch to next board)

// write alphanumeric string at a given height

// display contents of a variable (decimal)
//
// Need an option to write to only one line.
// Two possible implementations:
// 1 - use address selection for every byte (+= 2 and loop)
// 2 - write everything to an SRAM table (144 bytes) and output table to matrix
//     probably nicest solution unless timing is critical.

FILE uart1_str = FDEV_SETUP_STREAM(uart1_putchar, uart1_getchar, _FDEV_SETUP_RW);
FILE uart_str = FDEV_SETUP_STREAM(uart_putchar, uart_getchar, _FDEV_SETUP_RW);
//FILE matrix_str = FDEV_SETUP_STREAM(uart_putchar, uart_getchar, _FDEV_SETUP_RW);


int main (void)
{
    char buf[30];
	//uint8_t scroll = 0;

	_delay_ms(400);
        // *** init ports ***
	PORTA = 0x00;
	DDRA = 0xFF;
	PORTB = 0;
	DDRB = 0xFF;

	DDRD = 0xFF;
	//TCCR2 = 0b00010001;
	//OCR2 = 0x00;

        // *** INIT FILE STREAMS *** //
	_delay_ms(10);
        uart_init();
	uart1_init(12);

        stderr = stdout = stdin = &uart_str;

	init_matrix();

        uint8_t n=0;

        // erase matrix
        for(n=1;n<=4;n++)
        {
            uint8_t i;
            enable_write(n);
            for(i=0;i<48;i++)
                write_byte_to_board(0x00);
            release_board(n);

        }
        _delay_ms(300);

        flash_board(4,250);
        flash_board(8,100);


        n=0;


            while(1)
            {
              printf("Ready\n > ");
	      fprintf(&uart1_str, "AAA\n");

              if (fgets(buf, sizeof buf - 1, stdin) == NULL)
                  break;

              printf(">> %s\n",buf);

              if (buf[0] == 'R')
                  if (buf[1] == 'S')
                      if (buf[2] == 'T')
                          reset_mcu();

                _delay_ms(100);

                enable_write(1);

                    //write_spaces(3);
                    write_string(buf,4);

                release_board(1);

                enable_write(2);

                    write_spaces(4);
                    write_number(n,4,1);

                release_board(2);

                enable_write(3);

                    write_byte_to_board(0xFF);
                    write_byte_to_board(0xFF);
                    write_byte_to_board(0xFF);
                    write_byte_to_board(0xFF);
                    write_spaces(8);
                    write_number(99-n,4,1);

                release_board(3);

                enable_write(4);
                    write_string("blue",4);
                release_board(4);

                n++;
                if (n >= 100)
                    n = 0;
            }

	    while(1);


}

void write_spaces(uint8_t num_spaces)
{
    while(num_spaces>0)
    {
        write_byte_to_board(0x00);
        write_byte_to_board(0x00);
        num_spaces--;
    }
}


void write_number(uint8_t number,uint8_t offset,uint8_t digits)
{
    //uint8_t digit=0;
    // start with only 2 digit numbers
    // TODO : correct this function to use the DIGITS argument
    uint8_t chiffre=0;
    uint8_t i,current_byte;
    while(1)
    {
        if(number<10)
            break;
        else
        {
            number -= 10;
            chiffre++;
        }
    }
    for(i=0;i<5;i++)
    {
        if(chiffre == 0)
            current_byte = 0x00;
        else
            current_byte = numbers_5x7[chiffre][i];
        write_byte_to_board(current_byte>>offset);
        write_byte_to_board(current_byte<<(8-offset));
    }

    write_byte_to_board(0x00);
    write_byte_to_board(0x00);

    chiffre = number;
    for(i=0;i<5;i++)
    {
        current_byte = numbers_5x7[chiffre][i];
        write_byte_to_board(current_byte>>offset);
        write_byte_to_board(current_byte<<(8-offset));
    }
}

void write_letter(uint8_t letter,uint8_t offset)
    // currently only works with lowercase
{
    uint8_t i,current_byte=0;
    for(i=0;i<5;i++)
    {
        current_byte = letters_5x7[letter][i];
        write_byte_to_board(current_byte>>offset);
        write_byte_to_board(current_byte<<(8-offset));
    }
    write_byte_to_board(0x00);
    write_byte_to_board(0x00);
}

void write_string(char *string, uint8_t length)
{
    uint8_t i, char_to_write;
    for(i=0;i<length;i++)
    {
        char_to_write = string[i];
        if (char_to_write == ' ')
        {
            write_byte_to_board(0x00);
            write_byte_to_board(0x00);
            write_byte_to_board(0x00);
            write_byte_to_board(0x00);
            write_byte_to_board(0x00);
            write_byte_to_board(0x00);
            write_byte_to_board(0x00);
            write_byte_to_board(0x00);
            write_byte_to_board(0x00);
            write_byte_to_board(0x00);
            write_byte_to_board(0x00);
            write_byte_to_board(0x00);
        } else {
            write_letter(char_to_write-'a',4);
        }
    }
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
void write_array_to_board(unsigned char *a, uint8_t index)
{
	uint8_t i, b;

        for(b=1;b<=4;b++) // loop for each device on plank
        {
            enable_write(b);

            for(i=0;i<48;i++) // loop for each of 48 columns
            {
                    if(index>127) index = 0; // loop around array
                    if(index % 2)
                            write_byte_to_board(a[index]);
                    else
                            write_byte_to_board(a[index]>>2); 
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

void wait_ms(uint16_t ms)
{
	while(ms)
	{
		_delay_ms(1);
                ms--;
	}
}

void flash_board(unsigned int n_times, unsigned int delayms)
{
    uint8_t n = 0;
        while(n_times)
        {
            for(n=1;n<=4;n++)
            {
                uint8_t i;
                enable_write(n);
                for(i=0;i<48;i++)
                    write_byte_to_board(0xff);
                release_board(n);

            }
            wait_ms(delayms);
            for(n=1;n<=4;n++)
            {
                uint8_t i;
                enable_write(n);
                for(i=0;i<48;i++)
                    write_byte_to_board(0x00);
                release_board(n);

            }
            wait_ms(delayms);
            n_times--;
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
}

void reset_mcu(void) // use WDT to hardware reset
{
    wdt_enable(WDTO_15MS);
    while(1);
}

