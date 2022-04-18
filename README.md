help :'(

# Using development environment (pipenv)

Install pipenv (pip install pipenv).

If there is a virtualenv issue when runing pipenv, make sure to uninstall all previous versions of virtualenv (installing virtualenv with sudo apt-get and pip can sometimes cause it to download two versions of virtualenv which confuses pipenv).

Run the environment with (pipenv shell) which should create a environment with all the dependencies already installed.

Pipenv will automatically install the dependencies and resolve subdependency issues.

Therefore installing python modules, do so with pipenv (pipenv install module-name).

# Development

Use the ptyhon formatter tool (Black: https://github.com/psf/black).

An installation and use guide for using black in vscode can be found here: https://dev.to/adamlombard/how-to-use-the-black-python-code-formatter-in-vscode-3lo0

Add files to be ignored by git/that should not be added to the repo into the (.gitignore) file.

# Adding and processing data for the dashboard

Add data (csv files) to the data/raw directory.

Multiple data files can be added for one country.

Scripts assume that there are no repeat tweets recorded in the data or across all the datasets.

Then run the (sentiment_analysis.py) script from inside the data directory (otherwise it will not work). This should output a processed data csv file into the data directory.

That processed file in the data directory is what should be used by the (app.py) script. It will be named ("processed\_" + original_filename.csv).

# Running dashboard

Inside the pipenv environment, run (python app.py).

Make sure there is processed data (refer to previous section) in the data directory before running.

You do not need to run or edit the (module_data.py) or (module_graph.py) script to run the dashboard.
