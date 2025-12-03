#!/bin/bash
# Activate virtual environment and run script

# Activate virtual environment
source ~/face_attendance_env/bin/activate

# Run the script with all arguments
python3 "$@"

# Deactivate virtual environment
deactivate
