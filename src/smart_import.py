import subprocess
import sys
import os
import time

def try_import(import_module: str, submodules: list = [], pip_package_name: str | None = None, force_import: bool = False):
    """
    Try import the given module, return the module if success
    else install the module when the user confirm(said yes)
    return the module after installation

    Args:
        import_module (str): Module to import
        submodules (list[str], optional): Submodules to import. Defaults to [None].
        pip_package_name (str, optional): The name of the package in PyPI. Defaults to None.
        force_import (bool, optional): Install the module without asking. Defaults to False.

    Example:
        [1. import check and import]
        FROM:  from discord.embeds import Embed OtherModule
        TO:    Embed = try_import("discord.embeds", ["Embed", "OtherModule"], "discord.py").Embed
        
        [2. just do the import check]
        FROM: from discord.embeds import Embed
        TO:    try_import("discord", pip_package_name="discord.py")
               from discord.embeds import Embed

    Returns:
        module: The module
    """
    try:
        return __import__(import_module, fromlist=submodules)
    except ModuleNotFoundError:
        if pip_package_name is None:
            pip_package_name = import_module
        if force_import:
            return _install_module(pip_package_name, import_module, submodules)
        print(f"Module '{import_module}' not found.")
        print("Do you want to install this module? (y/n)")
        if input().lower() == "y":
            return _install_module(pip_package_name, import_module, submodules)
        else:
            exit()


def _install_module(pip_package_name, import_module, submodules):
    """
    Install the module and return the module
    
    Args:
        pip_package_name (str): The name of the package in PyPI.
        import_module (str): Module to import
        submodules (list[str]): Submodules to import.
    """
    print("Installing module...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", pip_package_name])
    print("Module installed.")
    time.sleep(1)
    os.system("cls")
    return __import__(import_module, fromlist=submodules)