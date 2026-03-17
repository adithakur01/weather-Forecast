import subprocess
import os
import sys
import shutil

# Files ka execution order
steps = [
    "root/ingestion.py",
    "root/transformation.py",
    "root/feature_engineering.py",
    "root/model.py"
]

def cleanup_old_data():
    folders_to_clean = ["data/raw", "data/processed"]
    for folder in folders_to_clean:
        if os.path.exists(folder):
            shutil.rmtree(folder) # Poora folder delete
            os.makedirs(folder)   # Khali folder dobara create
    print("Workspace Cleaned: Old data removed.")

def run_production_pipeline():
    print("STARTING AUTO WEATHER PIPELINE")
    print("-" * 40)
    
    # Step 0: Cleanup
    cleanup_old_data()

    # Step 1-4: Sequential Execution
    for script in steps:
        script_name = os.path.basename(script).upper()
        print(f"Running: {script_name}")
        
        try:
            env = os.environ.copy()
            env["PYTHONPATH"] = os.getcwd()
            
            # Script run karna
            subprocess.run([sys.executable, script], check=True, env=env)
            print(f"{script_name} Completed")
            
        except subprocess.CalledProcessError as e:
            print(f"Critical Failure In {script_name}")
            sys.exit(1)

    print("-" * 40)
    print("Pipeline Refreshed: New Models & Data Ready.")

if __name__ == "__main__":
    run_production_pipeline()