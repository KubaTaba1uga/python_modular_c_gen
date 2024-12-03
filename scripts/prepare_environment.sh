#!/bin/bash
# This script sets up a Python virtual environment for a project, installs packages
# required to work with the repo and opens a new shell with the virtual environment
# activated.

# Define paths
THIS_SCRIPT_PATH=$(realpath "$0")
PROJ_ROOT_PATH=$(dirname "$(dirname "$THIS_SCRIPT_PATH")")
VENV_PATH="$PROJ_ROOT_PATH/.venv"
VENV_PYTHON_PATH="$VENV_PATH/bin/python"

# Check if virtualenv exists
if ! command -v virtualenv &> /dev/null; then
   echo "virtualenv could not be found"
   exit -1
fi

# Create a virtual environment if it doesn't exist
if [ ! -d "$VENV_PATH" ]; then
   virtualenv "$VENV_PATH"
fi

# Install invoke
if ! $VENV_PYTHON_PATH -m pip install invoke==2.2.0; then
   echo "invoke could not be installed"
   exit -1
fi

# Create a temporary file for the shell initialization
TEMP_RCFILE=$(mktemp)

# Add commands to the temporary file
echo "source \"$VENV_PATH/bin/activate\"" > "$TEMP_RCFILE"
## Substitute .venv with .lt-venv in the export PS1 command using awk
echo 'export PS1=$(echo $PS1 | awk "{gsub(\".venv\", \".new-repo\"); print}")' >> "$TEMP_RCFILE"
echo 'export PS1="$(echo $PS1) "' >> "$TEMP_RCFILE"

# Start a new shell using the temporary initialization file
bash --rcfile "$TEMP_RCFILE"

# Clean up the temporary file
rm -f "$TEMP_RCFILE"

