import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, CheckButtons
from matplotlib.patches import Patch

def create_figure():
    # --- Step 1: Prepare data ---
    df2017 = pd.read_excel('Resources/Employee Diversity.xlsx', sheet_name='2017')
    df2017.replace(0, np.nan, inplace=True)
    df2021 = pd.read_excel('Resources/Employee Diversity.xlsx', sheet_name='2021')
    df2021.replace(0, np.nan, inplace=True)
    companies = df2017['Company'].tolist()
    x = np.arange(len(companies))

    ethnicities = ['Female', 'Asian', 'Black', 'Latino']
    normal_data = {}
    for eth in ethnicities:
        col_name = f'{eth} %' if eth == 'Female' else f'% {eth}'
        normal_data[f"{eth} (2017)"] = df2017[col_name].values
        normal_data[f"{eth} (2021)"] = df2021[col_name].values

    delta_data = {}
    for eth in ethnicities:
        col_name = f'{eth} %' if eth == 'Female' else f'% {eth}'
        delta_data[eth] = df2021[col_name].values - df2017[col_name].values

    ethnicity_colors = {
        'Female': 'lightcoral',
        'Asian': 'lightblue',
        'Black': 'violet',
        'Latino': 'gold'
    }

    # --- Step 2: Create figure and axes ---
    fig, ax = plt.subplots(figsize=(14, 8))
    plt.subplots_adjust(left=0.25, right=0.88)

    # We'll store these states in function-local scope:
    current_mode = "empty"
    current_filter = None

    # ... define your helper functions (draw_empty_plot, draw_selected_plot, etc.) ...
    # (copy them exactly as you had, but keep them inside create_figure()).

    # Because you’re returning fig to Flask, you typically wouldn’t call plt.show() here.
    # Instead, you can leave all the event logic if you want, but note that mpld3 
    # may not fully replicate the Matplotlib Buttons/CheckButtons in a browser.

    def draw_empty_plot():
        # (same as before)
        ax.clear()
        ax.set_xticks(x)
        ax.set_xticklabels(companies, rotation=45, ha='right')
        ax.set_xlabel('Company')
        ax.set_ylabel('Employee %')
        ax.set_title('Employee Diversity by Top 10 Tech Companies')
        fig.canvas.draw()

    # ... repeat for draw_selected_plot(), draw_delta_plot(), etc. ...

    # Initialize the empty plot:
    draw_empty_plot()

    # Create your buttons/checkboxes:
    # (Note: these won't truly be interactive in a browser via mpld3; 
    #  but you can still define them if you want.)
    button_ax_trump = plt.axes([0.91, 0.55, 0.08, 0.05])
    button_ax_biden = plt.axes([0.91, 0.48, 0.08, 0.05])
    button_ax_delta = plt.axes([0.91, 0.38, 0.08, 0.05])

    button_trump = Button(button_ax_trump, 'Trump\n(2017)', color='white', hovercolor='lightgray')
    button_biden = Button(button_ax_biden, 'Biden\n(2021)', color='white', hovercolor='lightgray')
    button_delta = Button(button_ax_delta, 'Delta:\nTrump Minus\nBiden', color='white', hovercolor='lightgray')
    button_delta.label.set_fontsize(8)

    series_labels = list(normal_data.keys())
    checkbox_state = {lbl: False for lbl in series_labels}

    # ... define show_trump(), show_biden(), show_delta() ...
    # ... define check buttons, legend, etc. ...

    # DO NOT call plt.show() here if you want to embed this figure in Flask.
    # Return the figure object so we can pass it to mpld3 or another library.
    return fig

# If you still want to run this file standalone (for testing), you can do:
if __name__ == "__main__":
    f = create_figure()

plt.show()
