from setuptools import setup

package_name = 'betaflight_bridge'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='your.email@example.com',
    description='Betaflight to ROS2 bridge',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'betaflight_bridge = betaflight_bridge.betaflight_bridge:main',
            'mock_flight_controller = betaflight_bridge.mock_flight_controller:main',
        ],
    },
)