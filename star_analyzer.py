import PySimpleGUI as sg
from PIL import Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, FigureCanvasAgg
import cv2
import matplotlib.pyplot as plt
from os import mkdir, listdir
import tkinter as Tk
# --------------------------------- Constants -------------------------------- #
PREVI_PATH = "tmp/previ.png"
PARAM_PREVI_PATH = "tmp/param_previ.png"
INIT_IMG_PATH = None
IMG = None
CURRENT_FIG = None
LBL_LEN = 20
if "tmp" not in listdir(): # Create a directory to store temporary files
    mkdir("tmp")

if "results" not in listdir(): # Create a directory to store saved figures
    mkdir("results")

# --------------------------------- Functions -------------------------------- #
def draw_figure(canvas, figure):
    """ Draws a matplotlib.pyplot figure on a Tkinter Canvas"""
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def mk_fig(vert_values, horiz_values):
    figure = plt.Figure()
    figure.subplots_adjust(hspace=.5)

    ax = figure.add_subplot(211)
    ax.plot(vert_values, color="g")
    ax.set_xlabel("Position in the image (height)")
    ax.set_title("Vertical slice plot")

    ax2 = figure.add_subplot(212)
    ax2.plot(horiz_values, color="r")
    ax2.set_xlabel("Position in the image (width)")
    ax2.set_title("Horizontal slice plot")
    return figure

def name(name):
    dots = LBL_LEN-len(name)-2
    return sg.Text(name + ' ' + '•'*dots, size=(LBL_LEN,1), justification='r',pad=(0,0), font='Courier 10')

# ---------------------------------------------------------------------------- #
#                               LAYOUT DEFINITION                              #
# ---------------------------------------------------------------------------- #
parameters_frame_layout = [
    [name("c (% width)"), sg.Spin([i for i in range(0,101)], initial_value=50, key="-C-", enable_events=True)], # c settings
    [name("r (% height) "), sg.Spin([i for i in range(0,101)], initial_value=50, key="-R-", enable_events=True)], # r setings
    [name("N : "), sg.Spin([i for i in range(1,11)], initial_value=1, key="-N-", enable_events=True)], # N settings
    [name("M : "), sg.Spin([i for i in range(1,11)], initial_value=1, key="-M-", enable_events=True)], # M settings
    [sg.Input("StAn_figure.png", disabled=True, key="-SAVEFNME-")], # Filename for the saved figure
    [sg.Button("Trace", key="-TRACE-"), sg.Button("Save figure", key="-SAVEFIG-", disabled=True)] # Trace & save figure buttons
]

left_col = [
    [sg.Text('Choose a file : '), sg.In(size=(25,1), enable_events=True ,key='-FILE_LAB-'), sg.FileBrowse(key="-FILE-")], # Warning label/filename + Browse btn
    # [sg.Button("OK", key="-VAL_IMG-")], # Validate the choosen image
    [sg.Image(key="-PREVI-")], # Previsualitation
    [sg.Frame(layout=parameters_frame_layout, title="Parameters", expand_x=True, element_justification="l")],  # Parameters frame
    [sg.Image("tmp/tuto.png")]
]

rigth_col = [
    [sg.Canvas(key="-CHART-", size=(700,500))] # Canvas to display plots
]

layout = [
    [sg.Column(left_col, element_justification="t"), sg.VSeparator(), sg.Column(rigth_col, element_justification="c")]
]


# ----------------------------- WINDOW DEFINITION ---------------------------- #
window = sg.Window('Star Analyzer', layout,resizable=False, finalize=True)
#window.Maximize()

# ---------------------------------------------------------------------------- #
#                                 INFINITE LOOP                                #
# ---------------------------------------------------------------------------- #
flag = False
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    print(event, values)
    if event == "-FILE_LAB-":
        INIT_IMG_PATH = values[event]
        img = Image.open(values[event])
        img = img.resize((200,150))
        img.save(PREVI_PATH)
        print(type(values[event]))
        window["-PREVI-"].update(PREVI_PATH)
        flag = True
        event = "-INIT-"

    if (event == "-INIT-" or event in ["-N-", "-M-", "-C-", "-R-"]) and flag == True: # flag : insure that an image has been selected first
        try:
            img = cv2.imread(PREVI_PATH)
            data = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            print(data.shape)
            w, h = data.shape[:2]

            c = int(int(values["-C-"]) / 100 * w)
            r = int(int(values["-R-"]) / 100 * w)
            N = int(values["-N-"])
            M = int(values["-M-"])

            if c-N < 0:
                c += N
            if c+N > w:
                c-= N
            if r-M < 0:
                r += M
            if r+M > w:
                r-= M

            #print("--> ", (0,c-N), (h, c+N), (r-M, 0), (r+M, w))
            img_rect = cv2.rectangle(img, (0,c-N), (h, c+N), (255,0,0), 1)
            img = cv2.rectangle(img_rect, (r-M, 0), (r+M, w), (255,0,0), 1)
            #print("->", img.shape)
            cv2.imwrite(PARAM_PREVI_PATH, img)
            window["-PREVI-"].update(PARAM_PREVI_PATH)
        except:
            print("No previ image found")

    if event == "-TRACE-":
        try:
            figure_canvas_agg.get_tk_widget().forget()
            plt.close('all')
        except:
            pass
        vert_values = data[:, c-N:c+N].sum(axis=1)/(2*N)
        horiz_values = data[r-M:r+M, :].sum(axis=0)/(2*M)

        figure = mk_fig(vert_values, horiz_values)
        CURRENT_FIG = plt.gcf()
        canvas = window["-CHART-"].TKCanvas
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)

        window["-SAVEFIG-"].update(disabled=False)
        window["-SAVEFNME-"].update(disabled=False)
    
    if event == "-SAVEFIG-":
        figure = mk_fig(vert_values, horiz_values)
        figure.savefig("results/" + values["-SAVEFNME-"])


    #     NAME_SIZE = 23

    # def name(name):
    #     


    #     def draw_plot(self, canvas, figure, loc=(0, 0)):

    #     figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    #     figure_canvas_agg.draw()
    #     figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    #     return figure_canvas_agg

    # def delete_plot(self, fig_agg):

    #     fig_agg.get_tk_widget().forget()
    #     plt.close('all')