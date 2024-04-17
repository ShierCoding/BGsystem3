@echo off

set PATH=%~dp0python-embed-amd64\;%PATH%;%~dp0python-embed-amd64\

cd ./BGsystem3-server

python --version

python main.py