from tkinter import *
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0                            # reps variable to store the current rep number
timer = None                        # timer variable to be used with the window.after and window.after_cancel methods
timer_running = False               # timer running variable to determine if the timer is running


# ---------------------------- TIMER RESET ------------------------------- #

def reset_timer():
    """function to stop the timer and reset the reps and Labels to default value"""
    global timer_running
    global reps
    reps = 0                                        # resetting the number of reps
    timer_running = False                           # setting timer running variable to False
    window.after_cancel(timer)                      # canceling the current timer
    check_marks.config(text="")                     # removing the current check marks
    label.config(text="Pomodoro")                   # resetting the original title
    canvas.itemconfig(timer_text, text="00:00")     # resetting the counter




# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    """function that starts the timer"""
    global reps
    global timer_running
    if not timer_running:                    # condition to avoid triggering the timer while it is already running
        timer_running = True                 # setting the timer running variable to True
        reps += 1                            # increasing the number of reps
        work_secs = WORK_MIN * 60                   # changing work time from minutes to secs
        long_break_secs = LONG_BREAK_MIN * 60       # changing long break time from minutes to secs
        short_break_secs = SHORT_BREAK_MIN * 60     # changing short break time from minutes to secs

        if reps % 8 == 0:                           # triggering a long break after multiples of 8 reps pass
            label.config(text= "Break", fg=RED)
            count_down(long_break_secs)
        elif reps % 2 == 0:                         # triggering a short break every 2 reps until 8 then a long break is triggered
            label.config(text="Break", fg=PINK)
            count_down(short_break_secs)
        else:                                       # triggering work time
            label.config(text="Work", fg=GREEN)
            count_down(work_secs)



# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #

def count_down(count):
    """function that counts down and updates the timer on screen"""
    global reps
    global timer
    count_min = math.floor(count / 60)        # using the floor method from math module we can get the remaining number of minutes after the division
    count_sec = round(count % 60)             # using mod to determine the number of secs remaining in the fractured minute
    if count_sec < 10:
        count_sec = f"0{count_sec}"           # using dynamic typing to correct the values under 10 to show in 00 format
    if count_min < 10:
        count_min = f"0{count_min}"           # using dynamic typing to correct the values under 10 to show in 00 format



    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")      # displaying the new value for min and secs
    if count > 0:
        timer = window.after(1000, count_down, count - 1)     # recalling the counter if timer remaining > 0
    else:
        start_timer()               # calling the start timer when the timer is done to start the following phase
        marks = ""                  # variable to hold the check marks for displaying
        work_sessions = math.floor(reps/2)      # getting the number of completed sessions
        for _ in range (work_sessions):         # generating a ✓ for every completed session
            marks += "✓"
            check_marks.config(text=marks)

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()                                   # creating a window object from the TK class
window.title("Pomodoro")                        # choosing the window title
window.config(padx=100, pady=50, bg=YELLOW)     # adding padding and choosing background colour for the window


# Creating a canvas for the image
canvas = Canvas(width=202, height=224, bg=YELLOW, highlightthickness=0)         # creating a canvas for the image and setting dimension and colors
tomato = PhotoImage(file="tomato.png")                      # setting the desired image path
canvas.create_image(102, 112, image=tomato)           # loading the image into the canvas
timer_text = canvas.create_text(102, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold")) # over laying the timer text
canvas.grid(row=1, column=1)            # choosing alignment in the grid

# Creating a label
label = Label(text="Pomodoro", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 50), width= 8)  # creating a Label and choosing text, foreground color, background color and font
label.grid(row=0, column=1)   # choosing alignment in the grid


# Creating a start button
start_button = Button(text="Start", command=start_timer)   # creating a start button and assigning it to start_timer function
start_button.grid(row=2, column=0)       # choosing alignment in the grid

# Creating a reset button
start_button = Button(text="Reset", command=reset_timer)   # creating a reset button and assigning it to reset_timer function

start_button.grid(row=2, column=2)      # choosing alignment in the grid

# creating a tick
check_marks = Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME, 20, "bold"))   # creating a label for the session completion check marks
check_marks.grid(row=3, column=1)        # choosing alignment in the grid


window.mainloop()                      # main loop to keep the window from closing
