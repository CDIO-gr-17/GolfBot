from unittest.mock import Mock

# Mock the move_forward function
move_forward = Mock()

# Use the mock in your test
move_forward()
move_forward.assert_called_once()  # Assert it was called once

# Simulate robot state and log actions
robot_state = {'position': 0}

def move_forward_mock():
    robot_state['position'] += 1
    print("Robot moved forward to position", robot_state['position'])

move_forward.side_effect = move_forward_mock

# Call the mock function
move_forward()

# Output should indicate the robot moved
