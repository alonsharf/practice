import re
import subprocess
from datetime import datetime
from os import error


def update_repository(repo_name):
    try:
        #update apt repo.
        subprocess.run(['aptly', 'mirror', 'update', repo_name], check=True)
        print(f"Repository '{repo_name}' updated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to update repository '{repo_name}'. Error: {e}")

def create_snapshot(repo_name):
    try:
        #take snapshot of apt repo.
        current_date = datetime.now().strftime('%Y-%m-%d')
        snapshot_name = f"{repo_name}-{current_date}"
        subprocess.run(['aptly', 'snapshot', 'create', snapshot_name, 'from', 'repo', repo_name], check=True)
        return snapshot_name
    except subprocess.CalledProcessError as e:
        print(f"Failed to create snapshot for repository '{repo_name}'. Error: {e}")
        return None

def get_snapshot_diff(repo_name, snapshot_a, snapshot_b):
    try:
        diff_output = subprocess.check_output(['aptly', 'snapshot', 'diff', '-json', snapshot_a, snapshot_b])

        diff_json = diff_output.decode('utf-8')
        diff_data = eval(diff_json)

        updated_files = []
        file_paths = []
        for package in diff_data['Diff']['Added']:
            if 'Files' in package:
                updated_files.extend(package['Files'])
                file_paths.extend(package['PackageRefs'])

        # Construct full paths to the updated files  - TODOOOOOOOOOO
        full_paths = [f"/var/lib/aptly/{repo_name}/{snapshot_b}/pool/{path}/{file}" for path, file in file_paths]
        return updated_files, full_paths
    
    except subprocess.CalledProcessError as e:
        print(f"Failed to get snapshot diff. Error: {e}")
        return [], []

def main():

    repository_name = 'repo-name'
    
    snapshot_name_a = 'snapshot-a'
    snapshot_name_b = create_snapshot(repository_name)
    if snapshot_name_b == None:
        print("Issue with update package")
        return None
    
    update_repository(repository_name)
    updated_files, file_paths = get_snapshot_diff(repository_name, snapshot_name_a, snapshot_name_b)