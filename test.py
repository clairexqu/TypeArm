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
        pass

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

        # Print the new target positions
        # print("New target positions:", new_positions)

        # Move the robot to the new joint positions
        self.movej(new_positions)

        # Retrieve and print the list of new placements of all 6 joints
        updated_positions = self.get_control_state()["q"]
        print("Updated positions:", updated_positions)




if __name__ == "__main__":
    ip_addr = "192.168.8.136"
    indy = CobotWrapper(ip_addr)

    indy.move_upright()
    
    

    # # Home position
    # indy.movej([0, 0, -90, 0, -90, -0])
