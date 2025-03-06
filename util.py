import pandas as pd
from scipy.io import arff

import os
import zipfile

# REPO_DIR = "CSCE-474/"
# DATA_DIR = "data/"
REPO_DIR = ""
DATA_DIR = ""

def arff_to_df(file, directory="", decode_bytes=True):
    """
    Load an ARFF file into a pandas DataFrame
    
    Arguments:
    file: str
        The name of the ARFF file to be loaded
    directory: str
        The name of the directory where the ARFF file is located
        (Assumes the directory is located in the REPO_DIR, and that the ARFF file is located in a directory with the standard name DATA_DIR)
    decode_bytes: bool
        Whether to decode bytes to strings in the DataFrame 
        (most ARFF files contain byte strings)
    """
    
    repo_dir_name = os.path.basename(os.path.normpath(REPO_DIR))
    active_dir_name = os.path.basename(os.getcwd())

    if repo_dir_name == active_dir_name:
        data_directory = f"{directory}{DATA_DIR}"
    else:
        data_directory = f"{REPO_DIR}{directory}{DATA_DIR}"
    
    df = pd.DataFrame(arff.loadarff(f'{data_directory}{file}')[0])
    if decode_bytes:
        for col in df.columns:
            if df[col].dtype == object:
                df[col] = df[col].str.decode('utf-8')
    return df

# TODO: the private flag currently overrides the content of the .gitignore -> fix this
def create_assignment(assignment, dataset, repo_directory=REPO_DIR, data_directory=DATA_DIR, signature=["Dante Dyches-Chandler"], private=False):
    os.makedirs(f"{repo_directory}{assignment}/{data_directory}", exist_ok=True)
    # write in the new directory two files: README.md and file.py, where file.py contains the import statements
    with open(f"{repo_directory}{assignment}/README.md", "w") as f:
        f.write(f"# {assignment}\n\n## Dataset\n{dataset}\n")
        f.write("\n## Contributors\n")
        for name in signature:
            f.write(f"- {name}\n")
    with open(f"{repo_directory}{assignment}/file.py", "w") as f:
        f.write(f"import pandas as pd\nimport util\n\ndf = util.arff_to_df(\"{dataset}\")\n")
    if private:
        with open(f"{REPO_DIR}.gitignore", "w") as f:
            f.write(f"\n{assignment}\n")



# TODO: include util.py and requirements.txt in all downloads (and data directory)
# TODO: include terminal arguments for prepare_submission function, ie., py -m prepare_submission.py "CSCE-474/Assignment 2" "test"
def prepare_submission(folder_name, repo_directory=REPO_DIR, zip_name=None):
    """
    Transform the specified folder into a zip file, including all dependencies
    """
    def zipdir(path, ziph):
        for root, dirs, files in os.walk(path):
            for file in files:
                ziph.write(os.path.join(root, file))
    if not zip_name:
        zipf = zipfile.ZipFile(f'{folder_name}.zip', 'w', zipfile.ZIP_DEFLATED)
        zipdir(folder_name, zipf)
    else: 
        zipf = zipfile.ZipFile(f'{zip_name}.zip', 'w', zipfile.ZIP_DEFLATED)
        zipdir(folder_name, zipf)
    zipf.close()

# Example usage:
# prepare_submission(f"{REPO_DIR}Assignment N", zip_name="test")
# create_assignment("Assignment N", "vote.arff", signature=["Dante Dyches-Chandler", "Dante Dyches-Chandler"], private=True)