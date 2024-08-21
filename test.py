import sys
sys.path.append('..')
from HikrobotCamera.hik_camera import HikCamera
import cv2

from controller.arm_wrapper import ArmWrapper

if __name__ == "__main__":
    arm = ArmWrapper()
    arm.connect()
    # arm.start_stream()
    
    # while True:
    #     frame = arm.camera.get_frame_reader()
    #     if frame is not None:
    #         print(frame.shape)
    #         cv2.imshow('frame', frame)
    #         if cv2.waitKey(1) & 0xFF == ord('q'):
    #             break

    # arm.reset_position()

    # arm.move_backward(80)
    # arm.move_down(50)
    # arm.turn_ccw(50)
    # arm.move_right(-50)
    # arm.move_upright()
    # arm.move_backward(50)

    # current_positions = arm.indy.get_control_state()["q"]
    # print("Current positions:", current_positions)

    arm.close_gripper()