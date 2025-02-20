import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, CheckButtons
from matplotlib.patches import Patch

# Real Excel code 

df2017 = pd.read_excel('Resources/Employee Diversity.xlsx', sheet_name='2017')
df2017.replace(0, np.nan, inplace=True)
df2021 = pd.read_excel('Resources/Employee Diversity.xlsx', sheet_name='2021')
df2021.replace(0, np.nan, inplace=True)
companies = df2017['Company'].tolist()
n_companies = len(companies)

x = np.arange(n_companies)


# Prepare Data for Normal Plot
ethnicities = ['Female', 'Asian', 'Black', 'Latino']
normal_data = {} 
for eth in ethnicities:
    col_name = f'{eth} %' if eth == 'Female' else f'% {eth}'
    normal_data[f"{eth} (2017)"] = df2017[col_name].values
    normal_data[f"{eth} (2021)"] = df2021[col_name].values

# Compute Delta Data (2021 minus 2017) per Ethnicity

delta_data = {}
for eth in ethnicities:
    col_name = f'{eth} %' if eth == 'Female' else f'% {eth}'
    delta_data[eth] = df2021[col_name].values - df2017[col_name].values


# Colors (one per ethnicity)

ethnicity_colors = {
    'Female': 'lightcoral',
    'Asian': 'lightblue',
    'Black': 'violet',
    'Latino': 'gold'
}


# Global State and Figure Setup

fig, ax = plt.subplots(figsize=(14, 8))
plt.subplots_adjust(left=0.25, right=0.88)
# Modes: "empty", "normal", or "delta"
current_mode = "empty"
current_filter = None

def draw_empty_plot():
    """Draw an empty plot (axes and labels only)."""
    ax.clear()
    ax.set_xticks(x)
    ax.set_xticklabels(companies, rotation=45, ha='right')
    ax.set_xlabel('Company')
    ax.set_ylabel('Employee %')
    ax.set_title('Employee Diversity by Top 10 Tech Companies')
    fig.canvas.draw()

def draw_selected_plot():
    """Draw the normal plot with only the series selected via checkboxes,
       and add a value label at the top of each bar.
    """
    selected = [lbl for lbl in series_labels if checkbox_state[lbl]]
    ax.clear()
    if not selected:
        draw_empty_plot()
        return
    total_series = len(selected)
    total_bar_width = 0.8
    bar_width = total_bar_width / total_series
    for i, label in enumerate(selected):
        eth = label.split()[0]
        offset = -total_bar_width/2 + (i + 0.5) * bar_width
        container = ax.bar(x + offset, normal_data[label], width=bar_width,
                           color=ethnicity_colors[eth], label=label)
        for bar in container:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height, f'{height:.0f}',
                    ha='center', va='bottom', fontsize=8, color='black')
    ax.set_xticks(x)
    ax.set_xticklabels(companies, rotation=45, ha='right')
    ax.set_xlabel('Company')
    ax.set_ylabel('Employee %')
    ax.set_title('Employee Diversity by Top 10 Tech Companies')
    fig.canvas.draw()

def draw_delta_plot():
    ax.clear()
    n_eth = len(ethnicities)
    total_bar_width = 0.8
    bar_width = total_bar_width / n_eth
    for i, eth in enumerate(ethnicities):
        offset = -total_bar_width/2 + (i + 0.5) * bar_width
        container = ax.bar(x + offset, delta_data[eth], width=bar_width,
                           color=ethnicity_colors[eth], label=eth)
        for bar in container:
            height = bar.get_height()
            va = 'bottom' if height >= 0 else 'top'
            ax.text(bar.get_x() + bar.get_width()/2, height, f'{height:+.1f}',
                    ha='center', va=va, fontsize=8, color='black')
    ax.axhline(0, color='black', linewidth=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels(companies, rotation=45, ha='right')
    ax.set_xlabel('Company')
    ax.set_ylabel('Delta (%)')
    ax.set_title('Delta: Change from Trump (2017) to Biden (2021)')
    fig.canvas.draw()

# Start with an empty plot.
draw_empty_plot()

# Mode Buttons (Trump, Biden, Delta)

button_ax_trump = plt.axes([0.91, 0.55, 0.08, 0.05])
button_ax_biden = plt.axes([0.91, 0.48, 0.08, 0.05])
button_ax_delta = plt.axes([0.91, 0.38, 0.08, 0.05])

button_trump = Button(button_ax_trump, 'Trump\n(2017)', color='white', hovercolor='lightgray')
button_biden = Button(button_ax_biden, 'Biden\n(2021)', color='white', hovercolor='lightgray')
button_delta = Button(button_ax_delta, 'Delta:\nTrump Minus\nBiden', color='white', hovercolor='lightgray')
button_delta.label.set_fontsize(8)

# List of series labels 
series_labels = list(normal_data.keys())
# Initialize checkbox state: all unchecked.
checkbox_state = {lbl: False for lbl in series_labels}

def set_checkboxes_for_year(year):
    for i, lbl in enumerate(series_labels):
        desired = (year in lbl)
        if checkbox_state[lbl] != desired:
            check_buttons.set_active(i)  # toggle state and calls callback

def update_button_state(button, active):
    if active:
        button.set_facecolor('white')
    else:
        button.set_facecolor('grey')


def update_all_button_states():
    update_button_state(button_ax_trump, (current_mode == "normal" and current_filter == "2017"))
    update_button_state(button_ax_biden, (current_mode == "normal" and current_filter == "2021"))
    update_button_state(button_ax_delta, (current_mode == "delta"))

def show_trump(event):
    global current_mode, current_filter
    if current_mode == "normal" and current_filter == "2017":
        # If Trump is already active, clear the chart.
        current_mode = "empty"
        current_filter = None
        draw_empty_plot()
    else:
        # Reset all checkboxes to unchecked.
        for lbl in series_labels:
            checkbox_state[lbl] = False
        draw_empty_plot()  # Clear the chart first.
        current_mode = "normal"
        current_filter = "2017"
        set_checkboxes_for_year("2017")
        draw_selected_plot()
    update_all_button_states()

def show_biden(event):
    global current_mode, current_filter
    if current_mode == "normal" and current_filter == "2021":
        current_mode = "empty"
        current_filter = None
        draw_empty_plot()
    else:
        for lbl in series_labels:
            checkbox_state[lbl] = False
        draw_empty_plot()
        current_mode = "normal"
        current_filter = "2021"
        set_checkboxes_for_year("2021")
        draw_selected_plot()
    update_all_button_states()

def show_delta(event):
    global current_mode, current_filter
    if current_mode == "delta":
        current_mode = "empty"
        current_filter = None
        draw_empty_plot()
    else:
        draw_delta_plot()
        current_mode = "delta"
        current_filter = None
    update_all_button_states()

button_trump.on_clicked(show_trump)
button_biden.on_clicked(show_biden)
button_delta.on_clicked(show_delta)


# CheckButtons for Interactive Series Selection

check_ax = fig.add_axes([0.02, 0.25, 0.15, 0.30])
check_buttons = CheckButtons(check_ax, series_labels, [False]*len(series_labels))

def toggle_series(label):
    global checkbox_state, current_mode
    checkbox_state[label] = not checkbox_state[label]
    if current_mode == "normal":
        draw_selected_plot()

check_buttons.on_clicked(toggle_series)


# Static Color Legend (shows mapping from ethnicity to color)

legend_handles = [Patch(facecolor=ethnicity_colors[eth], label=eth) for eth in ethnicity_colors]
legend_ax = fig.add_axes([0.02, 0.72, 0.15, 0.15])
legend_ax.axis('off')
legend_ax.legend(legend_handles, list(ethnicity_colors.keys()), loc='upper left')

plt.show()
