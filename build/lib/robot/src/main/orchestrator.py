from pip._vendor.distlib.compat import raw_input

from robot.src.main.movement import Movement
from robot.src.main.rotation import Rotation
from robot.src.main.placement import Placement
from robot.src.main.inputs import Inputs
from robot.src.exceptions.start_exception import StartException


class Orchestrator(object):

    def __init__(self):
        self.movement = Movement()
        self.placement = Placement()
        self.rotation = Rotation()
        self.inout = Inputs()

    def place_robot(self, desired_pos):
        return self.placement.place(desired_pos)

    def move_robot(self, current_pos):
        return self.movement.move(current_pos)

    def rotate_robot(self, direc, current_pos):
        return self.rotation.rotate(direc, current_pos)

    def treat_inputs(self, inp):
        return self.inout.treat_inputs(inp)

    # Method to execute the actions
    def execute_command(self, cmd, current_pos):
        try:
            if cmd['cmd'] == 'PLACE':
                new_pos = self.place_robot(cmd)
            elif cmd['cmd'] == 'MOVE':
                new_pos = self.move_robot(current_pos)
            elif cmd['cmd'] == 'LEFT':
                new_pos = self.rotate_robot(
                    {"direc": "LEFT"}, current_pos)
            elif cmd['cmd'] == 'RIGHT':
                new_pos = self.rotate_robot(
                    {"direc": "RIGHT"}, current_pos)
            elif cmd['cmd'] == 'REPORT':
                print(current_pos)
                new_pos = current_pos
            else:
                raise Exception

        except Exception as ex:
            raise ex

        return new_pos

    # Method to check if the robot was already placed on the table
    @staticmethod
    def start(cmd, current_pos):
        try:
            # Raise exception if the robot is not in the table
            if cmd['cmd'] != 'PLACE' and current_pos['x'] is None:
                raise StartException(
                    'Please, first place the robot on the table')

        except Exception as ex:
            raise ex

        return 1


if __name__ == '__main__':

    # Initialize the game
    current_position = {'x': None, 'y': None, 'f': None}
    start = 0
    orchestrator = Orchestrator()
    while 1:
        try:
            # Get and treat the input
            inputs = {'inp': raw_input()}
            command = orchestrator.treat_inputs(inputs)

            # Check if the robot is already placed
            if start == 0:
                start = orchestrator.start(command, current_position)

            # Execute the action
            current_position = orchestrator.execute_command(
                command, current_position)

        except Exception as ex:
            print(repr(ex))
