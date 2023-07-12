import os
import subprocess
import win32process, win32event, win32api, win32con
import shutil
from git import Repo


def ignore_folder(path, names):
    # Пропускать папку .git
    return ['.git'] if '.git' in names else []


os.system('taskmgr')
# repo_path = 'pig_bot'
# repo = Repo(repo_path)
# repo.git.add('.')
# repo.index.commit("Auto Commit")
# origin = repo.remote(name='origin')
# origin.push()
# exit()
bat_file = 'A:/test_pig_bot/start.bat'
shutil.rmtree('A:/test_pig_bot')
shutil.copytree('pig_bot', 'A:/pig_bot', ignore=ignore_folder)
with open('A:/test_pig_bot/pig_code/core/config.py', 'r+') as f:
    content = f.read()
    new_content = content.replace('TEST = False', 'TEST = True').replace('PUBLIC_TEST = False', 'PUBLIC_TEST = True')
    f.seek(0)
    f.write(new_content)
with open(bat_file, 'w') as f:
    f.write(
        r"""
        @echo off
        cd /D "A:/pig_bot"
        start "PigBotProcess" /B pythonw main.py
        """
    )
