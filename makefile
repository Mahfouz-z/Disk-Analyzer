all: __main__.py packages
	python3 __main.py
packages:
	sudo apt-get install python3
	sudo apt-get install python3-pip
	sudo apt-get install python3-pyqt5
	pip3 install matplotlib


