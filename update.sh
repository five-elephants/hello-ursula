#!/bin/bash

git fetch

if [ $(git rev-parse HEAD) != $(git rev-parse @{u}) ] ; then
	echo "Updating"
	git pull

	echo "Restarting service"
	systemctl restart hello-ursula
fi
