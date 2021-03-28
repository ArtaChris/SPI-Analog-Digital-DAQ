from micropython import const
from adafruit_bus_device.spi_device import SPIDevice

# _________________________________________________________________
# |                          Start Byte                           |
# |---------------------------------------------------------------|
# |     0 |     0 |     0 |     0 |     0 |     0 |     0 |     1 |
# |---------------------------------------------------------------|
# |          Command Bits         |           Data Bits           |
# |---------------------------------------------------------------|
# | ~DIFF | ~SIGN |  MSBF |  NULL |   D11 |   D10 |   D09 |   D08 |
# |---------------------------------------------------------------|
# |                           Data Bits                           |
# |---------------------------------------------------------------|
# |   D07 |   D06 |   D05 |   D04 |   D03 |   D02 |   D01 |   D00 |
# -----------------------------------------------------------------

# ~DIFF: Select Single-ended or Differential Mode
#        0 - Differential
#        1 - Single-ended

# ~SIGN: ADC Channel (SGL) or Polarity (DIFF)
#        0 - Channel 0 / 0+ : 1-
#        1 - Channel 1 / 0- : 1+

#  MSBF: Most Significant Bit First
#        0 - MSB format read in first
#        1 - LSB format read in following MSB

# MCP4822 - 12-bit - D11:D00
# MCP4812 - 10-bit - D11:D02
# MCP4802 -  8-bit - D11:D04

_MCP3202_START_BYTE = const(0x01)
_MCP3202_CMD_MASK = const(0xE0)

_MCP3202_MODE_SELECT = const(0x80)
_MCP3202_CHAN_SELECT = const(0x40)
_MCP3202_SIGN_SELECT = const(0x40)
_MCP3202_MSBF_SELECT = const(0x20)

_MCP3202_HIGH_BYTE = const(0x0F)
_MCP3202_LOW_BYTE = const(0xFF)

_MCP3202_MAX_SCLK = const(1000000)

class MCP3202:
    cmd = bytearray(3)
    buf = bytearray(3)

    def __init__(self, spi, cs):
        self.spi_device = SPIDevice(spi, cs, baudrate=_MCP3202_MAX_SCLK, polarity=0, phase=0)


    def analogIn(self, channel):
        self.cmd[0] = _MCP3202_START_BYTE
        self.cmd[1] = ((0x01 << 7) & _MCP3202_MODE_SELECT) | ((channel << 6) & _MCP3202_CHAN_SELECT) | _MCP3202_MSBF_SELECT
        self.cmd[2] = 0x00
        self.buf[0] = 0x00
        self.buf[1] = 0x00
        self.buf[2] = 0x00
        with self.spi_device as spi:
            spi.write_readinto(self.cmd, self.buf)
        return ((self.buf[1] & _MCP3202_HIGH_BYTE) << 8) + self.buf[2]