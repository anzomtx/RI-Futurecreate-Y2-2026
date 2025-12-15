from machine import I2C, Pin
import time
from mpu6050 import MPU6050


def print_sensor_data(data):
    """
    Print formatted sensor data
    """
    print("\n" + "="*50)
    print("MPU6050 SENSOR DATA")
    print("="*50)
    print(f"Accelerometer:")
    print(f"  X: {data['accel']['x']:7.3f} g")
    print(f"  Y: {data['accel']['y']:7.3f} g") 
    print(f"  Z: {data['accel']['z']:7.3f} g")
    print(f"Gyroscope:")
    print(f"  X: {data['gyro']['x']:7.2f} °/s")
    print(f"  Y: {data['gyro']['y']:7.2f} °/s")
    print(f"  Z: {data['gyro']['z']:7.2f} °/s")
    print(f"Temperature: {data['temp']:6.2f} °C")
    print("="*50)


def main():
    """
    Main program loop
    """
    try:
        # Initialize I2C
        print("Initializing I2C communication...")
        i2c = I2C(0, sda=21, scl=22, freq=400000)
        
        # Initialize MPU6050
        print("Initializing MPU6050 sensor...")
        mpu = MPU6050(i2c)
        
        print("\nMPU6050 is ready! Starting data reading...")
        print("Press Ctrl+C to stop\n")
        
        # Main reading loop
        reading_count = 0
        while True:
            try:
                # Get all sensor data
                data = mpu.get_all_data()
                
                # Print data
                print_sensor_data(data)
                reading_count += 1
                print(f"Reading count: {reading_count}")
                
                # Wait before next reading
                time.sleep(2)
                
            except Exception as e:
                print(f"Error reading sensor data: {e}")
                time.sleep(1)
                
    except KeyboardInterrupt:
        print("\n\nProgram stopped by user")
    except Exception as e:
        print(f"\nFatal error: {e}")

# Run the main program
if __name__ == "__main__":
    main()
    
    
    

