from micropython import const
from adafruit_bus_device.spi_device import SPIDevice

# _________________________________________________________________
# |          Command Bits         |           Data Bits           |
# |---------------------------------------------------------------|
# |  ~A/B |   XXX |   ~GA | ~SHDN |   D11 |   D10 |   D09 |   D08 |
# |---------------------------------------------------------------|
# |                           Data Bits                           |
# |---------------------------------------------------------------|
# |   D07 |   D06 |   D05 |   D04 |   D03 |   D02 |   D01 |   D00 |
# -----------------------------------------------------------------

#  ~A/B: Select DAC
#        0 - DAC0 (A)
#        1 - DAC1 (B)

#   ~GA: Gain Adjust
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


_MCP48X2_DAC_SELECT = const(0x80)
_MCP48X2_GAIN_ADJUST = const(0x20)
_MCP48X2_SHUTDOWN = const(0x10)

_MCP48X2_HIGH_BYTE = const(0x0F)
_MCP48X2_LOW_BYTE = const(0xFF)

_MCP48X2_MAX_SCLK = const(20000000)

class MCP48X2:
    gain = 0
    buf = bytearray(2)

    def __init__(self, spi, cs):
        self.spi_device = SPIDevice(spi, cs, baudrate=_MCP48X2_MAX_SCLK, polarity=0, phase=0)


    def analogOut(self, channel, value, gain = 0):
        self.buf[0] = ((channel << 7) & _MCP48X2_DAC_SELECT) | ((gain << 5) & _MCP48X2_GAIN_ADJUST) | (_MCP48X2_SHUTDOWN) | ((value >> 8) & _MCP48X2_HIGH_BYTE)
        self.buf[1] = (value & _MCP48X2_LOW_BYTE)
        with self.spi_device as spi:
            spi.write(self.buf)


    def analogResolution(self, gain):
        if gain is 1:
            self.gain = 0
        else:
            self.gain = 1


    def dacShutdown(self, channel):
        self.buf[0] = ((channel << 8) & _MCP48X2_DAC_SELECT) | ((self.gain << 6) & _MCP48X2_GAIN_ADJUST) | (_MCP48X2_SHUTDOWN)
        self.buf[0] = 0x00
        with self.spi_device as spi:
            spi.write(self.buf)