/*
 * button.h
 *
 *  Created on: Jul 1, 2018
 *      Author: xi
 */

#ifndef BUTTON_H_
#define BUTTON_H_

typedef enum ButtonState {
    BUTTON_STATE_INIT,
    BUTTON_STATE_PUSHED,
    BUTTON_STATE_RELEASED,
    BUTTON_STATE_DOWN,
    BUTTON_STATE_UP
} ButtonState;

ButtonState button_update();

#endif /* BUTTON_H_ */
