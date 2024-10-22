import os
import shutil
import subprocess
import logging

def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        logging.error(f"Error running command '{' '.join(command)}': {e}")
        return None, None, str(e)

def copy_test_file():
    source = "/utils/raft_test.go"
    destination = "/workspace/raft/src/github.com/cmu440/raft/raft_test.go"
    try:
        shutil.copy2(source, destination)
        logging.info(f"Copied {source} to {destination}")
        return True
    except Exception as e:
        logging.error(f"Failed to copy test file: {e}")
        return False

def run_test(test_command):
    os.chdir("/workspace/raft/src/github.com/cmu440/raft/")
    returncode, stdout, stderr = run_command(test_command)
    if returncode is None:
        logging.error("Command execution failed")
        return False

    output = stdout + "\n" + stderr

    if "no tests to run" in output.lower():
        logging.warning("No tests were run. Command may be invalid.")
        return False

    if "PASS" in output and "ok" in output and "FAIL" not in output:
        logging.info("All tests passed.")
        return True
    else:
        logging.error("Tests failed or unexpected output.")
        return False

# Check pass all 2A tests
def grade_checkpoint1():
    if not copy_test_file():
        logging.error("Failed to copy test file in checkpoint1")
        return False

    return run_test(["go", "test", "-run", "2A"])

# Check pass all tests
def grade_checkpoint2():
    if not copy_test_file():
        logging.error("Failed to copy test file in checkpoint2")
        return False

    return run_test(["go", "test"])

def grade_checkpoints():
    checkpoints = [
        (grade_checkpoint1, "Checkpoint 1: go test -run 2A passes", 5),
        (grade_checkpoint2, "Checkpoint 2: Full test passes", 5)
    ]

    earned_points = 0
    for grade_func, description, point_value in checkpoints:
        try:
            passed = grade_func()
            if passed:
                earned_points += point_value
            print(f"{'✓' if passed else '✗'} {description}")
            if not passed:
                break
        except Exception as e:
            logging.error(f"Error while grading checkpoint {description}: {e}")
            break

    return earned_points

if __name__ == "__main__":
    earned_points = grade_checkpoints()
    print(f"\nFinal points: {earned_points}/10")