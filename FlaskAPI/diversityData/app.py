from flask import Flask, render_template, jsonify
import mpld3
from diversityData import create_figure

app = Flask(__name__)

@app.route('/diversityData.html')
def index():
    # Generate the mpld3 interactive chart
    fig = create_figure()
    html_fig = mpld3.fig_to_html(fig)
    
    return render_template('diversityData.html', plot=html_fig)

@app.route('/api/diversityData')
def get_diversity_data():
    # Read the generated JSON file
    with open("data/diversityData.json", "r") as json_file:
        data = json_file.read()
    
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
