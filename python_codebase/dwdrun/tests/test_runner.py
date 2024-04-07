import unittest
import subprocess


class TestRunFile(unittest.TestCase):

    def test_run_file(self):
        # Run the file in dwdrun using subprocess
        result = subprocess.call(["python3.11", "python_codebase/dwdrun/runner.py", "--jobModule=tests.test_runner_run", "--runDate=2024-01-01"])

        # Check if the return code is 0 (success)
        self.assertEqual(result, 0, "Run file did not execute successfully")

        # Optional: Check the output if needed
        # self.assertIn("expected output", result.stdout, "Output does not match expected")


if __name__ == "__main__":
    unittest.main()
