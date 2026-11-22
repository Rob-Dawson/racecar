#!/usr/bin/env python3

import rclpy
from geometry_msgs.msg import PoseStamped
from nav2_msgs.action import ComputePathToPose
from nav_msgs.msg import Path
from rclpy.action import ActionClient
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, QoSProfile, ReliabilityPolicy


class GoalToPlanner(Node):
    def __init__(self):
        super().__init__("goal_to_planner")

        self.goal_subscriber = self.create_subscription(
            PoseStamped,
            "/goal_pose",
            self.goal_callback,
            10,
        )

        path_qos = QoSProfile(
            depth=1,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
            reliability=ReliabilityPolicy.RELIABLE,
        )

        self.path_publisher = self.create_publisher(
            Path,
            "/plan",
            path_qos,
        )

        self.planner_client = ActionClient(
            self,
            ComputePathToPose,
            "/compute_path_to_pose",
        )

        self.request_id = 0

        self.get_logger().info("Goal-to-planner adapter ready. Select a goal in RViz.")

    def goal_callback(self, goal_pose):
        self.request_id += 1
        request_id = self.request_id

        self.get_logger().info(
            f"Planning to x={goal_pose.pose.position.x:.2f}, y={goal_pose.pose.position.y:.2f}"
        )

        # Remove the previous path from RViz.
        empty_path = Path()
        empty_path.header.frame_id = "map"
        empty_path.header.stamp = self.get_clock().now().to_msg()
        self.path_publisher.publish(empty_path)

        if not self.planner_client.server_is_ready():
            self.get_logger().warn("Planner Server is not available.")
            return

        goal = ComputePathToPose.Goal()
        goal.goal = goal_pose
        goal.planner_id = "GridBased"
        goal.use_start = False

        future = self.planner_client.send_goal_async(goal)
        future.add_done_callback(lambda future: self.goal_response_callback(future, request_id))

    def goal_response_callback(self, future, request_id):
        try:
            goal_handle = future.result()
        except Exception as exc:
            self.get_logger().error(f"Failed to send planning goal: {exc}")
            return

        if not goal_handle.accepted:
            self.get_logger().warn("Planning goal rejected.")
            return

        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(lambda future: self.result_callback(future, request_id))

    def result_callback(self, future, request_id):
        try:
            response = future.result()
        except Exception as exc:
            self.get_logger().error(f"Planning action failed: {exc}")
            return

        # Ignore results from older requests.
        if request_id != self.request_id:
            return

        path = response.result.path

        if not path.poses:
            self.get_logger().warn("Planner returned an empty path.")
            return

        self.path_publisher.publish(path)

        self.get_logger().info(f"Published planned path containing {len(path.poses)} poses.")


def main(args=None):
    rclpy.init(args=args)

    node = GoalToPlanner()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
