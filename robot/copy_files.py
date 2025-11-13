import subprocess
import os

# List of files to copy to the robot
FILES = [
    "drive.py",
    "line_sensor.py",
    "ultrasound.py",
    "neopix_buzzer.py",
    "simple_reader.py",
    "line_follower.py",
]

def copy_file(filename):
    print(f"→ Uploading {filename}...")
    result = subprocess.run(
        ["python", "-m", "mpremote", "fs", "cp", filename, f":{os.path.basename(filename)}"],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print(f"✅ {filename} uploaded successfully.\n")
    else:
        print(f"❌ Failed to upload {filename}:\n{result.stderr}\n")

def main():
    print("=== Deploying files to MicroPython robot ===\n")
    for f in FILES:
        if os.path.exists(f):
            copy_file(f)
        else:
            print(f"⚠️ File not found: {f}")

    print("\n✅ Deployment complete!")

if __name__ == "__main__":
    main()
