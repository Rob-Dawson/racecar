from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import (
    LaunchConfiguration,
    PathJoinSubstitution,
    PythonExpression,
)
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    racecar_bringup_dir = FindPackageShare("racecar_bringup")
    racecar_control_dir = FindPackageShare("racecar_control")
    racecar_localisation_dir = FindPackageShare("racecar_localisation")
    environment_arg = DeclareLaunchArgument(
        "environment",
        default_value="gazebo",
        # choices=["gazebo", "isaacsim", "realrobot"],
        description="Select the execution environment",
    )
    environment = LaunchConfiguration("environment")
    sim_mode = PythonExpression(
        [
            "'true' if '",
            environment,
            "' == 'gazebo' else 'false'",
        ]
        # [
        #     "'true' if '",
        #     environment,
        #     "' in ['gazebo', 'isaacsim'] else 'false'",
        # ]
    )
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([racecar_bringup_dir, "launch", "rsp.launch.py"])
        ),
        launch_arguments={
            "sim_mode": sim_mode,
        }.items(),
    )

    is_gazebo = IfCondition(PythonExpression(["'", environment, "' == 'gazebo'"]))
    ###
    # This is here ready for when the real robot or issac sim are implemented
    # is_issacsim = IfCondition(PythonExpression(["'", environment, "' == 'issacsim'"]))
    # is_realrobot = IfCondition(PythonExpression(["'", environment, "' == 'realrobot'"]))
    ###
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([racecar_bringup_dir, "launch", "gazebo.launch.py"])
        ),
        condition=is_gazebo,
    )

    racecar_control = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [racecar_control_dir, "launch", "racecar_control.launch.py"]
            )
        ),
        condition=is_gazebo,
    )

    racecar_localisation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [racecar_localisation_dir, "launch", "racecar_localisation.launch.py"]
            )
        )
    )

    ld = LaunchDescription()
    ld.add_action(environment_arg)
    ld.add_action(rsp)
    ld.add_action(gazebo)
    ld.add_action(racecar_control)

    return ld
