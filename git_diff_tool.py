import subprocess
import os
import argparse

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
    subprocess.run(["git", "remote", "add", "temp_remote_branch", url], stderr=subprocess.DEVNULL)

    print(f"Fetching the {main_branch} branch from the remote repository...")
    subprocess.run(["git", "fetch", "temp_remote_branch", main_branch], check=True)

def compare_with_remote_branch(local_branch, main_branch, target_folder):
    print(f"Comparing {local_branch} with remote {main_branch}...")

    diff_output = subprocess.run(
        ["git", "diff", f"temp_remote_branch/{main_branch}", local_branch, "--", target_folder],
        capture_output=True, text=True
    )

    if diff_output.returncode != 0:
        print("Error occurred while comparing the branches.")
        print(diff_output.stderr)
        exit(1)
    
    if diff_output.stdout == "":
        print("No changes detected.")
        exit(0)
    
    return diff_output.stdout

def save_diff_to_file(diff_content, save_dir):
    lines = diff_content.splitlines()

    formatted_diff = ""
    current_file = None

    for line in lines:
        if line.startswith("diff --git"):
            file_path = line.split()[-1]
            formatted_diff += f"\n=== Changes in file: {file_path} ===\n\n"
            current_file = file_path
        elif line.startswith("---") or line.startswith("+++"):
            continue
        else:
            formatted_diff += line + "\n"

    os.makedirs(save_dir, exist_ok=True)
    diff_path = os.path.join(save_dir, "diff_output.txt")
    
    with open(diff_path, "w") as f:
        f.write(formatted_diff)
    
    print(f"Saved diff content to {diff_path}")

def extract_changed_files(diff_content, save_dir):
    changed_files = []
    
    for line in diff_content.splitlines():
        if line.startswith("diff --git"):
            file_path = line.split(" ")[2][2:]
            changed_files.append(file_path)
    
    file_list_path = os.path.join(save_dir, "changed_file_names.txt")
    with open(file_list_path, "w") as f:
        f.write("\n".join(changed_files))
    
    print(f"Saved list of changed files to {file_list_path}")
    return changed_files

def main():
    welcome_art()

    path = "."

    git_folder = os.path.join(path, ".git")
    if not os.path.isdir(git_folder):
        print(f"❌ A git repository not found in '{os.path.abspath(path)}'.")
        exit(1)

    parser = argparse.ArgumentParser(
        description="Git Diff Tool - Compare two branches of a Git repository and save the output."
    )

    parser.add_argument("--repository", type=str, help="URL of the Git repository")
    parser.add_argument("--main-branch", type=str, help="Main branch to compare from")
    parser.add_argument("--local-branch", type=str, help="Local branch to compare to")
    parser.add_argument("--save-dir", type=str, help="Directory to save the diff output")
    parser.add_argument("--target-folder", type=str, help="Target folder for the diff operation")

    args = parser.parse_args()

    if args.repository is None or args.main_branch is None or args.local_branch is None or args.save_dir is None or args.target_folder is None:
        REPOSITORY_URL = args.repository or input("Enter the repository URL: ")
        MAIN_BRANCH = args.main_branch or input("Enter the main branch (e.g., 'main'): ")
        LOCAL_BRANCH = args.local_branch or input("Enter the local branch (e.g., 'dev'): ")
        SAVE_DIR = args.save_dir or input("Enter the directory to save the diff output: ")
        TARGET_FOLDER = args.target_folder or input("Enter the target folder for the diff operation: ") or "."
    else:
        REPOSITORY_URL = args.repository
        MAIN_BRANCH = args.main_branch
        LOCAL_BRANCH = args.local_branch
        SAVE_DIR = args.save_dir
        TARGET_FOLDER = args.target_folder
    
    fetch_remote_branch(REPOSITORY_URL, MAIN_BRANCH)
    
    diff_content = compare_with_remote_branch(LOCAL_BRANCH, MAIN_BRANCH, TARGET_FOLDER)
    
    save_diff_to_file(diff_content, SAVE_DIR)
    
    extract_changed_files(diff_content, SAVE_DIR)

    print("Comparison completed.")

    subprocess.run(
        ["git", "remote", "remove", "temp_remote_branch"],
        capture_output=True, text=True
    )

if __name__ == "__main__":
    main()
