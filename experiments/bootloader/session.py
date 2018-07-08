#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Sample bootloader (STM32 stock bootloader) session interface

Connect USART1 to RPi's UART (pins 8, 10)
Connect STM's nRST to RPI's BCM23 (pin 16)
Connect STM's BOOT0 to RPI's BCM24 (pin 18)

Ensure to add these two lines to RPi's /boot/config.txt:

    enable_uart=1
    dtoverlay=pi3-miniuart-bt

And use /dev/serial0

Note: the overlay above swaps the miniuart between the UART pins and the BT module
'''

import time
import argparse
import atexit
import logging

import serial

import RPi.GPIO as GPIO


logger = logging.getLogger(__name__)


class GPIOControl:
    PIN_NRST = 23
    PIN_BOOT0 = 24

    def __init__(self):
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.PIN_NRST, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.PIN_BOOT0, GPIO.OUT, initial=GPIO.LOW)

        atexit.register(GPIO.cleanup)

    def reset(self):
        GPIO.output(self.PIN_NRST, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(self.PIN_NRST, GPIO.HIGH)

    def boot_sysmem(self):
        GPIO.output(self.PIN_BOOT0, GPIO.HIGH)
        self.reset()
        time.sleep(0.1)



class BootloaderSession:
    HELLO = 0x7f
    ACK = 0x79
    NAK = 0x1f

    def __init__(self, port):
        self._ser = serial.Serial(port, 115200, parity=serial.PARITY_EVEN, timeout=0.5)
        self._ser.flush()
        self._gpioctl = GPIOControl()

    def connect(self):
        self._gpioctl.boot_sysmem()
        return self._handshake()

    def get_pid(self):
        '''Check AN2606 for a PID table'''

        self._send(0x02)

        if self._expect(self.ACK):
            comps = self._read_packet()
            return comps[0] << 8 | comps[1]
        else:
            logger.error('Unable to retrieve PID')
            return None

    def _send(self, *seq, send_checksum=True):
        seq = list(seq)

        if send_checksum:
            if len(seq) == 1:
                csum = seq[0] ^ 0xff
            else:
                csum = 0

                for b in seq:
                    csum ^= b

            seq.append(csum)

        logger.debug('Sending: {}'.format(seq))

        self._ser.write(bytearray(seq))

    def _expect(self, *seq):
        logger.debug('Expecting: {}'.format(seq))
        rx_data = self._ser.read(len(seq))

        logger.debug('Received data={}'.format(rx_data))

        return rx_data == bytearray(seq)

    def _read_packet(self):
        length = ord(self._ser.read(1))
        logger.debug('read len={}'.format(length))

        data = self._ser.read(length + 1)

        if self._expect(self.ACK):
            return list(bytearray(data))
        else:
            logger.error('Missed ACK while reading packet')

            return None

    def _handshake(self):
        self._send(self.HELLO, send_checksum=False)

        if not self._expect(self.ACK):
            logger.error('Cannot initiate bootloader session')

            return False
        else:
            logger.info('Bootloader connection established')

            return True




def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('port')
    parser.add_argument('--debug', '-d', action='store_true')

    return parser.parse_args()

def main():
    args = parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    session = BootloaderSession(args.port)

    if session.connect():
        logger.info('Product ID: 0x{0:02x}'.format(session.get_pid()))


if __name__ == '__main__':
    main()
