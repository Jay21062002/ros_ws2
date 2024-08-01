import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Int32
from ipc_ros_wrapper.ipc_wrapper import write_data

class IpcSubscriber(Node):
    def __init__(self):
        super().__init__('ipc_subscriber')

        # Dictionary to map topics to their instance and chan_id
        self.topic_map = {
            '/telemetry_Cargo/cargo_door2_pin': {'instance': 0, 'chan_id': 1},
            '/telemetry_Cargo/cargo_door2_state': {'instance': 0, 'chan_id': 2},
            # Add more topics as needed
        }

        self.create_subscription(Int32, '/telemetry_Cargo/cargo_door2_pin', self.callback, 10)
        self.create_subscription(String, '/telemetry_Cargo/cargo_door2_state', self.callback, 10)

    def callback(self, msg):
        topic = msg._topic_name  # Get the topic name from the message

        if topic in self.topic_map:
            instance = self.topic_map[topic]['instance']
            chan_id = self.topic_map[topic]['chan_id']
            msg_data = str(msg.data)
            self.get_logger().info(f'Received on {topic}: {msg_data}')

            try:
                write_data(instance, chan_id, msg_data)
            except Exception as e:
                self.get_logger().error(f'Failed to write data to IPC for {topic}: {e}')
        else:
            self.get_logger().warn(f'No mapping found for topic: {topic}')

def main(args=None):
    rclpy.init(args=args)
    node = IpcSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

