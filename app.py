from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hello-hi'
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

responses = []
options = satisfaction_survey.questions[0].choices
ind = 0
complete = False

@app.route('/')
def home():
    return render_template('home.html', title = satisfaction_survey.title, instructions = satisfaction_survey.instructions)

@app.route('/questions/<int:index>')
def question(index):
    global ind
    if complete:
        flash("Survey Complete")
        return render_template('Complete.html')
    elif index != ind:
        flash("Let's stick with the order we have")
        index = ind
    q = satisfaction_survey.questions[index].question
    options = satisfaction_survey.questions[index].choices
    return render_template('question.html', question = q, choices = options)

@app.route('/answer', methods = ['POST'])
def answer():
    ans = request.form['ans']
    responses.append(ans)
    global ind
    global complete
    if ind == (len(satisfaction_survey.questions)-1):
        ind = 0
        complete = True
        return render_template('Complete.html')
    else:
        ind +=1
        next = f'/questions/{ind}'
    return redirect(next)