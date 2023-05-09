import os
import shutil
import time
import threading
from threading import Thread, Lock

print("Starting")

# Set the directory to watch for .plot files
watch_dir = ""

# Set the list of destination drives to move the files to
# tuple should be in the format of (drive, description)
# dest_drives = [("/mnt/drive1", "drive1"), ("/mnt/drive2", "drive2"), ("/mnt/drive3", "drive3"), ("/mnt/drive4", "drive4")]
dest_drives = []

# Set the maximum number of plots to copy simultaneously to each drive
max_plots_per_drive = 1

# Define a lock for the moving list
moving_list_lock = Lock()

#used to track plots that are being moved
moving_list = list()

# Define a function to move a plot file to a destination drive
def move_plot(plot_file, dest_drive, drive_name):
    print(f"Moving {plot_file} to {dest_drive}")
    start_time = time.time()
    shutil.move(os.path.join(watch_dir, plot_file), dest_drive)
    end_time = time.time()
    print(f"Moved {plot_file} to {dest_drive} in {end_time - start_time:.2f} seconds")
    with moving_list_lock:
            moving_list.remove(plot_file);

# Loop indefinitely to watch for new .plot files
while True:
    # Get a list of all .plot files in the watch directory
    plot_files = [f for f in os.listdir(watch_dir) if f.endswith(".plot")]

    # Loop through the list of .plot files
    for plot_file in plot_files:
        # Check if the plot_file is being moved. If it is than skip it.
        with moving_list_lock:
            if plot_file in moving_list:
                continue;

        # Loop through the list of destination drives
        for dest_drive, drive_name in dest_drives:
            # Check if the destination drive is mounted and has free space and is not already copying max_plots_per_drive plots
            if os.path.ismount(dest_drive) and shutil.disk_usage(dest_drive).free > os.path.getsize(os.path.join(watch_dir, plot_file)):
                plots_copied_to_dest = sum([1 for t in threading.enumerate() if t.name == drive_name])
                if plots_copied_to_dest < max_plots_per_drive:
                    with moving_list_lock:
                        # Move the plot file to the destination drive in a new thread
                        t = Thread(target=move_plot, args=(plot_file, dest_drive, drive_name), name=drive_name)
                        t.start()
                        moving_list.append(plot_file)

                    # Break out of the inner for loop after a successful plot file move
                    break
        else:
            # If all destination drives are full or not mounted, print an error message
            print(f"All destination drives are full or not mounted, could not move {plot_file}")

    # Wait for a short time before checking for new files
    time.sleep(10)
