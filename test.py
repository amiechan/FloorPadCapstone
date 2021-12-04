import PySimpleGUI as sg
import gpiozero
import time

sg.theme('GreenTan')


def time_as_int():
    return int(round(time.time() * 100))

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

    duration_frame = [[sg.Column(duration_left_col, element_justification='center', pad=10), sg.Column(
        duration_right_col, element_justification='center', pad=10)]]

    score_frame = [[sg.Checkbox(
        'Display Score', default=False, pad=38, key='-SCORE-', font='Any 20')]]

    left_col1 = [[sg.Frame(' Mode ', mode_frame, element_justification='center', font='Any 24', pad=10)],
                 [sg.Frame(' Duration ', duration_frame,
                           font='Any 24', pad=10)],
                 [sg.Button(' Submit ', key='-SUBMIT-', font='Any 20', pad=10)]]

    right_col1 = [[sg.Frame(' Movement Timer ', movement_frame, element_justification='center', font='Any 24', pad=10)],
                  [sg.Frame(' Score ', score_frame,
                            element_justification='center', font='Any 24', pad=10)],
                  [sg.Button(' Exit ', font='Any 20', pad=10)]]

    layout = [[sg.Text('Create a New Session', font=(any, 30), pad=5)],
              [sg.Column(left_col1, element_justification='center'), sg.Column(right_col1, element_justification='center')]]
    return sg.Window('Floor Pad', layout, size=(800, 480), element_justification="center", finalize=True)


# Second window
def make_win2():
    # Druation timer
    remaining_duration_frame = [
        [sg.Text('test', key='-REMAINING-DURATION-', pad=10, font='Any 20')]]

    # Movement Timer
    remaining_movement_frame = [
        [sg.Text('test', key='-REMAINING-TIMER-', pad=10, font='Any 20')]]

    # End Score
    end_score_frame = [
        [sg.Text('test', key='-REMAINING-TIMER-', pad=10, font='Any 20')]]

    left_col2 = [[sg.Frame(' Remaining Time ', remaining_duration_frame, element_justification='center', font='Any 24', pad=10)],
                 [sg.Button(' Pause ', key='-RUN-PAUSE-', font='Any 20', pad=10)]]

    right_col2 = [[sg.Frame(' Movement Timer ', remaining_movement_frame, element_justification='center', font='Any 24', pad=10)],
                  [sg.Button(' End ', font='Any 20', pad=10)]]

    layout = [[sg.Text('Session In Progress', font=(any, 30), key='-TITLE-', pad=5)],
              [sg.Column(left_col2, element_justification='center'),
               sg.Column(right_col2, element_justification='center')],
              [sg.Frame(' Score ', end_score_frame,
                        element_justification='center', font='Any 24', pad=10)],
              [sg.Button(' Continue ', font='Any 20', pad=10)]]
    return sg.Window('Floor Pad', layout, size=(800, 480), element_justification="center", finalize=True)


window1, window2 = make_win1(), None        # start off with 1 window open

# window1.Maximize()
# current_time, paused_time, paused = 0, 0, False
# start_time = time_as_int()
win2_active = False

while True:
    window, event, values = sg.read_all_windows()
    current_time, paused_time, paused = 0, 0, False
    start_time = time_as_int()
    # --------- Window Exit --------
    if event == sg.WIN_CLOSED or event == ' Exit ':
        window1.close()    # if closing win 1, exit program
        break
    elif event == '-SUBMIT-':
        # if values['-MODE-'] == 'Chair':
        #     sg.popup('You Chose Chair Mode',
        #              'Place a chair on the floor pad.')
        mins_duration = values['-MINUTES-']
        secs_duration = values['-SECONDS-']

        total_secs_duration = (mins_duration * 60) + secs_duration
        print(total_secs_duration)
        

        print(values)
        window2 = make_win2()
        win2_active = True
        # window2.Maximize()
    elif event == '-RUN-PAUSE-':
        paused = not paused
        if paused:
            paused_time = time_as_int()
        else:
            start_time = start_time + time_as_int() - paused_time
        window['-RUN-PAUSE-'].update(' Run ' if paused else ' Pause ')

    while win2_active:
        if not paused:
            event, values = window2.read(timeout=10)
            current_time = time_as_int() - start_time
        else:
            event, values = window2.read()

        if event == sg.WIN_CLOSED or event == ' End ':
            window2.close()
            print('ENDING SESSION')
            win2_active = False
        elif event == '-RUN-PAUSE-':
            paused = not paused
            if paused:
                paused_time = time_as_int()
            else:
                start_time = start_time + time_as_int() - paused_time
            window2['-RUN-PAUSE-'].update(' Run ' if paused else ' Pause ')

        window2['-REMAINING-DURATION-'].update('{:02d}:{:02d}'.format((current_time // 100) // 60, (current_time // 100) % 60))
        window2['-REMAINING-TIMER-'].update('{:02d}:{:02d}'.format((current_time // 100) // 60, (current_time // 100) % 60))

window.close()

# get total seconds
# divmod(t, 60)
# format timer
# print timer
# sleep 1
# t -= 1
