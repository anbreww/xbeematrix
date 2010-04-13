#ifndef QUADM_H
/*
 * Robopoly library for Quad Matrix display
 * Group of four 16x24 led matrix displays from Sure Electronics
 *
 * Andrew Watson - 2010
 * This code is licensed under the LGPL
 *
 */


/*
 * Pin and Port definitions. Should live in a config.h
 */

#ifndef HARDWARE_H
//#warning "Hardware configuration file not defined. Using default pin mapping"


#define MATRIX_DDR 	DDRA
#define MATRIX_PORT PORTA
#define M_CS1 	7
#define M_CS2	6
#define M_CS3	5
#define M_CS4	4
#define M_WR 	3
#define M_DATA 	1


#endif

/*
 * Bit-banging macros
 */

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

/*
 * General matrix specs
 */
#define QM_ROWS		16			// X pixels
#define QM_COLS		24			// Y pixels
#define QM_NUM_BOARDS	4			// number of boards on bus

#define QM_BYTE_ROWS	(QM_ROWS/8)		// vertical bytes 
#define QM_BYTE_COLS	(QM_BYTE_ROWS*QM_COLS)	// total bytes for one matrix
#define QM_BUFFER_SIZE	(QM_NUM_BOARDS*QM_BYTE_COLS)

#define QM_X_PIXELS	(QM_COLS*QM_NUM_BOARDS)
#define QM_Y_PIXELS	(QM_ROWS)

/*
 * Command bytes
 * Matrix takes two kinds of commands.
 * ID_CMD followed by 9-bit command code
 * or
 * read/write ID followed by 7 bit address + 4 bits data
 * - definitions stolen from Bill Westfield's sample code on Arduino forums
 */

#define QM_ID_CMD 4		/* ID = 100 - Commands */
#define QM_ID_RD  6		/* ID = 110 - Read RAM */
#define QM_ID_WR  5		/* ID = 101 - Write RAM */

#define QM_CMD_SYSDIS 0x00	/* CMD= 0000-0000-x Turn off oscil */
#define QM_CMD_SYSON  0x01	/* CMD= 0000-0001-x Enable system oscil */
#define QM_CMD_LEDOFF 0x02	/* CMD= 0000-0010-x LED duty cycle gen off */
#define QM_CMD_LEDON  0x03	/* CMD= 0000-0011-x LEDs ON */
#define QM_CMD_BLOFF  0x08	/* CMD= 0000-1000-x Blink ON */
#define QM_CMD_BLON   0x09	/* CMD= 0000-1001-x Blink Off */
#define QM_CMD_SLVMD  0x10	/* CMD= 0001-00xx-x Slave Mode */
#define QM_CMD_MSTMD  0x14	/* CMD= 0001-01xx-x Master Mode */
#define QM_CMD_RCCLK  0x18	/* CMD= 0001-10xx-x Use on-chip clock */
#define QM_CMD_EXTCLK 0x1C	/* CMD= 0001-11xx-x Use external clock */
#define QM_CMD_COMS00 0x20	/* CMD= 0010-ABxx-x commons options */
#define QM_CMD_COMS01 0x24	/* CMD= 0010-ABxx-x commons options */
#define QM_CMD_COMS10 0x28	/* CMD= 0010-ABxx-x commons options */
#define QM_CMD_COMS11 0x2C	/* CMD= 0010-ABxx-x commons options */
#define QM_CMD_PWM    0xA0	/* CMD= 101x-PPPP-x PWM duty cycle */

/*
 * Function definitions
 */

void init_matrix(void);
// issues all the init commands

void matrix_clear(void);
// clear the display

void init_command(unsigned int command_data);
// for sending init command

void write_array_to_board(unsigned char *a, uint8_t index, uint8_t buf_len);
// *a is array, index is start value

void write_byte_to_board(uint8_t byte);	
// use this only after write sequence has begun (101 + address)

void select_board (int board_number);
// select board number before writing data to it.

void enable_write(int board_number);
// enable chip select on board

void release_board(int board_number);
// release chip select on board (always use this after writing to a board!)


#endif
