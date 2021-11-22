import PySimpleGUI as sg

sg.theme('GreenTan')

# First window
def make_win1():
    ############### Pre-Session ###############
    # Mode
    mode_frame = [[sg.Combo(('Standing', 'Chair'),
                        default_value='Standing', readonly=True, key='-MODE-', pad=10, font='Any 20')]]

    # Movement Timer
    movement_frame = [[sg.Combo(('10 seconds', '20 seconds', '30 seconds', '40 seconds',
                             '50 seconds', '60 seconds'), default_value='10 seconds', readonly=True, key='-TIMER-', pad=10, font='Any 20')]]

    # Duration
    duration_left_col = [[sg.Text('Minutes', font='Any 20')],
                     [sg.Combo([i for i in range(1, 6)], default_value='1', readonly=True, key='-MINUTES-', font='Any 20', pad=10)]]

    duration_right_col = [[sg.Text('Seconds', font='Any 20')],
                      [sg.Combo([i for i in range(0, (4+1)*15, 15)], default_value='0', readonly=True, key='-SECONDS-', font='Any 20', pad=10)]]

    duration_frame = [[sg.Column(duration_left_col, element_justification='center', pad=10), sg.Column(duration_right_col, element_justification='center', pad=10)]]

    score_frame = [[sg.Checkbox('Display Score', default=False, pad=38, key='-SCORE-', font='Any 20')]]

    left_col1 = [[sg.Frame(' Mode ', mode_frame, element_justification='center', font='Any 24', pad=10)],
            [sg.Frame(' Duration ', duration_frame, font='Any 24', pad=10)],
            [sg.Button(' Submit ', font='Any 20', pad=10)]]

    right_col1 = [[sg.Frame(' Movement Timer ', movement_frame, element_justification='center', font='Any 24', pad=10)],
        [sg.Frame(' Score ', score_frame, element_justification='center', font='Any 24', pad=10)],
        [sg.Button(' Exit ', font='Any 20', pad=10)]]

    layout = [[sg.Text('Create a New Session', font=(any, 30), pad=5)],
            [sg.Column(left_col1, element_justification='center'), sg.Column(right_col1, element_justification='center')]]
    return sg.Window('Floor Pad', layout, size=(800, 480), element_justification="center", finalize=True)


# Second window
def make_win2():
    # Druation timer
    remaining_duration_frame = [[sg.Text('test', key='-REMAININGDURATION-', pad=10, font='Any 20')]]

    # Movement Timer
    remaining_movement_frame = [[sg.Text('test', key='-REMAININGTIMER-', pad=10, font='Any 20')]]

    # End Score
    end_score_frame = [[sg.Text('test', key='-REMAININGTIMER-', pad=10, font='Any 20')]]

    left_col2 = [[sg.Frame(' Remaining Time ', remaining_duration_frame, element_justification='center', font='Any 24', pad=10)],
            [sg.Button(' Pause ', font='Any 20', pad=10)]]

    right_col2 = [[sg.Frame(' Movement Timer ', remaining_movement_frame, element_justification='center', font='Any 24', pad=10)],
            [sg.Button(' Exit ', font='Any 20', pad=10)]]


    layout = [[sg.Text('Session In Progress', font=(any, 30), key='-TITLE-', pad=5)],
              [sg.Column(left_col2, element_justification='center'), sg.Column(right_col2, element_justification='center')],
              [sg.Frame(' Score ', end_score_frame, element_justification='center', font='Any 24', pad=10)],
              [sg.Button(' Continue ', font='Any 20', pad=10)]]
    return sg.Window('Floor Pad', layout, size=(800, 480), element_justification="center", finalize=True)

window1, window2 = make_win1(), None        # start off with 1 window open

# window1.Maximize()

while True:             # Event Loop
    window, event, values = sg.read_all_windows()
    if event == sg.WIN_CLOSED or event == ' Exit ':
        window.close()
        if window == window2:       # if closing win 2, mark as closed
            window2 = None
        elif window == window1:     # if closing win 1, exit program
            break
    elif event == 'Popup':
        sg.popup('This is a BLOCKING popup',
                 'all windows remain inactive while popup active')
    elif event == ' Submit ' and not window2:
        window2 = make_win2()
        # window2.Maximize()
    # elif event == ' Erase ':
    #     window['-IN-'].update('')
window.close()
