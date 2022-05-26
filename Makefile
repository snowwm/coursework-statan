start:
	python main.py

# Builds a single-file executable with bundled Python.
# Of course, you need to "pip install pyinstaller".
# On Windows you may need to use the full path to pyinstaller binary.
# On Linux generated executable has some problems with opening files.
build:
	pyinstaller -wFn statan main.py
