from micropython import const
from adafruit_bus_device.spi_device import SPIDevice

# _________________________________________________________________
# |                  Command Bits                 |   Data Bits   |
# |---------------------------------------------------------------|
# |    A3 |    A2 |    A1 |    A0 |    C1 |    C0 |   D09 |   D08 |
# |---------------------------------------------------------------|
# |                           Data Bits                           |
# |---------------------------------------------------------------|
# |   D07 |   D06 |   D05 |   D04 |   D03 |   D02 |   D01 |   D00 |
# -----------------------------------------------------------------

# A3:A0: Register Address
#        0 - DAC0 (A)
#        1 - DAC1 (B)

# C1:C0: Command Select
#        0 - 2x, 0.5mV/LSB
#        1 - 1x, 1.0mV/LSB

# ~SHDN: Shutdown
#        0 - DAC Disabled
#        1 - DAC Enabled

# ~LDAC: Latch DAC Input
#        LO - Synchronize DAC Output with Input on CS Rise
#        HI - Maintain DAC Output since trigger

# MCP4822 - 12-bit - D11:D00
# MCP4812 - 10-bit - D11:D02
# MCP4802 -  8-bit - D11:D04


_MCP41X1_REG_SELECT = const(0xF0)
_MCP41X1_CMD_SELECT = const(0x0C)

_MCP41X1_WIPER_0 = const(0x00)
_MCP41X1_WIPER_1 = const(0x01)

_MCP41X1_WRITE = const(0x00)
_MCP41X1_READ = const(0x0C)
_MCP41X1_INCR = const(0x04)
_MCP41X1_DECR = const(0x08)

_MCP41X1_HIGH_BYTE = const(0x03)
_MCP41X1_LOW_BYTE = const(0xFF)

_MCP41X1_MAX_SCLK = const(10000000)

class MCP41X1:

    def __init__(self, spi, cs):
        self.spi_device = SPIDevice(spi, cs, baudrate=_MCP41X1_MAX_SCLK, polarity=0, phase=0)


    def setValue(self, value):
        buf = bytearray(2)
        buf[0] = ((_MCP41X1_WIPER_0 << 4) & _MCP41X1_REG_SELECT) | ((_MCP41X1_WRITE << 2) & _MCP41X1_CMD_SELECT) | ((value >> 8) & _MCP41X1_HIGH_BYTE)
        buf[1] = (value & _MCP41X1_LOW_BYTE)
        with self.spi_device as spi:
            spi.write(buf)