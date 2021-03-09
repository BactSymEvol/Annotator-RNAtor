#!/bin/python3

from lib.controller import Controller
from gui.mainInterface import startGUI

def main():
    controller = Controller(None)
    startGUI(controller)


if __name__ == "__main__":
    main()

