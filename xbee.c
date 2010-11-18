#include <avr/io.h>
#include "xbee.h"

void init_xbee(void)
{
	XBEE_PORT = 0;
	XBEE_DDR = (_BV(X_TXD) | _BV(X_RESET) | _BV(X_SLEEP_RQ));
	XBEE_PORT |= _BV(X_RESET); // disable reset
}
