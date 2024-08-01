import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Int32

class DummyPublisher(Node):
    def __init__(self):
        super().__init__('dummy_publisher')
        self.publisher1 = self.create_publisher(Int32, '/telemetry_Cargo/cargo_door2_pin', 10)
        self.publisher2 = self.create_publisher(String, '/telemetry_Cargo/cargo_door2_state', 10)

        timer_period = 1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg1 = Int32()
        msg1.data = self.i
        self.publisher1.publish(msg1)

        msg2 = String()
        msg2.data = f'State {self.i}'
        self.publisher2.publish(msg2)

        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    node = DummyPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

