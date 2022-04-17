help :'(

# Notes

When installing python modules, do so with pipenv (pipenv install module-name)
Add data to data folder

# Using development environment (pipenv)

Install pipenv (pip install pipenv)

If there is a virtualenv issue when runing pipenv, make sure to uninstall all previous versions of virtualenv (installing virtualenv with sudo apt-get and pip can sometimes cause it to download two versions of virtualenv which confuses pipenv)

Run the environment with (pipenv shell) which should create a environment with all the dependencies already installed

Pipenv will automatically install the dependencies and resolve subdependency issues

# Running dashboard

Inside the pipenv environment, run (python dashboard.py)

# Development

Use the ptyhon formatter tool (Black: https://github.com/psf/black)

An installation and use guide for using black in vscode can be found here: https://dev.to/adamlombard/how-to-use-the-black-python-code-formatter-in-vscode-3lo0

Add files to be ignored by git/that should not be added to the repo into the (.gitignore) file
