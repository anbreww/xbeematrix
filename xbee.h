#ifndef XBEE_H
#define XBEE_H

#define XBEE_DDR	DDRD
#define XBEE_PORT	PORTD
#define XBEE_PINS	PIND
#define X_RXD		2
#define	X_TXD		3
#define X_ON_SLEEP	4
#define X_RESET		5
#define X_SLEEP_RQ	6

void init_xbee(void);

#endif
