from neuromeka import IndyDCP3
import time

JOINT_MIN = [-180, -90, -120, -120, -180, -180]  # Minimum angles for each joint
JOINT_MAX = [180, 90, 120, 120, 180, 180]        # Maximum angles for each joint

def cap_joint_positions(jtarget):
    """
    Constrain the joint positions to be within the defined joint limits.
    
    Parameters:
    - jtarget: List of target joint positions [j1, j2, j3, j4, j5, j6]
    
    Returns:
    - Constrained joint positions
    """
    return [max(JOINT_MIN[i], min(jtarget[i], JOINT_MAX[i])) for i in range(len(jtarget))]





class CobotWrapper(IndyDCP3):
    def __init__(self, ip_addr: str):
        super().__init__(ip_addr)

    def move_home(self):
        self.movej([0, 0, -90, 0, -90, 0])

    def move_upright(self):
        # Retrieve current joint positions
        current_positions = self.get_control_state()["q"]
        print("Current positions:", current_positions)

        # Modify specific joints based on the third joint position
        new_positions = current_positions[:]
        if current_positions[2] < 0:
            new_positions[2] = -90 - current_positions[1]
            new_positions[3] = -90
        else:
            new_positions[2] = 90 - current_positions[1]
            new_positions[3] = 90

        # Move the robot to the new joint positions
        self.movej(new_positions)

        # Retrieve and print the list of new placements of all 6 joints
        # updated_positions = self.get_control_state()["q"]
        print("Updated positions:", new_positions)

        time.sleep(1)


    def sweep(self):
        # Cannot exceed -360 and 360
        positions = self.get_control_state()["q"]
        print(positions[4])
        if positions[4] < 0:
            print(positions[4])
            positions[4] += 360
            print(positions[4])
        else:
            print(positions[4])
            positions[4] -= 360
            print(positions[4])
        self.movej(positions)


    def turn_right(self):
        positions = self.get_control_state()["q"]
        print("Current positions:", positions)

        positions[0] -= 90
        self.movej(positions)
        print("Updated positions:", positions)


    def turn_left(self):
        positions = self.get_control_state()["q"]
        print("Current positions:", positions)

        positions[0] += 90
        self.movej(positions)
        print("Updated positions:", positions)


    def move_forward(self):
        positions = self.get_control_state()["q"]
        positions[1] -= 20

        self.movej(positions)
        print("Updated positions:", positions)


    def move_backward(self):
        positions = self.get_control_state()["q"]
        positions[1] += 20
        print(positions[1])

        self.movej(positions)
        print("Updated positions:", positions)


if __name__ == "__main__":
    ip_addr = "192.168.8.136"
    indy = CobotWrapper(ip_addr)

    # indy.move_home()

    indy.move_upright()

    # indy.sweep()
    
    # indy.turn_right()
    # indy.turn_left()

    # indy.move_forward()
    # indy.move_backward()

    # print(indy.get_control_state()["q"])