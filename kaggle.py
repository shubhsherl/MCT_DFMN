import shlex
import logging
import subprocess
from io import StringIO
import os

def pip_install():
    PACKAGES = ['googleDriveFileDownloader']
    print('installing packages')
    subprocess.call(['pip', 'install'] + PACKAGES)

def rm_data():
    print('removing data')
    zipFile_ = 'miniImageNet.zip'
    subprocess.call(['rm', zipFile_])

def clone_repo():
    REPO_LOCATION = 'https://github.com/shubhsherl/MCT_DFMN.git'
    REPO_BRANCH = 'master'
    
    # Clone the repository
    print('cloning the repository')
    subprocess.call(['git', 'clone', '-b', REPO_BRANCH, REPO_LOCATION])

def download_data():
    print('downlading data')
    from googleDriveFileDownloader import googleDriveFileDownloader
    a = googleDriveFileDownloader()
    url = 'https://drive.google.com/uc?id=1fJAK5WZTjerW7EWHHQAR9pRJVNg1T1Y7&export=download'
    a.downloadFile(url)

def extract_file():
    import zipfile
    print('extracting data')
    zipFile_ = 'miniImageNet.zip'
    subprocess.call(['mkdir', 'MCT_DFMN/mini_ImageNet/data/miniImageNet'])
    dest = 'MCT_DFMN/mini_ImageNet/data/miniImageNet'
    archive = zipfile.ZipFile(zipFile_)
    #   if file.startswith('miniImageNet_category_split_train_phase_train.pickle') or file.startswith('miniImageNet_category_split_test.pickle'):
    for file in archive.namelist():
        if file.startswith('mini-imagenet-cache-val.pkl'):
            archive.extract(file, dest)
    

def train_data():
    print('training...')
    os.chdir('./MCT_DFMN/mini_ImageNet/scripts')
    # subprocess.call(['python', 'train.py', '--transductive', 'False', '--flip' ,'False', '--drop' ,'False', '--n_shot', '1'])
    command_line = 'python train.py --is_train True --gpu 0 --transductive False --flip False --drop False --n_shot 1 --n_train_class 15'
    command_line_args = shlex.split(command_line)

    logging.info('Subprocess: "' + command_line + '"')

    try:
        command_line_process = subprocess.Popen(
            command_line_args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

        process_output, _ =  command_line_process.communicate()

        # process_output is now a string, not a file,
        # you may want to do:
        # process_output = StringIO(process_output)
        print(process_output)
    except (OSError, subprocess.CalledProcessError) as exception:
        logging.info('Exception occured: ' + str(exception))
        logging.info('Subprocess failed')
        return False
    else:
        # no exception was raised
        logging.info('Subprocess finished')

    return True

# pip_install()
# clone_repo()
# download_data()
# extract_file()
# rm_data()
train_data()
