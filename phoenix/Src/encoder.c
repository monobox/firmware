/*
 * encoder.c
 *
 *  Created on: Jun 23, 2018
 *      Author: xi
 */

#include "stm32l4xx_hal.h"


static volatile uint8_t encoder_position = 0;
static volatile uint8_t encoder_state = 0;
static volatile const int8_t offsets_lut[16] = {0, 1, -1, 0, -1, 0, 0, 1, 1, 0, 0, -1, 0, -1, 1, 0};


void encoder_update()
{
    // Using Paul Stoffregen's strategy
    // https://github.com/PaulStoffregen/Encoder

    encoder_state &= 0x03;

    encoder_state |= HAL_GPIO_ReadPin(ENC_A_GPIO_Port, ENC_A_Pin) << 2;
    encoder_state |= HAL_GPIO_ReadPin(ENC_B_GPIO_Port, ENC_B_Pin) << 3;

    int8_t offset = offsets_lut[encoder_state];

    if ((encoder_position != 0 && offset < 0) || (encoder_position < 127 && offset > 0)) {
        encoder_position += offset;
    }

    encoder_state >>= 2;
}

uint8_t encoder_read()
{
    return encoder_position;
}
