"""
Program Description:
This code was inspired by Hans Rosling's data visualization of gdp per capita, population and life expectancy, and
greatly drew from Professor Piech's Lecture 18 Mindset code. This code provides a 5-dimensional data visualization of
each state (year [time in animation], electoral college votes [position on y-axis], electoral votes as a share of the
total  electoral college [size of bubble], population [position on x-axis], and nominated party [color of bubble].
Such a data visualization is particularly relevant in today's times, where the electoral college and popular votes
almost had different victors for the third election within two decades. The visualization illustrates many important
trends, such how four states are increasingly dominating the electoral college (which can be seen by using option 1 and
option 2A, how "swing states" are converging in terms of electoral votes and population (option 2B), and how certain
states underwent shifts in party allegiance (option 3), as well as election years where the electoral college (and
sometimes the election) are completely dominated by a certain party (option 1, see 1964, 1972, 1980). A very necessary
extension to this code would be illustrating specific counties in each state, as Rosling did with parts of each country.
The election information was either summarized from or taken directly from history.com.
"""

# import packets
import json
import tkinter
import time
import math


# related to data
START_YEAR = 1892
END_YEAR = 2020
ELEC_CYCLE = 4

# related to x and y values
MAX_ELECTORAL_VOTES = 60
MIN_ELECTORAL_VOTES = 0
MAX_POP = math.log(48500000)
MIN_POP = math.log(580000)

# related to drawing
CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 600
X_AXIS_OFFSET = 50
Y_AXIS_OFFSET = 50
SECOND_Y_AXIS = 800


def main():
    state_data = json.load(open('b.json'))
    pres_data = json.load(open('c.json'))
    info_data = json.load(open('d.json'))

    # provides user with init info
    user_info()

    option = int(input("To select the option, please enter the option number and press enter:  "))
    space()

    # in case 1, allows user to input states
    if option == 1:
        states_to_track = []
        while True:
            a = str(input('State to track (0 to stop): '))
            if a == '0':
                break
            else:
                states_to_track.append(a)

        state_list = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware',
                  'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky',
                  'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri',
                  'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
                  'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island',
                  'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',
                  'West Virginia', 'Wisconsin', 'Wyoming']

    # in case 2, provides user with default lists
    if option == 2:

        print("Set A : Electoral Superpowers: California, Florida, Texas, New York")
        print("Set B: Midwestern Wall: Michigan, Minnesota, Ohio, Pennsylvania, Wisconsin")

        user_choice = str(input("Please enter A to select Set A or B to select Set B:   "))
        space()

        # accounts for case sensitive input
        if user_choice.lower() == 'a':
            states_to_track = ['California', 'Florida', 'Texas', 'New York']
        elif user_choice.lower() == 'b':
            states_to_track = ['Michigan', 'Minnesota', 'Ohio', 'Pennsylvania', 'Wisconsin']

        state_list = states_to_track

    # in case 3, allows user to input the states they wish to track
    if option == 3:
        a = str(input('State to track (0 to stop): '))
        states_to_track = [a]
        while True:
            a = str(input('State to track (0 to stop): '))
            if a == '0':
                break
            else:
                states_to_track.append(a)

        state_list = states_to_track

    canvas = make_canvas(CANVAS_WIDTH, CANVAS_HEIGHT, 'Electoral Politics')
    # for each year to be visualized
    for year in range(START_YEAR, END_YEAR + ELEC_CYCLE, ELEC_CYCLE):
        # draws the current year
        clear_canvas(canvas)
        draw_graph_background(canvas)
        draw_year_text(canvas, year)
        draw_elec_gen_text(canvas)
        draw_pres_names(canvas, year, pres_data)
        text_box(canvas, year, info_data)
        year_data = state_data[str(year)]
        plot_year_bubbles(canvas, year_data, states_to_track, state_list)

        # animate
        # time.sleep(2)
        canvas.update()

        # To make animation automatic, uncomment the time.sleep(3), and comment the two lines below
        if year % 4 == 0:
           input('Enter to continue')

    canvas.mainloop()


# **************************************************************
#                 CONTENT PRINTED TO TERMINAL                  *
# **************************************************************
def space():
    print("")


def user_info():
    space()
    space()
    print("Welcome! This data visualization aims to illustrate the way in which ")
    print("electoral college votes and population in each state have changed over time. ")
    print("Our data goes as far back as 1892, and covers every election from then until 2020. ")
    print("Each bubble corresponds to a certain state. The x-axis represents the state's population, ")
    print("and the y-axis represents the number of electoral college votes it possessed that ")
    print("election cycle. The size of the bubble is relative to the state's electoral votes as a")
    print(" percentage of the total electoral votes that election cycle")
    print("")
    print("To begin, choose one of three options listed below.")
    print("")
    print("Option 1: Track all states over time, and highlight specific states.")
    print("Option 2: Choose from one of our suggested state groups to track.")
    print("Option 3: Track specific states only")
    print("")

# **************************************************************
#           DYNAMIC PARTS OF THE ANIMATION                     *
# **************************************************************

def plot_year_bubbles(canvas, year_data, states_to_track, state_list):
    filled = states_to_track
    for state_name in state_list:
        state_data = year_data[state_name]
        elecvotes = float(state_data['uselec'])
        pop = int(state_data['uspop'])
        party = str(state_data['usparty'])
        votesize = float(int(state_data['uselec']) / int(year_data['United States']['uselec']))
        draw_bubble(canvas, elecvotes, pop, votesize, filled, party, state_name)


def draw_bubble(canvas, elecvotes, pop, votesize, filled, party, state):
    r = math.sqrt(votesize) * 100
    plot_width = CANVAS_WIDTH - Y_AXIS_OFFSET
    plot_height = CANVAS_HEIGHT - X_AXIS_OFFSET
    log_pop = 0
    if pop != 0:
        log_pop = float(math.log(pop))

    x = scale(log_pop, MAX_POP, MIN_POP, plot_width - 400) + Y_AXIS_OFFSET
    y = scale(elecvotes, MAX_ELECTORAL_VOTES, MIN_ELECTORAL_VOTES, plot_height) + X_AXIS_OFFSET
    y = CANVAS_HEIGHT - y
    party = party
    make_centered_bubble(canvas, x, y, 2 * r, filled, party, state)


def draw_year_text(canvas, year):
    y = CANVAS_HEIGHT - X_AXIS_OFFSET - 20
    canvas.create_text(750, y, anchor='c', font='Times 50', text=str(year))


def draw_elec_gen_text(canvas):
    canvas.create_text(Y_AXIS_OFFSET * 3.70, 25, anchor='e', font='Times 20', text='President: ')
    canvas.create_text(Y_AXIS_OFFSET * 3.70, 50 , anchor='e', font='Times 20', text='Vice-President: ')


def draw_pres_names(canvas, year, pres_data):
    cur_president = pres_data[str(year)]['pres']
    cur_vice = pres_data[str(year)]['vice']
    y = Y_AXIS_OFFSET
    canvas.create_text(Y_AXIS_OFFSET * 3.75, 25, anchor='w', font='Times 20', text=cur_president)
    canvas.create_text(Y_AXIS_OFFSET * 3.75, 50, anchor='w', font='Times 20', text=cur_vice)


def text_box(canvas, year, info_data):
    canvas.create_text(815, 25, anchor='w', font='Times 24', text='Election Information: ')

    # removes opening and closing quotation marks
    remove_start_quote = info_data[str(year)][0]
    info_data[str(year)][0] = remove_start_quote[1:]
    remove_end_quote = info_data[str(year)][-1]
    info_data[str(year)][-1] = remove_end_quote[0:-1]

    lines = []
    words = []
    total_char = 0

    for word in info_data[str(year)]:
        count = len(word)

        if total_char + count < 42:
            total_char += count
            words.append(word)
            # accounts for additional space between words
            total_char += 1
        else:
            lines.append(" ".join(words))
            words.clear()
            total_char = 0
            total_char += count
            words.append(word)

    if len(words) > 0:
        lines.append(" ".join(words))

    for i in range(len(lines)):
        canvas.create_text(815, 60 + (24 * i), anchor='w', font='Times 20', text=lines[i])


def clear_canvas(canvas):
    canvas.delete('all')


def scale(v, max_v, min_v, screen_max):
    p = (v - min_v) / (max_v - min_v)
    p = max(0, p)
    return p * screen_max


def make_centered_bubble(canvas, center_x, center_y, size, filled, party, state):
    x_1 = center_x - size / 2
    y_1 = center_y - size / 2

    # base case
    fill = None
    outline = None
    width = 0.2

    # determines color, width, outline
    if party == 'D':
        fill = 'steel blue'
        if state in filled:
            outline = 'DeepSkyBlue4'
            width = 5

    elif party == 'R':
        fill = 'indian red'
        if state in filled:
            outline = 'IndianRed4'
            width = 5

    elif party == 'AI' or 'I':
        fill = 'gray'
        if state in filled:
            outline = 'grey8'
            width = 5

    elif party == 'BM':
        fill = 'dark green'
        if state in filled:
            outline = 'aquamarine4'
            width = 5

    canvas.create_oval(x_1, y_1, x_1 + size, y_1 + size, fill=fill, width=width, outline=outline)


# **************************************************************
#           FIXED PARTS OF THE ANIMATION                       *
# **************************************************************

def draw_graph_background(canvas):
    draw_x_axis(canvas)
    draw_y_axis(canvas)


def draw_x_axis(canvas):
    y = CANVAS_HEIGHT - X_AXIS_OFFSET
    canvas.create_line(0, y, CANVAS_WIDTH - 400, y)
    label_y = y + X_AXIS_OFFSET / 2
    x_axis_txt = "Population (adjusted log thousands)"
    canvas.create_text(380, label_y, anchor='c', font='Times 24', text=x_axis_txt)


def draw_y_axis(canvas):
    canvas.create_line(Y_AXIS_OFFSET, 0, Y_AXIS_OFFSET, CANVAS_HEIGHT)
    y_axis_txt = "Electoral college power (votes)"
    canvas.create_text(Y_AXIS_OFFSET / 2, 300, anchor='c', font='Times 24', text=y_axis_txt, angle=90)
    canvas.create_line(SECOND_Y_AXIS, 0, SECOND_Y_AXIS, CANVAS_HEIGHT)


def make_canvas(width, height, title):
    top = tkinter.Tk()
    top.minsize(width=width, height=height)
    top.title(title)
    canvas = tkinter.Canvas(top, width=width + 1, height=height + 1, bg='bisque')
    canvas.pack()
    return canvas


if __name__ == '__main__':
    main()
