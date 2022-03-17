from djitellopy import Tello



class TelloGestureController:
    def __init__(self, tello: Tello):
        self.tello = tello
        self._is_landing = False

        # RC control velocities
        self.forw_back_velocity = 0
        self.up_down_velocity = 0
        self.left_right_velocity = 0
        self.yaw_velocity = 0

    def gesture_control(self, gesture_buffer):
        cnt= gesture_buffer.get_gesture()
        print("GESTURE", cnt)

        if not self._is_landing:
            if cnt == 0:  # Forward
                self.forw_back_velocity = 30
            elif cnt == 1:  # STOP
                self.forw_back_velocity = self.up_down_velocity = \
                    self.left_right_velocity = self.yaw_velocity = 0
            if cnt == 5:  # Back
                self.forw_back_velocity = -30

            elif cnt == 2:  # UP
                self.up_down_velocity = 25
            elif cnt == 4:  # DOWN
                self.up_down_velocity = -25

            elif cnt == 3:  # LAND
                self._is_landing = True
                self.forw_back_velocity = self.up_down_velocity = \
                    self.left_right_velocity = self.yaw_velocity = 0
                self.tello.land()

            elif cnt == 6: # LEFT
                self.left_right_velocity = 20
            elif cnt == 7: # RIGHT
                self.left_right_velocity = -20

            elif cnt == -1:
                self.forw_back_velocity = self.up_down_velocity = \
                    self.left_right_velocity = self.yaw_velocity = 0

            self.tello.send_rc_control(self.left_right_velocity, self.forw_back_velocity,
                                       self.up_down_velocity, self.yaw_velocity)