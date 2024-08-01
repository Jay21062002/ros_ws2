from setuptools import setup

package_name = 'ipc_ros_wrapper'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='your_name',
    maintainer_email='your_email@example.com',
    description='IPC ROS Wrapper for IPC Communication',
    license='License',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'ipc_subscriber = ipc_ros_wrapper.subscriber:main',
            'dummy_publisher = ipc_ros_wrapper.dummy_publisher:main',
        ],
    },
)

