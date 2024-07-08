from database.db import connect_to_mongodb
import subprocess

def run_bash_script(script_path):
    try:
        subprocess.run(["bash",script_path],check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

run_bash_script('/mnt/d/CollegeProject/UPNepse/run.sh')
        


