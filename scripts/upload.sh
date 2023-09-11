#!/bin/bash

rsync -auP . /run/media/$USER/CIRCUITPY --exclude '.git'
