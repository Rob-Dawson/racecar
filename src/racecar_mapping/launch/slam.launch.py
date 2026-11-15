from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    lifecycle_nodes = ["map_saver_server", "slam_toolbox"]
    mapping_dir = FindPackageShare("racecar_mapping")

    use_sim_time_arg = DeclareLaunchArgument("use_sim_time", default_value="true")

    slam_config_arg = DeclareLaunchArgument(
        "slam_config",
        default_value=PathJoinSubstitution(
            [mapping_dir, "config", "slam_toolbox.yaml"]
        ),
    )

    slam_config = LaunchConfiguration("slam_config")
    use_sim_time = LaunchConfiguration("use_sim_time")

    slam_toolbox = Node(
        package="slam_toolbox",
        executable="sync_slam_toolbox_node",
        name="slam_toolbox",
        output="screen",
        parameters=[slam_config, {"use_sim_time": use_sim_time}],
    )

    nav2_map_saver = Node(
        package="nav2_map_server",
        executable="map_saver_server",
        name="map_saver_server",
        output="screen",
        parameters=[
            {"save_map_timeout": 5.0},
            {"use_sim_time": use_sim_time},
            {"free_thresh_default": 0.196},
            {"occupied_thresh_default": 0.65},
        ],
    )

    nav2_lifecycle_manager = Node(
        package="nav2_lifecycle_manager",
        executable="lifecycle_manager",
        name="lifecycle_manager",
        output="screen",
        parameters=[
            {"node_names": lifecycle_nodes},
            {"autostart": True},
            {"use_sim_time": use_sim_time},
        ],
    )

    ld = LaunchDescription()

    ld.add_action(use_sim_time_arg)
    ld.add_action(slam_config_arg)
    ld.add_action(slam_toolbox)
    ld.add_action(nav2_map_saver)
    ld.add_action(nav2_lifecycle_manager)

    return ld
