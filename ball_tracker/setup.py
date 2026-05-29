from setuptools import find_packages, setup

package_name = 'ball_tracker'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Erdem Ozkan',
    maintainer_email='erdemzkn7@gmail.com',
    description='Ball tracking with pan-tilt head',
    license='MIT',
    entry_points={
        'console_scripts': [
            'ball_tracker_node = ball_tracker.ball_tracker_node:main',
        ],
    },
)
