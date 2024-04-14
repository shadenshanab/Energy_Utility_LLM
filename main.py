import os
import subprocess
import sys

def run_script(script_name):
    """ Function to run a Python script located in the same directory as this script """
    try:
        subprocess.run(['python', script_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to run {script_name}: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    print("Starting database creation...")
    run_script('create_database.py')
    print("Database created successfully.")
    #
    # print("Launching the bot GUI...")
    # run_script('bot_gui.py')

if __name__ == '__main__':
    main()
