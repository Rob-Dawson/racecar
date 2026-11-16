from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    sim_mode_arg = DeclareLaunchArgument(
        "sim_mode",
        default_value="false",
        description="Enable sim specific robot config",
    )
    sim_mode = LaunchConfiguration("sim_mode")

    use_ros2_control_arg = DeclareLaunchArgument(
        "use_ros2_control",
        default_value="true",
        description="Use ros2_control if true",
    )

    use_ros2_control = LaunchConfiguration("use_ros2_control")

    # Process the URDF file
    racecar_description_dir = FindPackageShare("racecar_description")

    xacro_file = PathJoinSubstitution([racecar_description_dir, "urdf", "racecar.xacro"])
    robot_description_config = Command(
        [
            "xacro ",
            xacro_file,
            " use_ros2_control:=",
            use_ros2_control,
            " sim_mode:=",
            sim_mode,
        ]
    )

    # Create a robot_state_publisher node
    rsp_params = {
        "robot_description": ParameterValue(robot_description_config, value_type=str),
        "use_sim_time": ParameterValue(sim_mode, value_type=bool),
    }
    node_robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[rsp_params],
    )

    # Launch!
    ld = LaunchDescription()
    ld.add_action(sim_mode_arg)
    ld.add_action(use_ros2_control_arg)
    ld.add_action(node_robot_state_publisher)

    return ld
