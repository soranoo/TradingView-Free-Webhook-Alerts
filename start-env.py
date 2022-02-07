# -----------------* reference *-----------------
# https://stackoverflow.com/a/60781848
# -----------------------------------------------

import os

path_env = r".\env\Scripts\activate"

'''
Create venv 'py -m venv env'
Freeze 'pip freeze -l > requirements.txt'
With /k cmd executes and then remain open
With /c executes and close
'''
if __name__ == "__main__":
	os.system(f"cmd /k {path_env}")
