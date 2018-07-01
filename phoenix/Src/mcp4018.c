/*
 * mcp4018.c
 *
 *  Created on: Jul 1, 2018
 *      Author: xi
 */

#include "stm32l4xx_hal.h"

#include "mcp4018.h"

static const uint8_t MCP4018_ADDRESS = 0x2f;

extern I2C_HandleTypeDef hi2c1;


int mcp4018_set_wiper(uint8_t value)
{
    // MCP4018 address: 0x2f, send directly the wiper value (7-bits)
    HAL_StatusTypeDef rc = HAL_I2C_Master_Transmit(&hi2c1, MCP4018_ADDRESS << 1, &value, 1, HAL_MAX_DELAY);

    if (rc != HAL_OK) {
       return 0;
    } else {
        return -1;
    }

}
