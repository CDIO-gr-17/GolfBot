import math
import time
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait
from Heading import Heading

def calculate_heading(current_position, next_position):
    dx = next_position[0] - current_position[0]
    dy = next_position[1] - current_position[1]

    # Calculate the heading in degrees
    heading = math.degrees(math.atan2(dy, dx))

    # Normalize the heading to be between 0 and 359
    heading = (heading + 360) % 360

    return heading

class Robot:
    # Initialize the EV3 Brick.
    def __init__(self):
        self.ev3 = EV3Brick()

        # Initialize the motors.
        self.left_motor = Motor(Port.D)
        self.right_motor = Motor(Port.A)
        self.front_motor = Motor(Port.C)

        # Initialize the drive base.
        self.WHEEL_DIAMETER = 55
        self.AXLE_TRACK = 110
        self.robot = DriveBase(self.left_motor, self.right_motor, self.WHEEL_DIAMETER, self.AXLE_TRACK)  # noqa: E501

        self.GRID_DISTANCE = 7.5
        self.current_heading = None
        self.step = 0

    def turn(self, degrees):
        self.robot.turn(degrees)
        self.current_heading = (self.current_heading + degrees) % 360
        print('turned ' + str(degrees) + ' degrees')

    def shortest_turn(self, current_degrees, target_degrees):
        delta = (target_degrees - current_degrees) % 360
        print('The calculated delta is: ' + str(delta))
        if delta > 180:
            delta -= 360
        return delta

    def turn_to_heading(self, target_heading):
        turn_degrees = self.shortest_turn(self.current_heading, target_heading)
        self.turn(turn_degrees)
        return target_heading

    def moveForward(self, distance):
        self.robot.straight(distance)


    def moveBackward(self):
        self.robot.straight(-100)

    #Either we want to wiggle the robot to make it stay more in one place
    #Or we want it to move back to goal after each ball
    def shoot_one_ball(self, distance):
        self.front_motor.run(-1200)
        self.robot.straight(-distance)
        wait(2000)
        self.robot.straight(distance)
        wait(2000)

    def shoot_all_balls(self):
        self.robot.settings(100, 200)
        wiggle = 40
        for i in range(3):
            self.shoot_one_ball(wiggle)
            wiggle += 40
        self.front_motor.stop()

    def pickup_ball(self, distance):
        self.front_motor.run(1200)
        wait(2000)
        self.robot.settings(100, 200)
        self.robot.straight(distance * self.GRID_DISTANCE*1.2)
        self.front_motor.stop()

    def deposit(self):
        goal_heading = 90 #directly east
    #Send command containing the following:
        self.turn_to_heading(goal_heading)
        self.shoot_all_balls()

    # def playWeAreTheChampions(self):
    # # Define the notes and durations (in ms) for "We Are The Champions"
    # # 90 BPM = 666.67 ms per beat in 6/8 time (111.11 ms per eighth note)
    #     tempo = 90
    #     eighth_note_duration = 60000 / tempo / 3  # duration of an eighth note

    # # Notes and durations based on the sheet music
    #     melody = [
    #         ('F4', 1.5 * eighth_note_duration), ('E4', 0.5 * eighth_note_duration), ('F4', eighth_note_duration),
    #         ('E4', eighth_note_duration), ('C4', 1.5 * eighth_note_duration), ('A4', 0.5 * eighth_note_duration),
    #         ('D4', eighth_note_duration), ('A4', eighth_note_duration), ('C4', eighth_note_duration),
    #         ('F4', 2 * eighth_note_duration), ('G4', 0.5 * eighth_note_duration), ('A4', 1.5 * eighth_note_duration),
    #         ('B4', eighth_note_duration), ('C4', eighth_note_duration), ('D4', eighth_note_duration),
    #         ('B4', eighth_note_duration), ('G4', 2 * eighth_note_duration), ('A4', eighth_note_duration),
    #         ('B4', 2 * eighth_note_duration), ('G4', 2 * eighth_note_duration), ('C4', eighth_note_duration),
    #         ('B4', eighth_note_duration), ('A4', eighth_note_duration), ('G4', eighth_note_duration),
    #         ('E4', eighth_note_duration), ('G4', eighth_note_duration), ('D4', eighth_note_duration),
    #         ('C5', eighth_note_duration), ('B4', 2 * eighth_note_duration), ('A4', 1.5 * eighth_note_duration),
    #         ('G4', 0.5 * eighth_note_duration), ('E4', eighth_note_duration), ('D4', eighth_note_duration),
    #         ('G4', eighth_note_duration), ('A4', eighth_note_duration), ('B4', eighth_note_duration),
    #         ('G4', 2 * eighth_note_duration)
    #     ]

    #     for note, duration in melody:
    #         self.ev3.speaker.beep(note, duration)
    #         wait(duration * 0.1)  # Short pause between notes

    def test_speaker(self):
        self.ev3.speaker.beep(frequency=440, duration=1000)  # Play a 440 Hz tone for 1000 ms (1 second)
        wait(1000)  # Wait for 1 second to hear the beep

    def move_robot_smoothly(self, path, heading, controller):
        i = 0
        while i < len(path) - 1:
            current_position = path[i]
            next_position = path[i + 1]

            # Calculate the necessary heading to move to the next position
            necessary_heading = calculate_heading(current_position, next_position)

            # If the necessary heading is the same as the current heading, count the number of consecutive cells with the same heading
            if necessary_heading == heading:
                steps = 1
                while i + steps < len(path) - 1 or steps < 20:
                    next_next_position = path[i + steps + 1]
                    next_necessary_heading = calculate_heading(next_position, next_next_position)
                    if next_necessary_heading == necessary_heading:
                        steps += 1
                        next_position = next_next_position
                    else:
                        break

                if necessary_heading % 90 != 0:            # Given we only can turn 45 degrees
                    distance = steps*self.GRID_DISTANCE*1.41421356
                else:
                    distance = steps*self.GRID_DISTANCE

                # Move the robot forward by the number of steps
                self.moveForward(distance)
                i += steps
                print('step++:', steps, "moved forward a lot")
            else:
                # Calculate the difference in heading
                heading_difference = self.shortest_turn(necessary_heading, heading)

                # Turn the robot to the necessary heading
                self.turn(heading_difference)

                if necessary_heading % 90 != 0:            # Given we only can turn 45 degrees
                    distance = self.GRID_DISTANCE*1.41421356
                else:
                    distance = self.GRID_DISTANCE

                # Move the robot forward
                self.moveForward(distance)

                i += 1
                print("moved forward")

            buffer = ""
            data = controller.recieve_command()
            if data:
                buffer += data
                while "\n" in buffer:
                    command, buffer = buffer.split("\n", 1)
                    if command == 'ABORT':
                        return

            # Update the current heading
            heading = necessary_heading
            self.current_heading = heading






