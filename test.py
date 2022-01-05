import PySimpleGUI as sg
import time
from gpiozero import LED, Button
from gpiozero.pins.pigpio import PiGPIOFactory
import random

factory = PiGPIOFactory(host='192.168.50.30')

led0 = LED(20, pin_factory=factory)
led1 = LED(19, pin_factory=factory)
led2 = LED(26, pin_factory=factory)

button0 = Button(5, pin_factory=factory)
button1 = Button(6, pin_factory=factory)
button2 = Button(13, pin_factory=factory)

leds = [led0, led1, led2]
pad = {led0: button0,
       led1: button1,
       led2: button2}


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
                                 '50 seconds', '60 seconds'), default_value='10 seconds', readonly=True, key='-MOVEMENT-TIMER-', pad=10, font='Any 20')]]

    # Duration
    duration_left_col = [[sg.Text('Minutes', font='Any 20')],
                         [sg.Combo([i for i in range(0, 6)], default_value='1', readonly=True, key='-MINUTES-', font='Any 20', pad=10)]]

    duration_right_col = [[sg.Text('Seconds', font='Any 20')],
                          [sg.Combo([i for i in range(0, (4+1)*15, 15)], default_value='0', readonly=True, key='-SECONDS-', font='Any 20', pad=10)]]

    duration_frame = [[sg.Column(duration_left_col, element_justification='center', pad=10), sg.Column(
        duration_right_col, element_justification='center', pad=10)]]

    # Score
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
    # Duration timer
    remaining_duration_frame = [
        [sg.Text('Start!', key='-REMAINING-DURATION-', pad=10, font='Any 20')]]

    # Movement Timer
    remaining_movement_frame = [
        [sg.Text('Start!', key='-REMAINING-TIMER-', pad=10, font='Any 20')]]

    # End Score
    end_score_frame = [
        [sg.Text('0', key='-CURRENT-SCORE-', pad=10, font='Any 20')]]

    left_col2 = [[sg.Frame(' Remaining Time ', remaining_duration_frame, element_justification='center', font='Any 24', pad=10)],
                 [sg.Button(' Pause ', key='-RUN-PAUSE-', font='Any 20', pad=10)]]

    right_col2 = [[sg.Frame(' Movement Timer ', remaining_movement_frame, element_justification='center', font='Any 24', pad=10)],
                  [sg.Button(' End ', key='-END-', font='Any 20', pad=10)]]

    layout = [[sg.Text('Session In Progress', font=(any, 30), key='-TITLE-', pad=5)],
              [sg.Column(left_col2, element_justification='center'),
               sg.Column(right_col2, element_justification='center')],
              [sg.Frame(' Score ', end_score_frame, element_justification='center', font='Any 24', pad=10)],
              [sg.Button(' Continue ', key='-CONTINUE-', font='Any 20', pad=10)]]
    return sg.Window('Floor Pad', layout, size=(800, 480), element_justification="center", finalize=True)

# start off with 1 window open
window1, window2 = make_win1(), None
# window1.Maximize()
win2_active = False

while True:
    window, event, values = sg.read_all_windows()
    elapsed_time, paused_time, paused = 0, 0, False
    d_start_time = time_as_int()
    m_start_time = time_as_int()
    # --------- Window Exit --------
    if event == sg.WIN_CLOSED or event == ' Exit ':
        window1.close()
        break
    elif event == '-SUBMIT-':
        # if values['-MODE-'] == 'Chair':
        #     sg.popup('You Chose Chair Mode',
        #              'Place a chair on the floor pad.')

        # Timers in seconds
        mins_duration = values['-MINUTES-']
        secs_duration = values['-SECONDS-']
        m_timer = values['-MOVEMENT-TIMER-']
        movement_value = int(m_timer[:2])
        movement_timer = movement_value
        overall_duration = (mins_duration * 60) + secs_duration
        
        window2 = make_win2()
        session_end = False
        win2_active = True
        # window2.Maximize()

    previous = None
    current_led = random.choice(leds)
    ms_count = 0
    score = 0
    

    # window2
    while win2_active:
        # --------- Read and update window --------
        if not paused:
            event, values = window2.read(timeout=10)
            # Duration timer
            d_elapsed_time = time_as_int() - d_start_time
            duration_timer = overall_duration - (d_elapsed_time // 100)
            # Movement timer
            m_elapsed_time = time_as_int() - m_start_time
            movement_timer = movement_value - (m_elapsed_time // 100)
        else:
            event, values = window2.read()

        # --------- Do Button Operations --------
        if event in (sg.WIN_CLOSED, '-END-', '-CONTINUE-'):
            print(current_led)
            window2.close()
            print('EXITING SESSION WINDOW')
            win2_active = False
        elif event == '-RUN-PAUSE-':
            paused = not paused
            if paused:
                paused_time = time_as_int()
            else:
                d_start_time = d_start_time + time_as_int() - paused_time
                m_start_time = m_start_time + time_as_int() - paused_time
            # Change Button Text
            window2['-RUN-PAUSE-'].update(' Run ' if paused else ' Pause ')

        # Movement Timer Complete
        if movement_timer == 0:
            print('Movement Timer Complete')
            # Session Complete: Movement timer greater than remaining duration
            if movement_value > duration_timer:
                paused = True
                session_end = True
                current_led.off()
                window2['-TITLE-'].update('Session Complete')
                window2['-RUN-PAUSE-'].update(disabled = True)
                window2['-END-'].update(disabled = True)
                print('ENDING SESSION: movement timer greater than remaining duration')
            # Movement timer less than or equal to remaining duration -> Reset movement timer and continue
            else:
                print("reset movement timer")
                movement_timer = movement_value
                m_start_time = time_as_int() 
        # Session Complete: duration timer ran out
        elif duration_timer == 0:
            paused = True
            session_end = True
            current_led.off()
            window2['-TITLE-'].update('Session Complete')
            window2['-RUN-PAUSE-'].update(disabled = True)
            window2['-END-'].update(disabled = True)
            print('ENDING SESSION: duration timer ran out')
            
        if current_led != previous:
            current_led.on()
            # correct button pressed
            if (pad[current_led].is_pressed):
                print("pressed" + str(current_led.pin))
                current_led.off()
                previous = current_led
                current_led = random.choice(leds)
                score += 1
                window2['-CURRENT-SCORE-'].update(score)
                movement_timer = movement_value
                m_start_time = time_as_int()
        else:
            current_led = random.choice(leds)
            movement_timer = movement_value
            
        window2['-REMAINING-DURATION-'].update('{:02d}:{:02d}'.format(duration_timer // 60, duration_timer % 60))
        window2['-REMAINING-TIMER-'].update('{:02d}:{:02d}'.format(movement_timer // 60, movement_timer % 60))

window.close()

# todo: 
# current led stays on after exiting window2 / when script ends