all: packages DiskAnalyzer.py 
	sudo python3 DiskAnalyzer.py
packages:
	sudo apt-get install g++
	sudo apt-get install python3
	sudo apt-get install python3-pip
	pip3 install --user --upgrade pip
	python3 -m pip install PyQt5
	sudo apt-get install python3-matplotlib


