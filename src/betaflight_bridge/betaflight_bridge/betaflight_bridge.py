import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
import struct
import os
import time

FIFO_NAME = '/tmp/flight_controller_fifo'
TARGET_FREQ = 10000  # Hz
LOG_INTERVAL = 1  # Log every 1 second

class BetaflightBridge(Node):
    def __init__(self):
        super().__init__('betaflight_bridge')
        self.publisher_ = self.create_publisher(Imu, 'imu/data', 10)
        
        if not os.path.exists(FIFO_NAME):
            os.mkfifo(FIFO_NAME)

        print(f"Opening FIFO for reading: {FIFO_NAME}")
        self.fifo = open(FIFO_NAME, 'rb')
        
        self.timer = self.create_timer(1.0 / TARGET_FREQ, self.timer_callback)
        self.msg = Imu()
        self.msg.header.frame_id = "base_link"

        self.last_log_time = time.time()
        self.iterations = 0

    def timer_callback(self):
        try:
            data = self.fifo.read(12)
            if len(data) == 12:
                ax, ay, az = struct.unpack('<fff', data)
                
                self.msg.header.stamp = self.get_clock().now().to_msg()
                self.msg.linear_acceleration.x = ax
                self.msg.linear_acceleration.y = ay
                self.msg.linear_acceleration.z = az
                
                self.publisher_.publish(self.msg)
                
                self.iterations += 1
                current_time = time.time()
                if current_time - self.last_log_time >= LOG_INTERVAL:
                    self.get_logger().info(f"Bridge: Published {self.iterations} messages in the last {LOG_INTERVAL} second(s). Last values: ax={ax:.2f}, ay={ay:.2f}, az={az:.2f}")
                    self.last_log_time = current_time
                    self.iterations = 0
                
        except Exception as e:
            self.get_logger().error(f'Error reading from FIFO: {e}')

    def __del__(self):
        if hasattr(self, 'fifo'):
            self.fifo.close()

def main(args=None):
    rclpy.init(args=args)
    betaflight_bridge = BetaflightBridge()
    rclpy.spin(betaflight_bridge)
    betaflight_bridge.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()