#!/bin/bash

RED='\033[0;31m'
ORANGE='\033[0;33m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
DARK_GRAY='\033[1;30m'
NC='\033[0m'

ARG="$1"
IMAGE_NAME="thexecutor"
CONTAINER_NAME="thexecutor_live"

USAGE=$(
	cat <<USAGE_STRING

setup.sh up | down | clean --

	\`up'	:
		Build docker image and run the container as a detach process.

	\`down'	:
		Kill main container if exists.

	\`clean' :
		Clear docker cache.

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

function up() {
	if docker run -it -d --rm -v /var/run/docker.sock:/var/run/docker.sock --name "$CONTAINER_NAME" "$IMAGE_NAME" &>/dev/null; then

		success "Running $CONTAINER_NAME container"
	else
		if docker ps | grep -q thexecutor_live; then
			danger "Failed running $CONTAINER_NAME container already running"
			danger "$(echo -e "\tRun the following command :")"
			danger "$(echo -e "\t\tsetup.sh down")"
		else
			danger "Failed running $CONTAINER_NAME container"
		fi

		exit 1
	fi

	exit 0
}

function down() {

	if docker ps | grep -q "$CONTAINER_NAME"; then
		if docker container kill "$CONTAINER_NAME" &>/dev/null; then
			success "Killing $CONTAINER_NAME"
		else
			danger "Killing $CONTAINER_NAME failed"
			exit 1
		fi
	fi

	exit 0
}

function clean() {
	echo "y" | docker system prune -a

	exit 0
}

function usage() {
	echo -e "$USAGE\n"
}

function install() {
	# Create network
	docker network create -d bridge dockerd-network

	# Build docker deamon image so my image can use it
	docker run --privileged --name docker-deamon -d \
		--network dockerd-network --network-alias docker \
		-e DOCKER_TLS_CERTDIR=/certs \
		-v docker-deamon-certs-ca:/certs/ca \
		-v docker-deamon-certs-client:/certs/client \
		docker:dind

	if docker build -t "$IMAGE_NAME" . ; then
		success "Build $IMAGE_NAME image"
	else
		danger "Failed building $IMAGE_NAME image"
	fi
}

if [ -z "$1" ]; then
	usage
	exit 1
fi

case "$ARG" in
"up")
	up
	;;
"down")
	down
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
