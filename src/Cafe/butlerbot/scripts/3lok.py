#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from nav2_msgs.action import NavigateToPose
from rclpy.action import ActionClient
from action_msgs.msg import GoalStatus


class SimpleMover(Node):
    def __init__(self):
        super().__init__('simple_mover')
        self.action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        self.current_goal_done = False
        self.points = [
            ("Home", -2.96, 7.05, 0.0),
            ("Table 1", -9.84, -2.68, -0.707),
            ("Table 2", -18.06, -3.13, -0.707),
            ("Table 3", -18.27, 2.83, 0.707),
        ]
        self.move_through_points()

    def move_through_points(self):
        for name, x, y, z in self.points:
            self.get_logger().info(f"Moving to {name}")
            self.move_to_position(x, y, z)

    def move_to_position(self, x, y, z):
        self.current_goal_done = False
        goal_pose = NavigateToPose.Goal()
        goal_pose.pose.header.frame_id = 'map'
        goal_pose.pose.pose.position.x = x
        goal_pose.pose.pose.position.y = y
        goal_pose.pose.pose.orientation.z = z

        self.action_client.wait_for_server()
        send_goal_future = self.action_client.send_goal_async(
            goal_pose,
            feedback_callback=self.feedback_callback
        )
        send_goal_future.add_done_callback(self.goal_response_callback)
        rclpy.spin_until_future_complete(self, send_goal_future)

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        # Optional: log feedback
        # self.get_logger().info(f"Feedback: {feedback}")

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            self.current_goal_done = True
            return
        self.get_logger().info('Goal accepted')
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self._wait_for_result)

    def _wait_for_result(self, result_future):
        result = result_future.result()
        if result.status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info('Goal succeeded!')
        else:
            self.get_logger().info(f'Goal failed with status: {result.status}')
        self.current_goal_done = True


def main(args=None):
    rclpy.init(args=args)
    mover = SimpleMover()
    rclpy.shutdown()


if __name__ == '__main__':
    main()