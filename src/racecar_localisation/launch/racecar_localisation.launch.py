from pathlib import Path

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo, OpaqueFunction
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def launch_localisation(context):
    map_name = LaunchConfiguration("map_name").perform(context)
    use_sim_time = LaunchConfiguration("use_sim_time")
    amcl_config = LaunchConfiguration("amcl_config")

    racecar_mapping_dir = Path(FindPackageShare("racecar_mapping").perform(context))
    racecar_map_path = racecar_mapping_dir / "maps" / map_name / "warehouse.yaml"

    if not racecar_map_path.is_file():
        return [
            LogInfo(
                msg=f"Map {map_name} not found at {racecar_map_path}"
                "Please create a map before starting localisation"
            )
        ]

    lifecycle_nodes = ["map_server", "amcl"]

    nav2_map_server = Node(
        package="nav2_map_server",
        executable="map_server",
        output="screen",
        parameters=[{"yaml_filename": str(racecar_map_path)}, {"use_sim_time": use_sim_time}],
    )

    nav2_amcl = Node(
        package="nav2_amcl",
        executable="amcl",
        name="amcl",
        output="screen",
        parameters=[amcl_config, {"use_sim_time": use_sim_time}],
    )

    nav2_lifecycle_manager = Node(
        package="nav2_lifecycle_manager",
        executable="lifecycle_manager",
        name="lifecycle_manger_localisation",
        output="screen",
        parameters=[
            {"node_names": lifecycle_nodes},
            {"autostart": True},
            {"use_sim_time": use_sim_time},
        ],
    )

    return [nav2_map_server, nav2_amcl, nav2_lifecycle_manager]


def generate_launch_description():
    racecar_localisation_dir = FindPackageShare("racecar_localisation")

    use_sim_time_arg = DeclareLaunchArgument("use_sim_time", default_value="true")

    amcl_config_arg = DeclareLaunchArgument(
        "amcl_config",
        default_value=PathJoinSubstitution([racecar_localisation_dir, "config", "amcl.yaml"]),
    )

    map_name_arg = DeclareLaunchArgument("map_name", default_value="warehouse")

    ld = LaunchDescription()
    ld.add_action(map_name_arg)
    ld.add_action(use_sim_time_arg)
    ld.add_action(amcl_config_arg)
    ld.add_action(OpaqueFunction(function=launch_localisation))
    return ld
