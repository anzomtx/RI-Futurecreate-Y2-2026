# 1. import statements
from mpu6050_lib import MPU6050
from machine import Pin
from time import sleep_ms

# 2. functions and variables 
mpu = MPU6050()
    
    
# 3. main loop
while True:
    # Accelerometer Data
    accel = mpu.read_accel_data() # read the accelerometer [ms^-2]
    aX = accel["x"]
    aY = accel["y"]
    aZ = accel["z"]
    #print("x: " + str(aX) + " y: " + str(aY) + " z: " + str(aZ))

    # Gyroscope Data
    gyro = mpu.read_gyro_data()   # read the gyro [deg/s]
    gX = gyro["x"]
    gY = gyro["y"]
    gZ = gyro["z"]
    print("x:" + str(gX) + " y:" + str(gY) + " z:" + str(gZ))

    # Rough Temperature
    temp = mpu.read_temperature()   # read the device temperature [degC]
    # print("Temperature: " + str(temp) + "°C")

    # G-Force
    # gforce = mpu.read_accel_abs(g=True) # read the absolute acceleration magnitude
    # print("G-Force: " + str(gforce))

    
    # Time Interval Delay in millisecond (ms)
    sleep_ms(100)
