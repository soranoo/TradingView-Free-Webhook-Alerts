import os
import time

def load_env(env_name):
	open_env_cmd = f"cmd /k {os.path.join(os.getcwd(), env_name, 'Scripts', 'activate')}"
	create_env_cmd = f"py -m venv env"
	if os.path.isdir(os.path.join(os.getcwd(), env_name, "Scripts")):
		os.system(open_env_cmd)
	else:
		print("No virtual environment found.")
		# ask the user create a new venv or not
		o = input("Do you want to create a new virtual environment? [y/n] ")
		if o.lower() == "y":
			print("Creating virtual environment...")
			os.system(create_env_cmd)
			os.system(open_env_cmd)
		else:
			print("The program will shut down after 10s...")
			time.sleep(10)
			exit()

if __name__ == "__main__":
	load_env("env")