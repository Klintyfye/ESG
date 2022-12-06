#!/bin/bash
echo "start"

npm=0
retire=0

if [[ "$OSTYPE" == "linux-gnu" ]]; then
	echo "running linux-gnu"
else
	echo "not running linux-gnu"
	exit 0
fi

sudo apt update

###

if dpkg --get-selections | grep -q "^npm[[:space:]]*install$" >/dev/null; then
	echo "npm already installed"
	npm=1
else
	echo "install npm"
	sudo apt install npm -y
	
	if dpkg --get-selections | grep -q "^npm[[:space:]]*install$" >/dev/null; then
		echo "npm installed"
		npm=1
	else
		echo "npm install failed"
		exit 0
	fi
fi

###

if [ `npm list -g | grep -c retire` -eq 1 ]; then
	echo "retire already installed"
	retire=1
else
	echo "install retire"
	sudo npm install -g retire

	if [ `npm list -g | grep -c retire` -eq 1 ]; then
		echo "retire installed"
		retire=1
	else
		echo "retire install failed"
		exit 0
	fi
fi

###

if [[ $npm -eq 1 && $retire -eq 1 ]]; then
	echo "npm and retire installed"
	exit 1
else
	echo "install failed"
	exit 0
fi
