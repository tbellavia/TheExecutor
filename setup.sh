#!/bin/bash

RED='\033[0;31m'
ORANGE='\033[0;33m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
DARK_GRAY='\033[1;30m'
NC='\033[0m'

ARG="$1"

USAGE=$(
	cat <<USAGE_STRING

setup.sh up | down | clean --

	\`up'		:
		Run bot.py

	\`install'	:
		Pull docker image and install all python dependencies

	\`setup'	:
		Setup the Dockerfile with the API_KEY provided by the user.

	\`clean'	:
		Clean docker cache.

USAGE_STRING
)

function status_bar() {
	_help=$(
		cat <<HELP
StatusMessage [--help], type, start, padding, message
	Parameters
		:type:		the status type of message, accept the following value
		:start:		the starting character
		:padding:	the space between start character and message
		:message:	the message to be printed
	Type
		- ${BLUE}primary${NC}
		- ${DARK_GRAY}secondary${NC}
		- ${YELLOW}success${NC}
		- ${RED}danger${NC}
		- ${ORANGE}warning${NC}
	Exit
		StatusMessage returns 0 if no error is encountered otherwise returns following values
			1 -> Missing parameter
			2 -> Unknown status type
			3 -> Help
			4 -> Too many parameters
HELP
	)

	if [[ "$#" == 1 ]]; then
		if [[ "$1" == "--help" ]]; then
			printf "%s\n" "$_help"
		fi
		exit 3
	elif [[ "$#" -gt 4 ]]; then
		printf "Too many parameters\n"
		exit 4
	fi

	case "$1" in
	"primary")
		_color="${BLUE}"
		;;
	"secondary")
		_color="${DARK_GRAY}"
		;;
	"success")
		_color="${YELLOW}"
		;;
	"danger")
		_color="${RED}"
		;;
	"warning")
		_color="${ORANGE}"
		;;
	*)
		exit 2
		;;
	esac

	printf "${_color}%s${NC} %${3}s%s\n" "${2}" "${4}"
}

function danger() {
	status_bar danger ">>>" 2 "$1"
}

function success() {
	status_bar success ">>>" 2 "$1"
}


function usage() {
	echo -e "$USAGE\n"
}

function up() {
	python bot.py
	exit 0
}

function install() {
	docker pull python:3
	docker pull node
	docker pull bash
	docker pull php:7.4-cli
	docker build -t python-custom manifests/python
	python -m pip install -r requirements.txt
	exit 0
}

function clean() {
	echo "y" | docker system prune -a
	rm -f poll/*
	exit 0
}

if [ -z "$1" ]; then
	usage
	exit 1
fi

case "$ARG" in
"up")
	up
	;;
"clean")
	clean
	;;
"install")
	install
	;;
*)
	usage
	exit 1
	;;
esac
