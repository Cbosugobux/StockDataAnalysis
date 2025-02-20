from flask import Flask, render_template
import mpld3  # or use Plotly/Bokeh as described above
from diversityData import create_figure  # Your script’s function

app = Flask(__name__)

@app.route('/diversityData.html')
def index():
    # For mpld3:
    fig = create_figure()  # Modify your function to generate the matplotlib figure
    html_fig = mpld3.fig_to_html(fig)
    return render_template('diversityData.html', plot=html_fig)
    # For Plotly or Bokeh, generate and pass the HTML snippet similarly.

if __name__ == '__main__':
    app.run(debug=True)
