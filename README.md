# tetris-rnn
Joseph Hines and John Zlotek

# Usage

Requires python3 and virtualenv, make preferred

## To install dependencies

`make venv` or `bash install.sh`

## To run the game

`make run-main`

At the end of the game, either press ENTER to
play another, or q to quit.
Data with be gathered into several JSON files,
which can be aggregated with:

`make data`

## To train the model

Given there is a file called default.json at the root of the
project (generated from the previous steps):

`make run-rnn`

## To see the model play

Given there is a model.h5 file (generated from training):

`make model-play`

## To clean

`make clean`
