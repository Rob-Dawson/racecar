from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    use_sim_time_arg = DeclareLaunchArgument("use_sim_time", default_value="true")
    use_sim_time = LaunchConfiguration("use_sim_time")

    racecar_state_estimation_dir = FindPackageShare("racecar_state_estimation")

    robot_localization_ekf = Node(
        package="robot_localization",
        executable="ekf_node",
        name="ekf_filter_node",
        output="screen",
        parameters=[
            PathJoinSubstitution([racecar_state_estimation_dir, "config", "ekf.yaml"]),
            {"use_sim_time": use_sim_time},
        ],
        remappings=[("/odometry/filtered", "/odometry/filtered_ekf")],
    )

    ld = LaunchDescription()
    ld.add_action(use_sim_time_arg)
    ld.add_action(robot_localization_ekf)
    return ld
