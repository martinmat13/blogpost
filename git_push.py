#!/usr/bin/env python3
import subprocess
import sys


def run_command(command):
  """Runs a shell command and streams its output, exiting if it fails."""
  process = subprocess.Popen(
      command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
  )
  for line in process.stdout:
    print(line.decode("utf-8").strip())
  process.wait()
  if process.returncode != 0:
    print(f"\n❌ Error executing command: '{command}'", file=sys.stderr)
    sys.exit(process.returncode)


def main():
  # Get commit message from arguments, or use a default one
  if len(sys.argv) > 1:
    commit_message = " ".join(sys.argv[1:])
  else:
    commit_message = "Update blog content and files"

  print("🚀 Starting Git Auto-Push Workflow...")

  # 1. Check git status
  print("\n--- [1/4] Checking status ---")
  run_command("git status")

  # 2. Add all changes
  print("\n--- [2/4] Staging files ---")
  run_command("git add .")

  # 3. Commit changes
  print(f"\n--- [3/4] Committing with message: '{commit_message}' ---")
  # Use check=False equivalent via handle so it doesn't crash if nothing to commit
  commit_process = subprocess.run(f'git commit -m "{commit_message}"', shell=True)
  if commit_process.returncode != 0:
    print(
        "\n⚠️ No changes to commit or commit failed. Proceeding to push"
        " anyway..."
    )

  # 4. Push to remote repository
  print("\n--- [4/4] Pushing to GitHub ---")
  run_command("git push")

  print("\n✨ Successfully pushed to GitHub!")


if __name__ == "__main__":
  main()