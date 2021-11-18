import PySimpleGUI as sg
from gpiozero import LED
import time

# # session countdown
def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        t -= 1 


# main
def main():
    # Theme
    sg.theme('GreenTan')

    # Mode
    frame_1 = [[sg.Combo(('Standing', 'Chair'),
                     default_value='Standing', readonly=True, key='-MODE-')]]

    # Movement Timer
    frame_2 = [[sg.Combo(('10 seconds', '20 seconds', '30 seconds', '40 seconds',
                     '50 seconds', '60 seconds'), default_value='10 seconds', readonly=True, key='-TIMER-')]]

    # Session Duration
    frame_3 = [[sg.Text('Minutes')],
           [sg.Combo([i for i in range(1, 6)], default_value='1',
                     readonly=True, key='-MINUTES-')],
           [sg.Text('Seconds')],
           [sg.Combo([i for i in range(0, (4+1)*15, 15)], default_value='0', readonly=True, key='-SECONDS-')]]

    # Layout
    layout = [[sg.Text('Create a New Session', font=('Helvetica', 20))],
          [sg.Frame('Mode', frame_1, font='Any 12')],
          [sg.Frame('Movement Timer', frame_2, font='Any 12')],
          [sg.Frame('Session Duration', frame_3, font='Any 12')],
          [sg.Checkbox('Display Score', default=False, key='-SCORE-')],
          [sg.Button('Submit'), sg.Button('Cancel')]]

    window = sg.Window('Floor Pad', layout, size=(800, 480), element_justification="center", finalize=True)
    window.Maximize()

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
            print('Closing window')
            break

        if event == 'Submit':
            print(values)

            mode = values['-MODE-']

            minutes = values['-MINUTES-']
            seconds = values['-SECONDS-']
            totalSeconds = (minutes * 60) + seconds
            print(totalSeconds)

            while totalSeconds:
                mins, secs = divmod(totalSeconds, 60)
                timeformat = '{:02d}:{:02d}'.format(mins, secs)
                print(timeformat, end='\r')
                time.sleep(1)
                totalSeconds -= 1 


            # countdown(minutes, seconds)
            movementTimer = int(values['-TIMER-'][:2])
            score = values['-SCORE-']

    window.close()


if __name__ == "__main__":
    main()