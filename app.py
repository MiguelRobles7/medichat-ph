from flask import Flask, render_template, url_for, redirect, request
from forms import GeneralForm, SymptomsForm
from prolog import PrologShell
import re
import itertools

pl = PrologShell('prolog.pl')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f53960fc5abb58f0aa0de107'


class Patient:
    def __init__(self):
        self.bmi = 0
        self.age = 0
        self.unknown_diseases = []
        self.unknown_sus = []
        self.to_confirm = []


p = Patient()


@app.route('/')
@app.route('/general', methods=['GET', 'POST'])
def general():
    form = GeneralForm()
    if request.method == 'POST':
        p.age = form.age.data
        p.bmi = form.bmi.data
        symptoms = request.form.getlist('symptoms')

        if symptoms:
            for s in symptoms:
                print(s)
                pl.assert_symptom(s)
        return redirect(url_for('symptoms'))
    return render_template('general_questions.html', form=form)


@app.route('/symptoms', methods=['GET', 'POST'])
@app.route('/symptoms')
def symptoms():
    form = SymptomsForm()
    try:
        if request.method == 'POST':
            print("POST")
            ans = request.form.get('symptoms')
            print(ans)
            print(p.to_confirm[0])
            print("PRE")
            print(p.to_confirm)
            if ans == 'Yes':
                pl.assert_symptom(p.to_confirm[0])
                print(p.to_confirm.pop(0))
            else:
                pl.assert_no_symptom(p.to_confirm[0])
                p.to_confirm = []

            print("POST")
            print(p.to_confirm)
    except:
        if not p.unknown_diseases and not p.unknown_sus:
            return redirect(url_for('results'))
        else:
            print("ERROR")

    p.unknown_diseases = pl.get_unknown_diseases()
    # while true
    if not p.unknown_diseases:
        p.unknown_sus = pl.get_unknown_susceptible_diseases()
        if not p.unknown_sus:
            return redirect(url_for('results'))
        else:
            symptoms = itertools.chain.from_iterable(
                map(pl.get_unknown_susceptible_disease_symptoms, p.unknown_sus)
            )
            if not p.to_confirm:
                p.to_confirm = find_symptoms_to_confirm(symptoms)
    else:
        symptoms = itertools.chain.from_iterable(
            map(pl.get_unknown_disease_symptoms, p.unknown_diseases)
        )

        if not p.to_confirm:
            p.to_confirm = find_symptoms_to_confirm(symptoms)

    return render_template('symptoms_questions.html', form=form, question="Do you have " + p.to_confirm[0].replace('_', ' ') + "?")


@app.route('/results')
def results():
    return render_template('results.html', diseases=pl.get_yes_diseases(), sus=pl.get_yes_susceptible_diseases())


if __name__ == '__main__':
    app.run(debug=True)


def find_symptoms_to_confirm(symptoms_list):
    unknown_symptoms = set(pl.get_unknown_symptoms())

    def count_unknowns(sym):
        count = 0
        for s in sym:
            if s in unknown_symptoms:
                count += 1
        return count

    symptoms = min(symptoms_list, key=count_unknowns)
    symptoms = list(filter(lambda s: s in unknown_symptoms, symptoms))
    symptoms.sort(key=lambda x: -pl.get_symptom_occurence(x))
    return symptoms


def confirm_symptoms(symptoms):
    for s in symptoms:
        y = input(f'Do you have ' + s.replace('_', ' ') + '? ').rstrip()
        if y[0].lower() == 'y':
            pl.assert_symptom(s)
        else:
            pl.assert_no_symptom(s)
            break
