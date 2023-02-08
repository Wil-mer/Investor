## Wilmer Liljenström
## Game using brownian motion to plot a simulated stock
## Task is to, based on given information, guess if the stock will go higher or lower next period

import matplotlib
import matplotlib.pyplot as plt
import PySimpleGUI as sg
from scipy.stats import norm
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

win_res = (1024,768)
sg.theme('Dark Gray 13')

main_layout = [
[sg.Canvas(size=win_res, key='Canvas')],
[sg.HorizontalSeparator(pad=15)],
[sg.Text('Where will the stock be priced in 365 days?',border_width=20,font='Courier 20')],
[sg.Button('Higher',size=(5,3/2),key='-Higher-'), sg.VerticalSeparator(pad=5), sg.Button('Lower',size=(5,3/2),key='-Lower-')]
]

win_layout = [[sg.Canvas(size=win_res, key='Canvas2')],[sg.HorizontalSeparator(pad=15)],[sg.Text('You were correct',border_width=20,font='Courier 20'),sg.Button('Try again',size=(5,3/2), key='Redo')]]
lose_layout = [[sg.Canvas(size=win_res, key='Canvas3')],[sg.HorizontalSeparator(pad=15)],[sg.Text('You were wrong',border_width=20,font='Courier 20'),sg.Button('Try again',size=(5,3/2), key='Redo2')]]
layout = [[sg.pin(sg.Column(main_layout, key='main_layout', element_justification='c')), sg.pin(sg.Column(win_layout, key='win_layout', visible=False)), sg.pin(sg.Column(lose_layout, key='lose_layout', visible=False))]]

## window uses three different layouts to hide choice buttons after game is completed and show win/lose
window = sg.Window('Investor', layout, grab_anywhere=False, finalize=True)
figure_agg = None

n_days = 365    #variable for 365 steps/days, used as 1 period in the game.

## Function to plot and draw prices on canvas
def draw_figure(prices, canvas):
    plt.plot(prices)
    if len(prices) > n_days:  # draw lines in second period window for better visual
        plt.axvline(n_days-1)
        plt.axhline(prices[n_days-1])
    plt.xlabel('Days')
    plt.ylabel('Price')
    plt.title('Value of stock Over Time')
    plot = plt.gcf()
    if not hasattr(draw_figure, 'canvas_packed'):
        draw_figure.canvas_packed = {}
    figure_canvas_agg = FigureCanvasTkAgg(plot, canvas)
    figure_canvas_agg.draw()
    widget = figure_canvas_agg.get_tk_widget()
    if widget not in draw_figure.canvas_packed:
        draw_figure.canvas_packed[widget] = plot
        widget.pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

## Generate a random stock price using Brownian motion
def calc_prices(prices,lower_bound, upper_bound):
    for j in range(lower_bound,upper_bound):
        prices.append(prices[j-1] + norm.rvs(loc=0))
    if prices[j] <0:
        prices[j] = 0
    return prices

## Function to delete the current figure shown
def delete_figure_agg(figure_agg):
    figure_agg.get_tk_widget().forget()
    draw_figure.canvas_packed.pop(figure_agg.get_tk_widget())
    plt.close('all')


## Game loop
def gameloop():
    window['win_layout'].update(visible=False)   # Reset window
    window['lose_layout'].update(visible=False)
    window['main_layout'].update(visible=True)
    prices = [100] 
    prices = calc_prices(prices,1,n_days)
    figure_agg = draw_figure(prices, window['Canvas'].TKCanvas)
    while True:
        event, values = window.read()       # reads inputs and values into window, e.g buttonpress
        if event in (sg.WIN_CLOSED, 'Exit'):             # if user closed window or clicked Exit button
            break
        elif event == '-Higher-':
            delete_figure_agg(figure_agg)
            prices = calc_prices(prices,n_days,2*n_days)
            if prices[n_days-1]<prices[2*n_days-1]:
                guess = True
            else: guess = False
            if guess == True:
                window['main_layout'].update(visible=False)
                figure_agg = draw_figure(prices, window['Canvas2'].TKCanvas)
                window['win_layout'].update(visible=True)
                event, values = window.read()

            elif guess == False:  
                window['main_layout'].update(visible=False)
                figure_agg = draw_figure(prices, window['Canvas3'].TKCanvas)
                window['lose_layout'].update(visible=True)
                event, values = window.read()

            if event == 'Redo' or 'Redo2':  #Bug with pysimplegui, can not have two identical keys in different layouts
                delete_figure_agg(figure_agg)   # Clear figure from canvas
                gameloop()     # Throw back to loop to restart game

        elif event == '-Lower-':
            delete_figure_agg(figure_agg)
            prices = calc_prices(prices,n_days,2*n_days)
            if prices[n_days-1]>prices[2*n_days-1]:
                guess = True
            else: guess = False

            if guess == True:
                window['main_layout'].update(visible=False)
                figure_agg = draw_figure(prices, window['Canvas2'].TKCanvas)
                window['win_layout'].update(visible=True)
                event, values = window.read()

            elif guess == False: 
                window['main_layout'].update(visible=False)
                figure_agg = draw_figure(prices, window['Canvas3'].TKCanvas)
                window['lose_layout'].update(visible=True)
                event, values = window.read()

            if event == 'Redo' or 'Redo2':
                delete_figure_agg(figure_agg)
                gameloop()
gameloop()
window.close()