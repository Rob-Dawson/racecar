from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    lifecycle_nodes = ["controller_server"]

    controller_dir = FindPackageShare("racecar_motion_controller")

    use_sim_time_arg = DeclareLaunchArgument(
        "use_sim_time",
        default_value="true",
    )

    controller_config_arg = DeclareLaunchArgument(
        "controller_config",
        default_value=PathJoinSubstitution([controller_dir, "config", "controller.yaml"]),
    )

    local_costmap_config_arg = DeclareLaunchArgument(
        "local_costmap_config",
        default_value=PathJoinSubstitution([controller_dir, "config", "local_costmap.yaml"]),
    )

    controller_config = LaunchConfiguration("controller_config")
    local_costmap_config = LaunchConfiguration("local_costmap_config")

    use_sim_time = LaunchConfiguration("use_sim_time")

    controller_server = Node(
        package="nav2_controller",
        executable="controller_server",
        name="controller_server",
        output="screen",
        parameters=[
            controller_config,
            local_costmap_config,
            {"use_sim_time": use_sim_time},
        ],
    )

    nav2_lifecycle_manager = Node(
        package="nav2_lifecycle_manager",
        executable="lifecycle_manager",
        name="lifecycle_manager_motion_control",
        output="screen",
        parameters=[
            {
                "node_names": lifecycle_nodes,
                "autostart": True,
                "use_sim_time": use_sim_time,
            }
        ],
    )

    twist_bridge = Node(
        package="racecar_control",
        executable="twist_to_twist_stamped.py",
        name="twist_to_twist_stamped",
        output="screen",
        parameters=[{"use_sim_time": use_sim_time}],
    )
    ld = LaunchDescription()

    ld.add_action(use_sim_time_arg)
    ld.add_action(controller_config_arg)
    ld.add_action(local_costmap_config_arg)
    ld.add_action(controller_server)
    ld.add_action(nav2_lifecycle_manager)
    ld.add_action(twist_bridge)

    return ld
