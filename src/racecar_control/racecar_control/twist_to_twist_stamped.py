#!/usr/bin/env python3

import rclpy
from geometry_msgs.msg import Twist, TwistStamped
from rclpy.node import Node


class TwistToTwistStamped(Node):
    def __init__(self):
        super().__init__("twist_to_twist_stamped")

        self.publisher = self.create_publisher(
            TwistStamped,
            "/ackermann_steering_controller/reference",
            10,
        )

        self.subscription = self.create_subscription(
            Twist,
            "/cmd_vel",
            self.cmd_vel_callback,
            10,
        )

        self.get_logger().info("Twist-to-TwistStamped bridge ready.")

    def cmd_vel_callback(self, msg):
        stamped_msg = TwistStamped()

        stamped_msg.header.stamp = self.get_clock().now().to_msg()
        stamped_msg.header.frame_id = "base_link"

        stamped_msg.twist = msg

        self.publisher.publish(stamped_msg)


def main(args=None):
    rclpy.init(args=args)

    node = TwistToTwistStamped()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
