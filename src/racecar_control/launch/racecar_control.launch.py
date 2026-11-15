from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    controller_manager_arg = DeclareLaunchArgument(
        "controller_manager",
        default_value="/controller_manager",
        description="Controller manager to connect to",
    )

    controller_manager = LaunchConfiguration("controller_manager")

    joint_state_broadcaster = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager",
            controller_manager,
            "--controller-manager-timeout",
            "60",
        ],
        output="screen",
    )

    ackermann_steering_controller = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "ackermann_steering_controller",
            "--controller-manager",
            controller_manager,
            "--controller-manager-timeout",
            "60",
        ],
        output="screen",
    )
    ld = LaunchDescription()

    ld.add_action(controller_manager_arg)
    ld.add_action(ackermann_steering_controller)
    ld.add_action(joint_state_broadcaster)

    return ld
