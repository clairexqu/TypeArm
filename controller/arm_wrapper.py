import time
from typing import Tuple

import sys
import cv2
sys.path.append('..')
from HikrobotCamera.hik_camera import HikCamera
from gripper import Gripper

from neuromeka import IndyDCP3
from .abs.robot_wrapper import RobotWrapper


def _cap_z(move_distance, height):
    MIN_Z = 140
    if height - move_distance < MIN_Z:
        print("Arm cannot move below 14 cm from the table.")
        return height - MIN_Z
    return move_distance

class ArmFrame:
    def __init__(self, cap):
        self.cap = cap

    @property
    def frame(self):
        img = self.cap.get_frame_reader()
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

class ArmWrapper(RobotWrapper):
    def __init__(self):
        self.ip_addr = "192.168.8.136"
        self.indy = None
        self.stream_on = False
        self.camera = HikCamera()
        self.gripper = Gripper()

    def keep_active(self):
        pass

    def connect(self):
        self.indy = IndyDCP3(self.ip_addr)

    def takeoff(self) -> bool:
        return True

    def land(self):
        pass

    def start_stream(self):
        self.camera.start_stream()
        self.stream_on = True

    def stop_stream(self):
        self.camera.stop_stream()
        self.stream_on = False

    def get_frame_reader(self):
        if not self.stream_on:
            return None
        frame = ArmFrame(self.camera)
        return frame

    def move_robot(self, distance: int, axis: int):
        # Retrieve the current workspace position
        current_pos = self.indy.get_control_state()['p']
        print("Current position:", current_pos)

        # Adjust the Z-axis position by the specified distance
        new_pos = current_pos[:]
        new_pos[axis] += distance

        # Move the robot to the new position
        self.indy.movel(new_pos)

        # Wait for the movement to complete
        sleep_time = (abs(distance) / 100) + 1
        time.sleep(sleep_time)

        # Print the updated position
        print("Updated position:", new_pos)
        return True, False
    
    def move_forward(self, distance: int) -> Tuple[bool, bool]:
        print(f"-> Moving forward {distance} mm")
        return self.move_robot(distance, 0)
        
    def move_backward(self, distance: int) -> Tuple[bool, bool]:
        print(f"-> Moving back {distance} mm")
        return self.move_robot(-distance, 0)

    def move_left(self, distance: int) -> Tuple[bool, bool]:
        print(f"-> Moving left {distance} mm")
        return self.move_robot(distance, 1)

    def move_right(self, distance: int) -> Tuple[bool, bool]:
        print(f"-> Moving right {distance} mm")
        return self.move_robot(-distance, 1)

    def move_up(self, distance: int) -> Tuple[bool, bool]:
        print(f"-> Moving up {distance} mm")
        return self.move_robot(distance, 2)

    def move_down(self, distance: int) -> Tuple[bool, bool]:
        current_pos = self.indy.get_control_state()['p']
        safe_distance = _cap_z(distance, current_pos[2])
        print(f"-> Moving down {safe_distance} mm")
        return self.move_robot(-safe_distance, 2)
    
    def down_distance(self)-> Tuple[int, bool]:
        current_pos = self.indy.get_control_state()['p']
        height = int(current_pos[2])
        if height > 400:
            return height - 400, False
        elif height <= 400:
            print("Cannot move down further.")
            return 0, False
        
    def up_distance(self) -> Tuple[int, bool]:
        current_pos = self.indy.get_control_state()['p']
        height = int(current_pos[2])
        if height < 647:
            return 647 - height, False
        elif height >= 647:
            print("Cannot move up further.")
            return 0, False
        
    def x_distance(self, current_x: float) -> Tuple[int, bool]:
        target_x = 0.5
        tolerance = 0.025  # Tolerance around the target position
                
        if current_x < target_x - tolerance or current_x > target_x + tolerance:
            distance = int((target_x - current_x) / 0.001)
            return distance, False
        else:
            # No movement needed
            return 0, False
        
    def y_distance(self, current_y: float) -> Tuple[int, bool]:
        target_y = 0.5
        tolerance = 0.025  # Tolerance around the target position
        
        if current_y < target_y - tolerance or current_y > target_y + tolerance:
            distance = int((target_y - current_y) / 0.001)
            return distance, False
        else:
            # No movement needed
            return 0, False

    def turn_ccw(self, degree: int) -> Tuple[bool, bool]:
        print(f"-> Turning CCW {degree} degrees")

        current_positions = self.indy.get_control_state()["q"]
        print("Current positions:", current_positions)

        # Modify the first joint for counter-clockwise rotation
        current_positions[0] += degree
        self.indy.movej(current_positions)

        # Wait for the movement to complete
        time.sleep(degree/20)

        # Print the updated positions
        print("Updated positions:", current_positions)
        return True, False

    def turn_cw(self, degree: int) -> Tuple[bool, bool]:
        print(f"-> Turning CW {degree} degrees")

        current_positions = self.indy.get_control_state()["q"]
        print("Current positions:", current_positions)

        # Modify the first joint for clockwise rotation
        current_positions[0] -= degree
        self.indy.movej(current_positions)

        # Wait for the movement to complete
        time.sleep(degree/20)

        # Print the updated positions
        print("Updated positions:", current_positions)
        return True, False
    
    def reset_position(self) -> Tuple[bool, bool]:
        print("-> Moving home")
        self.indy.movej([0, 0, -90, 0, -90, -90])
        self.open_gripper()

        time.sleep(1)
        return True, False

    def face_upright(self) -> Tuple[bool, bool]:
        print("-> Moving upright")

        # Retrieve current joint positions
        current_positions = self.indy.get_control_state()["q"]
        print("Current positions:", current_positions)

        # Modify specific joints based on the third joint position
        new_positions = current_positions[:]
        if current_positions[2] < 0:
            new_positions[2] = -90 - current_positions[1]
            new_positions[3] = -90
        else:
            new_positions[2] = 90 - current_positions[1]
            new_positions[3] = 90

        new_positions[5] = 0

        # Move the robot to the new joint positions
        self.indy.movej(new_positions)
        time.sleep(1)

        # Retrieve and print the list of new placements of all 6 joints
        print("Updated positions:", new_positions)
        return True, False
    
    def move_in_circle(self, cw) -> Tuple[bool, bool]:
        pass

    def open_gripper(self) -> Tuple[bool, bool]:
        self.gripper.open()
        return True, False

    def close_gripper(self) -> Tuple[bool, bool]:
        self.gripper.close()
        time.sleep(4)
        return True, False
