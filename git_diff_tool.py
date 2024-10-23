import subprocess
import os
import argparse
import shutil
import tempfile

def welcome_art():
    welcome_art = """
    =================================================
    |                                                |
    |          Welcome to the Git Diff Tool!         |
    |      Easily compare Git branches with ease     |
    |                                                |
    |                Version: 1.0.0                  |
    |                                                |
    =================================================
    """
    print(welcome_art)

def fetch_remote_branch(url, main_branch):
    subprocess.run(["git", "remote", "add", "temp_remote_branch", url], stderr=subprocess.DEVNULL, check=True)
    
    print(f"Fetching the {main_branch} branch from the remote repository...")
    subprocess.run(["git", "fetch", "temp_remote_branch", main_branch], check=True)

def compare_with_remote_branch(local_branch, main_branch, target_folder):
    print(f"Comparing {local_branch} with remote {main_branch}...")

    diff_files_output = subprocess.run(
        ["git", "diff", "--name-only", f"temp_remote_branch/{main_branch}", local_branch, "--", target_folder],
        capture_output=True, text=True, check=True
    )

    changed_files = diff_files_output.stdout.strip().split("\n")

    if diff_files_output.returncode != 0 or not changed_files or changed_files == ['']:
        print("Error or no changes detected.")
        exit(1)

    temp_dir = tempfile.mkdtemp()

    for file in changed_files:
        file_path = os.path.join(target_folder, file)
        temp_file_main = os.path.join(temp_dir, f"main_{file}")
        temp_file_local = os.path.join(temp_dir, f"local_{file}")

        os.makedirs(os.path.dirname(temp_file_main), exist_ok=True)
        os.makedirs(os.path.dirname(temp_file_local), exist_ok=True)

        subprocess.run(["git", "show", f"temp_remote_branch/{main_branch}:{file_path}"], stdout=open(temp_file_main, 'w'))
        subprocess.run(["git", "show", f"{local_branch}:{file_path}"], stdout=open(temp_file_local, 'w'))

        print(f"Opening diff for {file} in VS Code...")
        subprocess.run(["code", "--diff", temp_file_local, temp_file_main], check=True)

    # shutil.rmtree(temp_dir)

def main():
    welcome_art()

    path = "."

    git_folder = os.path.join(path, ".git")
    if not os.path.isdir(git_folder):
        print(f"❌ A git repository not found in '{os.path.abspath(path)}'.")
        exit(1)

    parser = argparse.ArgumentParser(
        description="Git Diff Tool - Compare two branches of a Git repository and display diffs in VS Code."
    )

    parser.add_argument("--repository", type=str, help="URL of the Git repository")
    parser.add_argument("--main-branch", type=str, help="Main branch to compare from")
    parser.add_argument("--local-branch", type=str, help="Local branch to compare to")
    parser.add_argument("--target-folder", type=str, help="Target folder for the diff operation")

    args = parser.parse_args()

    if not args.repository or not args.main_branch or not args.local_branch or not args.target_folder:
        REPOSITORY_URL = args.repository or input("Enter the repository URL: ")
        MAIN_BRANCH = args.main_branch or input("Enter the main branch (e.g., 'main'): ")
        LOCAL_BRANCH = args.local_branch or input("Enter the local branch (e.g., 'dev'): ")
        TARGET_FOLDER = args.target_folder or input("Enter the target folder for the diff operation: ") or "."
    else:
        REPOSITORY_URL = args.repository
        MAIN_BRANCH = args.main_branch
        LOCAL_BRANCH = args.local_branch
        TARGET_FOLDER = args.target_folder

    fetch_remote_branch(REPOSITORY_URL, MAIN_BRANCH)
    
    compare_with_remote_branch(LOCAL_BRANCH, MAIN_BRANCH, TARGET_FOLDER)

    subprocess.run(["git", "remote", "remove", "temp_remote_branch"], capture_output=True, text=True)

if __name__ == "__main__":
    main()
