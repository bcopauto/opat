#!usr/bin/env python3
import subprocess
import os
import time

def runner(bashFile, inputFile=None):
    os.chmod(bashFile,0o755)
    subprocess.call(bashFile, shell=True)

