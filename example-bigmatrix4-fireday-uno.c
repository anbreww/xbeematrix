#define F_CPU 8000000L
#include <avr/io.h>
#include <util/delay.h>

#define MATRIX_DDR 	DDRA
#define MATRIX_PORT PORTA
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


#define SCROLLRATE      2

/*unsigned char Array1[128]={
                        0x11,0x10,0x01,0x81,0x10,0x01,0x81,0x81,
                        0x22,0x20,0x02,0x42,0x20,0x02,0x42,0x20,
                        0x33,0x30,0x03,0xc3,0x30,0x03,0xc3,0x30,
                        0x44,0x40,0x04,0x24,0x40,0x04,0x24,0x40,
                        0x55,0x50,0x05,0xa5,0x50,0x05,0xa5,0x50,
                        0x66,0x60,0x06,0x66,0x60,0x06,0x66,0x60,
                        0x77,0x70,0x07,0xe7,0x70,0x07,0xe7,0x70,
                        0x88,0x80,0x08,0x18,0x80,0x08,0x18,0x80,
                       
                        0x88,0x80,0x08,0x18,0x80,0x08,0x18,0x80,
                        0x77,0x70,0x07,0xe7,0x70,0x07,0xe7,0x70,
                        0x66,0x60,0x06,0x66,0x60,0x06,0x66,0x60,
                        0x55,0x50,0x05,0xa5,0x50,0x05,0xa5,0x50,
                        0x44,0x40,0x04,0x24,0x40,0x04,0x24,0x40,
                        0x33,0x30,0x03,0xc3,0x30,0x03,0xc3,0x30,
                        0x22,0x20,0x02,0x42,0x20,0x02,0x42,0x20,
                        0x11,0x10,0x01,0x81,0x10,0x01,0x81,0x10
                        };   */
unsigned char AArray[] ={
		0x01,0x80,0x03,0xC0,0x07,0xE0,0x0F,0xF0,
		0x1F,0xF8,0x3F,0xFC,0x7F,0xFE,0xFF,0xFF,
		0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
		0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
		0xFF,0xFF,0x7F,0xFE,0x3F,0xFC,0x1F,0xF8,
		0x0F,0xF0,0x07,0xE0,0x03,0xC0,0x01,0x80,
		};   
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

int main (void)
{
	uint8_t scroll = 0;

	_delay_ms(400);
	PORTA = 0x00;
	DDRA = 0b11111111;
	PORTB = 0;
	DDRB = 0xFF;

	DDRD = 0xFF;
	TCCR2 = 0b00010001;
	OCR2 = 0x00;


	init_matrix();
	while(1)
	{

		_delay_ms(8);

		write_array_to_board(Fireday,scroll);
		//write_array_to_board(Samedi,scroll);



		if (scroll == 64);
	//	_delay_ms(2000);	// pause in the middle for second panel

		if (scroll > 128 || scroll == 0) 	
		{	
			scroll = 0;			// start again at the end of the array
			//_delay_ms(5000);	// and pause to show the first panel
		}
		
		_delay_ms(75); 	// scroll interval 
		scroll += SCROLLRATE;	// 1 vertical line = 2 bytes

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
