import traceback
from flask import render_template, request, redirect, url_for
import logging.config
from flask import Flask
from src.kickstarter_db import Campaign
from flask_sqlalchemy import SQLAlchemy
from src import predict_state



# Initialize the Flask application
app = Flask(__name__, template_folder="app/templates")

# Configure flask app from flask_config.py
app.config.from_pyfile('config/flaskconfig.py')


# Initialize the database
db = SQLAlchemy(app)

@app.route('/')
def index():
    """Main view that lists Campaigns in the database.

    Create view into index page that uses data queried from Campaign database and
    inserts it into the app/templates/index.html template.

    Args:
        None.

    Returns:
        rendered html template
    """
    return render_template('index.html')



@app.route('/output', methods=['POST'])
def add_entry():
    """View that process a POST with new Campaign input containing user-specified campaign information.

    Args:
        None.

    Returns:
         Redirects the output.html page.
    """

    campaign1 = Campaign(
                        name=request.form['name'],
                        blurb=request.form['blurb'],
                        USD_goal=request.form['USD_goal'],
                        num_days=request.form['num_days'],
                        country=request.form['country'],
                        category_name=request.form['category_name'],
                        p_category_name=request.form['p_category_name'],
                        staff_pick=request.form['staff_pick']
    )
    db.session.add(campaign1)
    db.session.commit()
    input = db.session.query(Campaign).order_by(Campaign.id.desc()).first()
    y_pred, y_pred_proba = predict_state.process_user_input(input)
    if y_pred == 1:
        predicted_state = 'SUCCESS'
        y_pred_proba = [i for i in y_pred_proba]
    elif y_pred == 0:
        predicted_state = 'FAILED'
        y_pred_proba = [i for i in y_pred_proba]
    else:
        predicted_state = 'INVALID USER ENTRY'
        y_pred_proba = ""

    return render_template("output.html", predicted_state=predicted_state, y_pred_proba=y_pred_proba)


if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])
