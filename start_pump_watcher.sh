# Start the pump watcher daemon.
# This script will never exit unless the pump watcher exits.
#
# Assumes that all python libraries are available.
#

echo "Starting pump watcher daemon..."
python3 pump_watcher.py

echo Exiting...
