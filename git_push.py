#!/usr/bin/env python3
import subprocess
import sys
import webbrowser
import time

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

    print("🚀 Starting Local Preview & Git Auto-Push Workflow...")

    # 1. Start Local Server for Verification
    print("\n--- [1/5] Starting local server for preview ---")
    port = 8000
    
    # Start Python's built-in HTTP server in the background
    server_process = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(port)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    print(f"Local server running at http://localhost:{port}")
    time.sleep(1.5) # Give the server a moment to spin up
    
    # Automatically open the default web browser
    webbrowser.open(f'http://localhost:{port}')
    
    print("\n" + "="*60)
    print("👀 PREVIEW MODE ACTIVE 👀")
    print("Your browser has opened to preview the site locally.")
    print("Verify your changes now to save Netlify deploy credits.")
    print("="*60 + "\n")

    # Ask for user confirmation before pushing
    try:
        choice = input("Does everything look good? Deploy to Netlify? (y/N): ").strip().lower()
    except KeyboardInterrupt:
        choice = 'n'
        print("\n")

    # Shut down the local server regardless of the choice
    print("\nShutting down local preview server...")
    server_process.terminate()
    server_process.wait()

    # Abort if the user didn't explicitly say yes
    if choice not in ['y', 'yes']:
        print("🛑 Deployment aborted. You can fix your files and run this script again.")
        sys.exit(0)

    print("\n✅ Changes confirmed. Proceeding with deployment...")

    # 2. Check git status
    print("\n--- [2/5] Checking status ---")
    run_command("git status")

    # 3. Add all changes
    print("\n--- [3/5] Staging files ---")
    run_command("git add .")

    # 4. Commit changes
    print(f"\n--- [4/5] Committing with message: '{commit_message}' ---")
    commit_process = subprocess.run(f'git commit -m "{commit_message}"', shell=True)
    if commit_process.returncode != 0:
        print("\n⚠️ No changes to commit or commit failed. Proceeding to push anyway...")

    # 5. Push to remote repository (Triggers Netlify)
    print("\n--- [5/5] Pushing to GitHub ---")
    run_command("git push")

    print("\n✨ Successfully pushed to GitHub! Netlify is now building your site.")

if __name__ == "__main__":
    main()