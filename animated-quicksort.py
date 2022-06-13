'''
animated_quicksort.py - takes an fps value and a string of numbers
                        and produces a sorted list of numbers with
                        a gui window and/or text prints.

Author: Mason Mariani

Full program which will take an input for fps and various numbers and sort
them in ascending order accordingly. Each step of the process can be displayed
in a gui window or by text; the speed at which this information is relayed to
the user depends on the given value for fps. Should the user decide not to use the
gui window, a value of 0 can be used as input to disable its creation, and will instead
only print out the information. Finally, the user can also choose to recieve a random
set of numbers by inputing 'random' followed by the desired length of the list when prompted
to input their data. If no list length value is chosen; 20 will be assigned as the default.
'''

from graphics import graphics
import random
from sys import stdin

class Gui:
    '''
    Class used to store the refrence to the graphics window
    '''
    def __init__(self):
        '''
        Takes no additional paramaters;
        when initilized the method will create a
        gui window.
        '''
        window = graphics(1000, 1000, "Quick Sort")
        self.gui = window
        self.gui.rectangle(0, 0, 1000, 1000, 'whitesmoke')

def returning(data, x, y, gui):
    '''
    data - portion of data which will be drawn
    x - x position on the gui window where the list drawing is started
    y - y position on the gui window where the list drawing is started
    gui - refrence to the gui graphics window which is being drawn on

    clears previous information and draws the list being collapsed onto the previous stack
    '''
    gui.rectangle(0, y, 1000, 1000, 'whitesmoke')
    y -= 100
    draw_array(data, x, y, gui)

def create_lists(data):
    '''
    data - list which is being sorted

    Generates the split in relation to the pivot; where all values less than
    or equal to the pivot are put into the less_than_input list and all
    others into the greater_than_input list. These two lists are then returned
    '''
    less_than_input = []
    greater_than_input = []
    for i in data[1:]:
        if i <= data[0]:
            less_than_input.append(i)
        else:
            greater_than_input.append(i)
    return less_than_input, greater_than_input

def draw_array(data, x, y, gui):
    '''
    data - portion of data which will be drawn
    x - x position on the gui window where the list drawing is started
    y - y position on the gui window where the list drawing is started
    gui - refrence to the gui graphics window which is being drawn on

    draws the array which is currently being sorted
    '''
    for i in data:
        gui.rectangle(x, y, 50, 50, 'black')
        gui.rectangle(x + 2, y + 2, 46, 46, 'white')
        gui.text(x + 5, y + 12, i)
        x += 50
    return x, y

def draw_pivot(data, x, y, gui):
    '''
    data - portion of data which will be drawn
    x - x position on the gui window where the list drawing is started
    y - y position on the gui window where the list drawing is started
    gui - refrence to the gui graphics window which is being drawn on

    draws the pivot value in a shade of red to highlight it
    '''
    gui.rectangle(x, y, 50, 50, 'black')
    gui.rectangle(x + 2, y + 2, 46, 46, 'red')
    gui.text(x + 5, y + 12, data[0])
    x += 50
    return x, y

def create_data(data_input):
    '''
    Takes the string given by the user and generates a list to be sorted
    and returns this list.
    '''
    data_input = data_input.split()
    if data_input[0] == 'random':
        data = []
        if len(data) > 1:
            for i in range(0, int(data_input[1])):
                data.append(random.randint(-50, 100))
        else:
            for i in range(0, 20):
                data.append(random.randint(-50, 100))
    else:
        data = data_input
        for i in range(0, len(data)):
            data[i] = int(data[i])
    return data

def quick_sort(data, fps, x, y, open_gui):
    '''
    data - list which is currently being sorted
    fps - frames per second amount entered by the user
          an input of zero does not produce a gui window
    x - x position on the gui window where the list drawing is started
    y - y position on the gui window where the list drawing is started
    open_gui - bool value used to check if a gui window is open
    gui - refrence to the gui graphics window which is being drawn on

    function called by main for the process of sorting and displaying
    the steps of said process though both a gui window and/or text
    '''
    # base case condition
    if len(data) < 2:
        print(
            "QS: The length of the input data, "
            + str(data)
            + ", is zero or one.  Returning immediately."
        )
        return data

    # drawing initial list before splits
    if open_gui != False:
        x, y = draw_array(data, x, y, open_gui)
        x = 25
        y += 100
        open_gui.update()
        open_gui.frame_space(fps)

    # generates the greater and less than splits in relation to the pivot
    less_than_input, greater_than_input = create_lists(data)

    # draws the next step in recursion; if the gui window is enabled
    if open_gui != False:
        x, y = draw_array(less_than_input, x, y, open_gui)
        x, y = draw_pivot(data, x, y, open_gui)
        x, y = draw_array(greater_than_input, x, y, open_gui)
        open_gui.update()
        open_gui.frame_space(fps)

    # print block when recursing
    print('QS: Data in:', data)
    print('    Pivot:  ', data[0])
    print('    Left:   ', less_than_input)
    print('    Right:  ', greater_than_input)

    y += 100
    x = 25
    # recurse into lesser list then greater list
    less_than = quick_sort(less_than_input, fps, x, y, open_gui)
    greater_than = quick_sort(greater_than_input, fps, x, y, open_gui)
    sorted_data = less_than + [data[0]] + greater_than

    # updating the gui such that lists collapse into previous stack
    if open_gui != False:
        returning(sorted_data, x, y, open_gui)
        open_gui.update()
        open_gui.frame_space(fps)

    # print block when returning
    print('QS: AFTER RECURSION...')
    print('    Original data: ', data)
    print('    Left (sorted): ', less_than)
    print('    Right (sorted):', greater_than)
    print('    Sorted data:   ', sorted_data)

    return sorted_data


def main():
    # get list data from user
    print("Frames per second?  (Give 0 to disable animation.)")
    fps = float(input())
    print("Please give the input data:")

    data_input = []
    line = stdin
    for line in stdin:
        if line:
            data_input.append(line)
        else:
            break
    data_input = '\n'.join(data_input)

    # create the list
    data = create_data(data_input)
    open_gui = False
    if fps != 0:
        window = Gui()
        open_gui = window.gui

    # sort the list
    print("INPUT DATA: " + str(data))
    new_sorted = quick_sort(data, fps, 25, 25, open_gui)
    print("AFTER THE SORT: " + str(new_sorted))


if __name__ == '__main__':
    main()
