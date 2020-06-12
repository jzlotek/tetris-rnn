# tetris-rnn
Joseph Hines and John Zlotek

# Usage

Requires python3 and virtualenv, make preferred

## To install dependencies

`make venv` or `bash install.sh`

Windows:
`python3 -m venv venv && source venv/Scripts/activate && pip install -r requirements.txt`

## To run the game

`make run-main`

Windows:
`source venv/Scripts/activate && python src/main.py`

Put any args after the main.py you want to run
-h is for help

At the end of the game, either press ENTER to
play another, or q to quit.
Data with be gathered into several JSON files,
which can be aggregated with:

`make data`
Windows:
`source venv/Scripts/activate && python src/datatools.py --combine default`

## To train the model

Given there is a file called default.json at the root of the
project (generated from the previous steps):

`make run-rnn`
Windows:
`source venv/Scripts/activate && python src/rnn.py`
Put any args after the rnn.py you want to run
-h is for help

## To see the model play

Given there is a model.h5 file (generated from training):

`make model-play`
Windows:
`source venv/Scripts/activate && python src/main.py -m model.h5`

## To clean

`make clean`
