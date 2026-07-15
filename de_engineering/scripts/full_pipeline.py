import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2] 

scripts_dir = Path(__file__).resolve().parents[0]
scripts = [
    scripts_dir / "build_warehouse.py",
    scripts_dir / "run_etl.py",
]

def run_script(script_path: Path):
    print("=" * 60)
    print(f"Running {script_path.name}")
    print("=" * 60)
    subprocess.run(
        [sys.executable, str(script_path)],
        check=True
    )
    print(f"{script_path.name} completed.\n")


def main():
    print("=" * 60)
    print("FULL DATA PIPELINE")
    print("=" * 60)
    for script in scripts:
        run_script(script)
    print("=" * 60)
    print("Pipeline finished successfully!")
    print("=" * 60)

if __name__ == "__main__":
    main()