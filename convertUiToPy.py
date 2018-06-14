"""
Script to convert a Qt5 .ui file to a .py file to be used with PyQt5.
"""
from PyQt5 import uic

# Enter file here.
QT_CREATOR_FILE = 'sudokuGUI.ui'
OUTPUT_PYTHON_FILE = "sudokuGUI.py"


def main():
    textFile = open(OUTPUT_PYTHON_FILE, "w")
    uic.compileUi(QT_CREATOR_FILE, textFile, True)
    textFile.close()
    print("Conversion done.")

if __name__ == '__main__':
    main()
