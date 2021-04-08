
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for,session
from flask_login import login_required, current_user

from . import db
import json
from .models import User, Question,QuestionCategory

views = Blueprint('views', __name__)

@views.route('/kidPage', methods=['GET', 'POST'])
@login_required
def kidPage():
    if current_user.auth=="kid":
        if request.method == 'POST':
            if request.form['submit_button'] == 'Start a quiz!':
                return redirect(url_for('views.question'))
        cats = QuestionCategory.query.all()
        return render_template("kidPage.html", user=current_user, cats = cats)
    elif current_user.auth=="editor":
        flash("No Permission to current user to enter kid page.", category='error')
        return render_template("editorPage.html", user=current_user)
    else:
        flash("No Permission to current user to enter admin page.", category='error')
        return render_template("adminPage.html", user=current_user)
    

@views.route('/adminPage', methods=['GET', 'POST'])
@login_required
def adminPage():
    if current_user.auth=="admin":
        return render_template("adminPage.html", user=current_user)
    elif current_user.auth=="kid":
        flash("No Permission to current user to enter admin page.", category='error')
        return render_template("kidPage.html", user=current_user)
    else:
        flash("No Permission to current user to enter admin page.", category='error')
        return render_template("editorPage.html", user=current_user)
    
@views.route('/editorPage')
@login_required    
def editorPage():
    if current_user.auth=="editor":
        return render_template("editorPage.html", user=current_user)
    elif current_user.auth=="kid":
        flash("No Permission to current user to enter editor page.", category='error')
        return render_template("kidPage.html", user=current_user)
    else:
        flash("No Permission to current user to enter editor page.", category='error')
        return render_template("adminPage.html", user=current_user)
   


@views.route('/question',methods=['GET', 'POST'])
@login_required
def question():
    if request.method == 'POST':
        print("hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
        if request.form.get('finish1')=="1":
            print("wwwwwwwwwwwwwwww")
            return redirect(url_for('views.kidPage'))
        if request.form['q_answer']==json.loads(session["questions"][0])['correct']:
            print("dddddddddddddddddd")
            session["score"]+=50
            current_user.score=session["score"]
            db.session.commit() 
        else:
            print("aaaaaaaaaaaaaaa")
            return redirect(url_for('views.info'))
    
        session["questions"].pop(0)
        if len(session["questions"])!=0:
            question=json.loads(session["questions"][0])
            return render_template("question.html",user=current_user,  question = question,score=session["score"])
        else:
            return redirect(url_for('views.finishQuestions'))
    if current_user.auth=="kid":
        questions = Question.query.filter_by(cat = "Animal").all()
        list=[]
        for q in questions:
            list.append(json.dumps(q,default=encoder_question))   
        session["questions"]=list
        session["score"]=current_user.score
        question=json.loads(session["questions"][0])
        return render_template("question.html", user=current_user, question = question,score=session["score"])
    
    elif current_user.auth=="editor":
        flash("No Permission to current user to enter kid page.", category='error')
        return render_template("editorPage.html", user=current_user)
    else:
        flash("No Permission to current user to enter admin page.", category='error')
        return render_template("adminPage.html", user=current_user)


def encoder_question(question):
    if isinstance(question,Question):
        return {'cat':question.cat,
        'question':question.question,
        'correct':question.correct,
        'wrong1':question.wrong1,
        'wrong2':question.wrong2,
        'wrong3':question.wrong3,
        'url':question.url
        }
    raise TypeError(f'Object {question} is not type of Person.')  


@views.route('/info',methods=['GET', 'POST'])
@login_required    
def info():
    if request.method == 'POST':
        return redirect(url_for('views.kidPage'))
    if current_user.auth=="kid":
        return render_template("info.html", user = current_user, question = json.loads(session["questions"][0]))

@views.route('/finishQuestions',methods=['GET', 'POST'])
@login_required    
def finishQuestions():
    if request.method == 'POST':
        return redirect(url_for('views.kidPage'))
    if current_user.auth=="kid":
        return render_template("finishQuestions.html", user = current_user)