#!/usr/bin/env python3
import subprocess
import sys
import webbrowser
import time

def run_command(command, ignore_errors=False):
    """Runs a shell command and streams its output."""
    process = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    for line in process.stdout:
        print(line.decode("utf-8").strip())
    process.wait()
    
    # If the command fails and we aren't ignoring errors, stop the script
    if process.returncode != 0 and not ignore_errors:
        print(f"\n❌ Error executing command: '{command}'", file=sys.stderr)
        print("⚠️ If this is a merge conflict, you edited the exact same line as the CMS. You must fix it manually.")
        sys.exit(process.returncode)

def main():
    if len(sys.argv) > 1:
        commit_message = " ".join(sys.argv[1:])
    else:
        commit_message = "Update blog structure and styling"

    print("🚀 Starting Two-Player Git Sync Workflow...")

    # 1. Save local changes FIRST so they aren't overwritten by the download
    print("\n--- [1/5] Saving your local computer's changes ---")
    run_command("git add .")
    # We ignore errors here in case you didn't actually change any files locally
    run_command(f'git commit -m "{commit_message}"', ignore_errors=True)

    # 2. Download the CMS changes from GitHub
    print("\n--- [2/5] Downloading latest stories from the CMS ---")
    # --no-edit prevents the script from trapping you in a terminal text editor
    run_command("git pull --no-edit")

    # 3. Start Local Server for Verification
    print("\n--- [3/5] Starting local server for preview ---")
    port = 8000
    
    server_process = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(port)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    print(f"Local server running at http://localhost:{port}")
    time.sleep(1.5) 
    webbrowser.open(f'http://localhost:{port}')
    
    print("\n" + "="*60)
    print("👀 PREVIEW MODE ACTIVE 👀")
    print("Your browser has opened to preview the site locally.")
    print("This preview NOW INCLUDES any stories Blessy Mary published!")
    print("="*60 + "\n")

    try:
        choice = input("Does everything look good? Push to Vercel? (y/N): ").strip().lower()
    except KeyboardInterrupt:
        choice = 'n'
        print("\n")

    print("\nShutting down local preview server...")
    server_process.terminate()
    server_process.wait()

    if choice not in ['y', 'yes']:
        print("🛑 Deployment aborted. Your combined files are saved safely on your computer.")
        sys.exit(0)

    # 4. Push the combined work to remote repository
    print("\n--- [4/5] Pushing combined updates to GitHub ---")
    run_command("git push")

    print("\n✨ Success! Vercel is now building your site with both your code and her stories.")

if __name__ == "__main__":
    main()