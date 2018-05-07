import smbus
import time


class LightSensor(object):
    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.addr = 0x29

        # TSL2561 address
        # Select control register, 0x00(00) with command register, 0x80(128)
        #		0x03(03)	Power ON mode
        self.bus.write_byte_data(self.addr, 0x00 | 0x80, 0x03)
        # TSL2561 address
        # Select timing register, 0x01(01) with command register, 0x80(128)
        #		0x02(02)	Nominal integration time = 402ms
        self.bus.write_byte_data(self.addr, 0x01 | 0x80, 0x02)
        time.sleep(0.5)

    def get_ambient_light(self):
        # Read data back from 0x0C(12) with command register, 0x80(128), 2 bytes
        # ch0 LSB, ch0 MSB
        data = self.bus.read_i2c_block_data(self.addr, 0x0C | 0x80, 2)

        # Read data back from 0x0E(14) with command register, 0x80(128), 2 bytes
        # ch1 LSB, ch1 MSB
        data1 = self.bus.read_i2c_block_data(self.addr, 0x0E | 0x80, 2)

        # Convert the data
        ch0 = data[1] * 256 + data[0]    # full spectrum
        ch1 = data1[1] * 256 + data1[0]  # infrared

        return (ch0, ch1)
