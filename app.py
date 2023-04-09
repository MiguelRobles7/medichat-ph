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
        self.gender = 'male'
        self.unknown_diseases = []
        self.unknown_sus = []
        self.to_confirm = []


p = Patient()


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/general', methods=['GET', 'POST'])
def general():
    form = GeneralForm()
    if request.method == 'POST':
        p.age = form.age.data
        p.bmi = form.bmi.data
        if form.gender.data == 'M':
            p.gender = 'male'
        else:
            p.gender = 'female'

        pl.assert_age(p.age)
        pl.assert_bmi(p.bmi)
        pl.assert_gender(p.gender)

        symptoms = request.form.getlist('symptoms')

        if symptoms:
            for s in symptoms:
                pl.assert_symptom(s)
        return redirect(url_for('symptoms'))
    return render_template('general_questions.html', form=form)


@app.route('/symptoms', methods=['GET', 'POST'])
@app.route('/symptoms')
def symptoms():
    form = SymptomsForm()
    try:
        if request.method == 'POST':
            ans = request.form.get('symptoms')
            if ans == 'Yes':
                pl.assert_symptom(p.to_confirm[0])
                p.to_confirm.pop(0)
            else:
                pl.assert_no_symptom(p.to_confirm[0])
                p.to_confirm = []

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
                p.to_confirm = find_symptom_to_confirm(symptoms)
    else:
        symptoms = itertools.chain.from_iterable(
            map(pl.get_unknown_disease_symptoms, p.unknown_diseases)
        )

        if not p.to_confirm:
            p.to_confirm = find_symptom_to_confirm(symptoms)

    return render_template('symptoms_questions.html', form=form, question=normalize_question_format(p.to_confirm[0]))


@app.route('/results')
def results():
    diseases = []
    sus = []
    for d in pl.get_yes_diseases():
        diseases.append(normalize_prolog_names(d))
    for s in pl.get_yes_susceptible_diseases():
        sus.append(normalize_prolog_names(s))

    danger_diseases = ["Dengue", "Stroke"]
    warning_disease = ["Malaria", "Tuberculosis",
                       "Type 2 Diabetes",  "Hypertension", "Leptospirosis"]
    return render_template('results.html', diseases=diseases, sus=sus, danger_diseases=danger_diseases, warning_disease=warning_disease)


if __name__ == '__main__':
    app.run(debug=True)


def find_symptom_to_confirm(symptoms_list):
    unknown_symptoms = set(pl.get_unknown_symptoms())

    def count_unknowns(symptoms):
        count = 0
        for s in symptoms:
            if s in unknown_symptoms:
                count += 1
        return count

    symptoms = min(symptoms_list, key=count_unknowns)
    symptoms = filter(lambda s: s in unknown_symptoms, symptoms)
    return [(max(symptoms, key=lambda x: pl.get_symptom_occurence(x)))]


def confirm_symptoms(symptoms):
    for s in symptoms:
        y = input(f'Do you have ' + s.replace('_', ' ') + '? ').rstrip()
        if y[0].lower() == 'y':
            pl.assert_symptom(s)
        else:
            pl.assert_no_symptom(s)
            break

# dirty way to make sure questions in app make sense


def normalize_question_format(name):
    if name == "coughing_blood_mucus" or name == "unusually_more_thirsty" or name == "coughing_blood_mucus_green_yellow" or name == "unvaccinated_for_pneumonia" or name == "malnourished" or name == "unusually_more_thirsty" or name == "urinating_often":
        return "Are you " + normalize_prolog_names(name) + "?"
    elif name == "works_wt_animals" or name == "lives_in_urban" or name == "lives_near_stagnant_water":
        return "Do you " + normalize_prolog_names(name) + "?"
    elif name == "smoker":
        return "Are you a " + normalize_prolog_names(name) + "?"
    elif name == "given_birth_to_9_pound_baby" or name == "gestational_diabetes" or name == "type_2_diabetes" or name == "chemotherapy" or name == "intestine_removal_surgery" or name == "gallbladder_removal_surgery":
        return "Have you ever had" + normalize_prolog_names(name) + "?"
    elif name == "long_term_steroids" or name == "antacids_wt_magnesium" or name == "antibiotics":
        return "Have you taken " + normalize_prolog_names(name) + "recently?"
    else:
        return "Do you have " + normalize_prolog_names(name) + "?"


def normalize_prolog_names(name):
    return re.sub(r'([a-z])([A-Z])', r'\1 \2', name).replace('_', ' ').title()
