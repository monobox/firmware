/*
 * button.c
 *
 *  Created on: Jul 1, 2018
 *      Author: xi
 */

#include "stm32l4xx_hal.h"

#include "button.h"

extern uint32_t sys_timer_ms;

static ButtonState button_state_saved = BUTTON_STATE_INIT;


ButtonState button_update()
{
    if (HAL_GPIO_ReadPin(ENC_BUT_GPIO_Port, ENC_BUT_Pin) == GPIO_PIN_RESET) {
        if (button_state_saved != BUTTON_STATE_DOWN) {
            button_state_saved = BUTTON_STATE_DOWN;

            return BUTTON_STATE_PUSHED;
        } else {
            return BUTTON_STATE_DOWN;
        }
    } else {
        if (button_state_saved != BUTTON_STATE_UP) {
            button_state_saved = BUTTON_STATE_UP;

            return BUTTON_STATE_RELEASED;
        } else {
            return BUTTON_STATE_UP;
        }
    }
}
