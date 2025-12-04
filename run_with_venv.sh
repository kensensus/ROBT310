#!/bin/bash
# Activate virtual environment and run script

source ~/face_attendance_env/bin/activate
python3 "$@"
deactivate
