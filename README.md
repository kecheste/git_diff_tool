# Git Diff Tool

Welcome to **Git Diff Tool**! A simple yet powerful command-line utility designed to compare two branches of a Git repository and save their differences into a file. Whether you're working on a feature branch or resolving conflicts, this tool makes it easy to spot changes between branches.

## Features
- Compare two branches of a Git repository (e.g., `main` and `dev`).
- Output the differences between the branches into a specified directory.
- Easy to use and flexible for any Git project.

## How to Use

#### 1. Running the Diff Tool
Use the following command to compare two branches of your Git repository:

```bash
python3 diff_tool.py \
--repository="https://github.com/<username>/<repository>" \
--main-branch="main" \
--local-branch="dev" \
--save-dir="/path/to/save/diff" \
--target-folder="."
```
Parameters
- *repository*: The URL of your Git repository. Example: https://github.com/username/repository
- *main-branch*: The branch you want to compare from (e.g., main).
- *local-branch*: The branch you want to compare to (e.g., dev).
- *save-dir*: The directory where you want to save the diff output file.
- *target-folder*: The target folder where the diff operation will be performed.

#### 2. Example Usage
Here's an example that compares the dev branch with a feature-branch and saves the output to the /home/user/documents directory:
```bash
python3 diff_tool.py --repository="https://github.com/username/sample_project" \
--main-branch="dev" \
--local-branch="feature-branch" \
--save-dir="/home/user/documents" \
--target-folder="."
```

#### 3. Interactive Mode
If you don't provide some of the parameters, the tool will prompt you to input them interactively. Simply run the command without arguments and the tool will guide you through the necessary steps.

```bash
python3 diff_tool.py
```
You will then be asked to enter details like the repository URL, branch names, save directory, and target folder.
This command compares the dev branch with the feature-branch and saves the differences in the specified directory.

### License
This project is licensed under the MIT License.