# MPU6050 MicroPython Library for ESP32
# Save this as mpu6050.py on your device

from machine import I2C, Pin
import time

# MPU6050 Register Map
MPU6050_ADDR = 0x68
PWR_MGMT_1 = 0x6B
SMPLRT_DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
ACCEL_CONFIG = 0x1C
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47
TEMP_OUT_H = 0x41

class MPU6050:
    def __init__(self, i2c, addr=MPU6050_ADDR):
        """
        Initialize MPU6050 sensor
        
        Args:
            i2c: I2C object
            addr: I2C address (default 0x68)
        """
        self.i2c = i2c
        self.addr = addr
        
        # Wake up the MPU6050 (remove sleep mode)
        self.i2c.writeto_mem(self.addr, PWR_MGMT_1, b'\x00')
        time.sleep(0.1)
        
        # Configure sample rate (1kHz)
        self.i2c.writeto_mem(self.addr, SMPLRT_DIV, b'\x07')
        
        # Configure accelerometer (±2g range)
        self.i2c.writeto_mem(self.addr, ACCEL_CONFIG, b'\x00')
        
        # Configure gyroscope (±250 °/s range)
        self.i2c.writeto_mem(self.addr, GYRO_CONFIG, b'\x00')
        
        print("MPU6050 initialized successfully")
    
    def read_raw_data(self, addr):
        """
        Read 2 bytes of data from register address
        """
        try:
            # Read 2 bytes (high and low)
            data = self.i2c.readfrom_mem(self.addr, addr, 2)
            # Combine bytes and handle negative values (two's complement)
            value = (data[0] << 8) | data[1]
            if value > 32768:
                value = value - 65536
            return value
        except Exception as e:
            print(f"Error reading from register {hex(addr)}: {e}")
            return 0
    
    def get_accel_data(self):
        """
        Get accelerometer data in g-forces
        
        Returns:
            tuple: (x, y, z) accelerometer values in g
        """
        # Read raw values and convert to g (±2g range: 16384 LSB/g)
        x = self.read_raw_data(ACCEL_XOUT_H) / 16384.0
        y = self.read_raw_data(ACCEL_YOUT_H) / 16384.0
        z = self.read_raw_data(ACCEL_ZOUT_H) / 16384.0
        return x, y, z
    
    def get_gyro_data(self):
        """
        Get gyroscope data in degrees per second
        
        Returns:
            tuple: (x, y, z) gyroscope values in °/s
        """
        # Read raw values and convert to °/s (±250 °/s range: 131 LSB/°/s)
        x = self.read_raw_data(GYRO_XOUT_H) / 131.0
        y = self.read_raw_data(GYRO_YOUT_H) / 131.0
        z = self.read_raw_data(GYRO_ZOUT_H) / 131.0
        return x, y, z
    
    def get_temp(self):
        """
        Get temperature in Celsius
        
        Returns:
            float: Temperature in °C
        """
        temp_raw = self.read_raw_data(TEMP_OUT_H)
        temp = (temp_raw / 340.0) + 36.53
        return temp
    
    def get_all_data(self):
        """
        Get all sensor data in one call
        
        Returns:
            dict: Dictionary containing all sensor readings
        """
        accel = self.get_accel_data()
        gyro = self.get_gyro_data()
        temp = self.get_temp()
        
        return {
            'accel': {'x': accel[0], 'y': accel[1], 'z': accel[2]},
            'gyro': {'x': gyro[0], 'y': gyro[1], 'z': gyro[2]},
            'temp': temp
        }
