#sudo apt-get install python3-pyqt5
import os
import sys
from PyQt5.QtWidgets import QApplication
from sudokuGUI import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets

def main():
    #Setup GUI
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    #Generate sudoku matrix
    matrix = generateSudokumatrix()

    index = 0
    continue_running = True
    while continue_running == True:
        found_new_placeable = False
        for ii in range(9):
            index = index+1
            for jj in range(9):
                result = checkCellFillable(matrix, ii, jj)
                matrix = result['mat']
                was_fillable = result['was_fillable']
                if(was_fillable == True):
                    found_new_placeable = True
                    fill_gui_matrix(ui, matrix)
        print("Did we find a new cell to add:"+str(found_new_placeable))
        if(found_new_placeable == False):
            matrix = elimination_by_row(matrix)
            input()
            continue_running = True
    fill_gui_matrix(ui, matrix)
    sys.exit(app.exec_())
    #print(matrix)

def elimination_by_row(matrix):
    for row in range(9):
        matrix = check_row_by_elimination(matrix,row)
    return matrix

def check_row_by_elimination(matrix, row):
    """
    Go through all places in the row and see if we can find single place to add the number
    """
    #Check which values are available in the row
    availableNumbers = [True, True, True, True, True, True, True, True, True]
    availableNumbers = invertArrayNumbers(checkRowNumbers(matrix, row, availableNumbers))
    #print("\nrow:"+str(row)+" available numbers:"+str(availableNumbers))

    #Check which slots are available
    availablePositionsInRow = checkRowPositionsAvailable(matrix, row)
    #input()
    if (checkAllFalse(availablePositionsInRow) == False): #Check if some value is available
        for number in range(1,10,1):
            if(availableNumbers[number-1] == True):
                numberOfAvailablePlaces = [False, False, False, False, False, False, False, False, False]
                #The number is available check all columns with this specific value and
                #see if there is only one place it can be located
                for column in range(9):
                    #Check if the column location is filled
                    if(matrix[row][column] != None):
                        #The column location already have a value, so it is not a possible position
                        numberOfAvailablePlaces[column] = False
                    else:
                        #The column location does not have a value, check if we can place the number here
                        availableNumbersInColumn = [True, True, True, True, True, True, True, True, True]
                        availableNumbersInColumn = invertArrayNumbers(checkColumnNumbers(matrix, column, availableNumbersInColumn))
                        availableNumbersInSection = [True, True, True, True, True, True, True, True, True]
                        availableNumbersInSection = invertArrayNumbers(checkSectionNumbers(matrix,row, column, availableNumbersInSection))
                        #print("availableNumbersInColumn:"+str(availableNumbersInColumn))
                        #print("availableNumbersInSection:"+str(availableNumbersInSection)+"\n")
                        #input()

                        if(checkIfNumberIsAvailable(number, availableNumbersInColumn) == True and checkIfNumberIsAvailable(number, availableNumbersInSection) == True):
                            print("number:"+str(number)+" is available in column:"+str(column))
                            numberOfAvailablePlaces[column] = True
                        else:
                            numberOfAvailablePlaces[column] = False
                #We have gone through all column locations check if there is only one possible place
                if(checkOnlyOnePossiblePlace(numberOfAvailablePlaces) == True):
                    #Only one possible place, therefore place it there
                    columnToPlaceNumber = getSinglePossibleLocation(numberOfAvailablePlaces)
                    print("***** Placed value ****\nrow:"+str(row)+"\ncolumn:"+str(columnToPlaceNumber)+"\nnumber:"+str(number)+"\n"+"numberOfAvailablePlaces:"+str(numberOfAvailablePlaces)+"\ngetSinglePossibleLocation(numberOfAvailablePlaces)"+str(getSinglePossibleLocation(numberOfAvailablePlaces)))
                    input()
                    matrix[row][columnToPlaceNumber] = number

    return matrix





def fill_gui_matrix(ui, matrix):
    for row in range(9):
        for column in range(9):
            print("row"+str(row))
            print("column"+str(column))
            matrix_to_btn(ui,row,column).setText(str(matrix[row][column]))


def matrix_to_btn(ui, row, column):
    """
    Takes row column values and returns the button
    """
    if(row == 0 and column == 0):
        return ui.btn_0_0
    elif(row == 0 and column == 1):
        return ui.btn_0_1
    elif(row == 0 and column == 2):
        return ui.btn_0_2
    elif(row == 0 and column == 3):
        return ui.btn_0_3
    elif(row == 0 and column == 4):
        return ui.btn_0_4
    elif(row == 0 and column == 5):
        return ui.btn_0_5
    elif(row == 0 and column == 6):
        return ui.btn_0_6
    elif(row == 0 and column == 7):
        return ui.btn_0_7
    elif(row == 0 and column == 8):
        return ui.btn_0_8
    elif(row == 1 and column == 0):
        return ui.btn_1_0
    elif(row == 1 and column == 1):
        return ui.btn_1_1
    elif(row == 1 and column == 2):
        return ui.btn_1_2
    elif(row == 1 and column == 3):
        return ui.btn_1_3
    elif(row == 1 and column == 4):
        return ui.btn_1_4
    elif(row == 1 and column == 5):
        return ui.btn_1_5
    elif(row == 1 and column == 6):
        return ui.btn_1_6
    elif(row == 1 and column == 7):
        return ui.btn_1_7
    elif(row == 1 and column == 8):
        return ui.btn_1_8
    elif(row == 2 and column == 0):
        return ui.btn_2_0
    elif(row == 2 and column == 1):
        return ui.btn_2_1
    elif(row == 2 and column == 2):
        return ui.btn_2_2
    elif(row == 2 and column == 3):
        return ui.btn_2_3
    elif(row == 2 and column == 4):
        return ui.btn_2_4
    elif(row == 2 and column == 5):
        return ui.btn_2_5
    elif(row == 2 and column == 6):
        return ui.btn_2_6
    elif(row == 2 and column == 7):
        return ui.btn_2_7
    elif(row == 2 and column == 8):
        return ui.btn_2_8
    elif(row == 3 and column == 0):
        return ui.btn_3_0
    elif(row == 3 and column == 1):
        return ui.btn_3_1
    elif(row == 3 and column == 2):
        return ui.btn_3_2
    elif(row == 3 and column == 3):
        return ui.btn_3_3
    elif(row == 3 and column == 4):
        return ui.btn_3_4
    elif(row == 3 and column == 5):
        return ui.btn_3_5
    elif(row == 3 and column == 6):
        return ui.btn_3_6
    elif(row == 3 and column == 7):
        return ui.btn_3_7
    elif(row == 3 and column == 8):
        return ui.btn_3_8
    elif(row == 4 and column == 0):
        return ui.btn_4_0
    elif(row == 4 and column == 1):
        return ui.btn_4_1
    elif(row == 4 and column == 2):
        return ui.btn_4_2
    elif(row == 4 and column == 3):
        return ui.btn_4_3
    elif(row == 4 and column == 4):
        return ui.btn_4_4
    elif(row == 4 and column == 5):
        return ui.btn_4_5
    elif(row == 4 and column == 6):
        return ui.btn_4_6
    elif(row == 4 and column == 7):
        return ui.btn_4_7
    elif(row == 4 and column == 8):
        return ui.btn_4_8
    elif(row == 5 and column == 0):
        return ui.btn_5_0
    elif(row == 5 and column == 1):
        return ui.btn_5_1
    elif(row == 5 and column == 2):
        return ui.btn_5_2
    elif(row == 5 and column == 3):
        return ui.btn_5_3
    elif(row == 5 and column == 4):
        return ui.btn_5_4
    elif(row == 5 and column == 5):
        return ui.btn_5_5
    elif(row == 5 and column == 6):
        return ui.btn_5_6
    elif(row == 5 and column == 7):
        return ui.btn_5_7
    elif(row == 5 and column == 8):
        return ui.btn_5_8
    elif(row == 6 and column == 0):
        return ui.btn_6_0
    elif(row == 6 and column == 1):
        return ui.btn_6_1
    elif(row == 6 and column == 2):
        return ui.btn_6_2
    elif(row == 6 and column == 3):
        return ui.btn_6_3
    elif(row == 6 and column == 4):
        return ui.btn_6_4
    elif(row == 6 and column == 5):
        return ui.btn_6_5
    elif(row == 6 and column == 6):
        return ui.btn_6_6
    elif(row == 6 and column == 7):
        return ui.btn_6_7
    elif(row == 6 and column == 8):
        return ui.btn_6_8
    elif(row == 7 and column == 0):
        return ui.btn_7_0
    elif(row == 7 and column == 1):
        return ui.btn_7_1
    elif(row == 7 and column == 2):
        return ui.btn_7_2
    elif(row == 7 and column == 3):
        return ui.btn_7_3
    elif(row == 7 and column == 4):
        return ui.btn_7_4
    elif(row == 7 and column == 5):
        return ui.btn_7_5
    elif(row == 7 and column == 6):
        return ui.btn_7_6
    elif(row == 7 and column == 7):
        return ui.btn_7_7
    elif(row == 7 and column == 8):
        return ui.btn_7_8
    elif(row == 8 and column == 0):
        return ui.btn_8_0
    elif(row == 8 and column == 1):
        return ui.btn_8_1
    elif(row == 8 and column == 2):
        return ui.btn_8_2
    elif(row == 8 and column == 3):
        return ui.btn_8_3
    elif(row == 8 and column == 4):
        return ui.btn_8_4
    elif(row == 8 and column == 5):
        return ui.btn_8_5
    elif(row == 8 and column == 6):
        return ui.btn_8_6
    elif(row == 8 and column == 7):
        return ui.btn_8_7
    elif(row == 8 and column == 8):
        return ui.btn_8_8

def generateSudokumatrix():
    c, r = 9, 9;
    matrix = [[0 for x in range(c)] for y in range(r)]
    matrix = fillSudokuArray(matrix)
    return matrix

def fillSudokuArray(matrix):
    #Easy1
    #matrix = fillSudokuRow(matrix, 0, 5,    None, 4,    7,    1,    3,    None, 9,    None)
    #matrix = fillSudokuRow(matrix, 1, 9,    None, None, None, None, 6,    None, None, None)
    #matrix = fillSudokuRow(matrix, 2, None, 2,    None, None, 8,    None, 6,    None, None)
    #matrix = fillSudokuRow(matrix, 3, 8,    7,    None, None, 4,    None, None, None, 9)
    #matrix = fillSudokuRow(matrix, 4, None, 1,    6,    9,    None, 8,    3,    7,    None)
    #matrix = fillSudokuRow(matrix, 5, 2,    None, None, None, 6,    None, None, 4,    8)
    #matrix = fillSudokuRow(matrix, 6, None, None, 2,    None, 7,    None, None, 3,    None)
    #matrix = fillSudokuRow(matrix, 7, None, None, None, 5,    None, None, None, None, 6)
    #matrix = fillSudokuRow(matrix, 8, None, 3,    None, 6,    9,    2,    7,    None, 4)

    #Easy2
    #matrix = fillSudokuRow(matrix, 0, 5, None, None, 9,1,None,7, None,  None)
    #matrix = fillSudokuRow(matrix, 1, None, None,9,None,4,None,None,2,None)
    #matrix = fillSudokuRow(matrix, 2, 4,6,None,None,None,None,None,9,5)
    #matrix = fillSudokuRow(matrix, 3, 2,7,None,None,9,None,3,None,8)
    #matrix = fillSudokuRow(matrix, 4, 8,5,None,None,None,None,None,6,9)
    #matrix = fillSudokuRow(matrix, 5, 1,None,4,None,3,None,None,5,7)
    #matrix = fillSudokuRow(matrix, 6, 6,8,None,None,None,None,None,7,2)
    #matrix = fillSudokuRow(matrix, 7, None,3,None,None,6,None,5,None,None)
    #matrix = fillSudokuRow(matrix, 8, None,None,5,None,2,7,None,None,3)

    #Hard1
    matrix = fillSudokuRow(matrix, 0, None,  None,  4,  None,  None,  None,  2,  8,  None)
    matrix = fillSudokuRow(matrix, 1, 1,  5,  None,  2,  3,  None,  None,  None,  7)
    matrix = fillSudokuRow(matrix, 2, None,  None,  None,  None,  None,  1,  9,  5,  3)
    matrix = fillSudokuRow(matrix, 3, None,  None,  None,  3,  None,  None,  None,  None,  None)
    matrix = fillSudokuRow(matrix, 4, 8,  None,  3,  None,  5,  None,  1,  None,  6)
    matrix = fillSudokuRow(matrix, 5, None,  None,  None,  None,  None,  7,  None,  None,  None)
    matrix = fillSudokuRow(matrix, 6, 7,  6,  5,  9,  None,  None,  None,  None,  None)
    matrix = fillSudokuRow(matrix, 7, 4,  None,  None,  None,  1,  6,  None,  3,  9)
    matrix = fillSudokuRow(matrix, 8, None,  1,  9,  None,  None,  None,  6,  None,  None)

    return matrix

def fillSudokuRow(matrix, row, value0, value1, value2, value3, value4, value5, value6, value7, value8):
    matrix[row][0] = value0
    matrix[row][1] = value1
    matrix[row][2] = value2
    matrix[row][3] = value3
    matrix[row][4] = value4
    matrix[row][5] = value5
    matrix[row][6] = value6
    matrix[row][7] = value7
    matrix[row][8] = value8
    return matrix

def checkCellFillable(matrix, row, column):
    """
    Check if the cell is fillable
    """
    if(matrix[row][column] != None):
        return {'mat':matrix, 'was_fillable':False}
    availableNumbers = [True, True, True, True, True, True, True, True, True]

    #Go through column to see what values can NOT be placed
    availableNumbers = checkColumnNumbers(matrix, column, availableNumbers)

    #Go through rows to see what values can NOT be placed
    availableNumbers = checkRowNumbers(matrix, row, availableNumbers)

    #Go through section to see what values can NOT be placed
    availableNumbers = checkSectionNumbers(matrix, row, column, availableNumbers)

    total = 0
    for ii in range(9):
        if availableNumbers[ii] == True:
            total = total+1

    if (total == 1):
        print("Found single one r:"+str(row)+" c:"+str(column)+" value:"+str(convertArrayToNumber(availableNumbers)))
        matrix[row][column] = convertArrayToNumber(availableNumbers)
        prettyPrintMatrix(matrix)
        return {'mat':matrix, 'was_fillable':True}
    return {'mat':matrix, 'was_fillable':False}

def singleAvailableNumber(availableNumbers):
    total = 0
    for ii in range(9):
        if availableNumbers[ii] == True:
            total = total+1
    if (total == 1):
        return convertArrayToNumber(availableNumbers)
    else:
        return False


def convertArrayToNumber(availableNumbers):
    """
    Converts the "availableNumbers" array into an actual integer. This can ONLY be used when there is only value left in availableNumbers.
    """
    if availableNumbers[0] == True:
        return 1
    elif availableNumbers[1] == True:
        return 2
    elif availableNumbers[2] == True:
        return 3
    elif availableNumbers[3] == True:
        return 4
    elif availableNumbers[4] == True:
        return 5
    elif availableNumbers[5] == True:
        return 6
    elif availableNumbers[6] == True:
        return 7
    elif availableNumbers[7] == True:
        return 8
    elif availableNumbers[8] == True:
        return 9
    else:
        return None

def prettyPrintMatrix(matrix):
    s = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print ('\n'.join(table))

def checkAllFalse(arrayOfNumbers):
    """
    Checks whether all numbers are false, i.e. none available
    """
    for index in range(len(arrayOfNumbers)):
        if(arrayOfNumbers[index] == True):
            return False
    return True

def checkOnlyOnePossiblePlace(arrayOfNumbers):
    """
    Checks if there is one and only one possible location
    """
    nrOfPossibleNumbers = 0
    for index in range(len(arrayOfNumbers)):
        if(arrayOfNumbers[index] == True):
            nrOfPossibleNumbers = nrOfPossibleNumbers+1
    if(nrOfPossibleNumbers == 1):
        return True
    else:
        return False

def getSinglePossibleLocation(arrayOfNumbers):
    for locationNumber in range(0,9,1):
        if(arrayOfNumbers[locationNumber] == True):
            return locationNumber
    return None

def checkRowPositionsAvailable(matrix, row):
    """
    Go through the positions in the rown and return a list of the available ones
    """
    availablePositions = [False, False, False, False, False, False, False, False, False]
    for index in range(9):
        if(matrix[row][index] == None):
            availablePositions[index] = True
    return availablePositions

def checkColumnPositionsAvailable(matrix, column):
    """
    Go through the positions in the rown and return a list of the available ones
    """
    availablePositions = [False, False, False, False, False, False, False, False, False]
    for index in range(9):
        if(matrix[index][column] == None):
            availablePositions[index] = True
    return availablePositions

def invertArrayNumbers(arrayOfNumbers):
    for index in range(len(arrayOfNumbers)):
        if(index == True):
            index = False
        else:
            index = True
    return arrayOfNumbers


def checkRowNumbers(matrix, row, availableNumbers):
    """
    Go through all values in the row and remove the ones already used
    """
    #print("Check row values")
    for ii in range(9):
        #print("Row values")
        #print(matrix[row][ii])
        if  (matrix[row][ii] == 1):
            availableNumbers[0] = False
        elif(matrix[row][ii] == 2):
            availableNumbers[1] = False
        elif(matrix[row][ii] == 3):
            availableNumbers[2] = False
        elif(matrix[row][ii] == 4):
            availableNumbers[3] = False
        elif(matrix[row][ii] == 5):
            availableNumbers[4] = False
        elif(matrix[row][ii] == 6):
            availableNumbers[5] = False
        elif(matrix[row][ii] == 7):
            availableNumbers[6] = False
        elif(matrix[row][ii] == 8):
            availableNumbers[7] = False
        elif(matrix[row][ii] == 9):
            availableNumbers[8] = False
    return availableNumbers

def checkColumnNumbers(matrix, column, availableNumbers):
    """
    Go through all values in the column and remove the ones already used
    """
    #print("Check column values")
    for ii in range(9):
        #print("column values")
        #print(matrix[ii][column])
        if  (matrix[ii][column] == 1):
            availableNumbers[0] = False
        elif(matrix[ii][column] == 2):
            availableNumbers[1] = False
        elif(matrix[ii][column] == 3):
            availableNumbers[2] = False
        elif(matrix[ii][column] == 4):
            availableNumbers[3] = False
        elif(matrix[ii][column] == 5):
            availableNumbers[4] = False
        elif(matrix[ii][column] == 6):
            availableNumbers[5] = False
        elif(matrix[ii][column] == 7):
            availableNumbers[6] = False
        elif(matrix[ii][column] == 8):
            availableNumbers[7] = False
        elif(matrix[ii][column] == 9):
            availableNumbers[8] = False
    return availableNumbers

def checkIfNumberIsAvailable(number, availableNumbers):
    #print(number)
    #input()
    if(availableNumbers[number-1] == True): #TODO shouldnt it be number+1?
        #print("number"+str(number)+" availableNumbers:"+str(availableNumbers))
        return True
    else:
        return False

def checkBothRowColumnNumbers(matrix, row, column, availableNumbers):
    """
    Go through both rows and columns
    """
    availableNumbers = checkColumnNumbers(matrix, column, availableNumbers)
    availableNumbers = checkRowNumbers(matrix, row, availableNumbers)
    return availableNumbers

def checkSectionNumbers(matrix, row, column, availableNumbers):
    """
    Checks wich section a particular cell belongs to and then check which values are already taken.
    Returns an array with available numbers
    """
    #print("Check section values")
    #Check which section the cell belongs to
    section = None
    rowAdd = 0
    columnAdd = 0

    #First check what section the number belongs to
    if(row <= 2):
        if(column <= 2):
            section = 0
            rowAdd = 0
            columnAdd = 0
        elif(column <= 5):
            section = 1
            rowAdd = 0
            columnAdd = 3
        else:
            section = 2
            rowAdd = 0
            columnAdd = 6
    elif(row <= 5):
        if(column <= 2):
            section = 3
            rowAdd = 3
            columnAdd = 0
        elif(column <= 5):
            section = 4
            rowAdd = 3
            columnAdd = 3
        else:
            section = 5
            rowAdd = 3
            columnAdd = 6
    else:
        if(column <= 2):
            section = 6
            rowAdd = 6
            columnAdd = 0
        elif(column <= 5):
            section = 7
            rowAdd = 6
            columnAdd = 3
        else:
            section = 8
            rowAdd = 6
            columnAdd = 6

    #if(row==8 and column == 3):
    #    print(section)
    #print("Row min:"+str(rowAdd))
    #print("Column min:"+str(columnAdd))

    #Check the cells in the section
    for ii in range(rowAdd, rowAdd+3):
        for jj in range(columnAdd, columnAdd+3):

            #if(row==8 and column == 3):
            #    print(ii,jj)
            #print("column values")
            #print(matrix[ii][jj])
            if  (matrix[ii][jj] == 1):
                availableNumbers[0] = False
            elif(matrix[ii][jj] == 2):
                availableNumbers[1] = False
            elif(matrix[ii][jj] == 3):
                availableNumbers[2] = False
            elif(matrix[ii][jj] == 4):
                availableNumbers[3] = False
            elif(matrix[ii][jj] == 5):
                availableNumbers[4] = False
            elif(matrix[ii][jj] == 6):
                availableNumbers[5] = False
            elif(matrix[ii][jj] == 7):
                availableNumbers[6] = False
            elif(matrix[ii][jj] == 8):
                availableNumbers[7] = False
            elif(matrix[ii][jj] == 9):
                availableNumbers[8] = False

    return availableNumbers

if __name__ == "__main__":
    main()
