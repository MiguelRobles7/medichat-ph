from subprocess import Popen, PIPE
import ast
import re

F = open('prolog_log.txt', 'w')


def _parse_pl_list(str: str):
    str = str[:str.index('\n')]
    str = re.sub(r'\w+', "'\g<0>'", str)
    return ast.literal_eval(str)


class PrologShell:
    def __init__(self, program_file):
        self.prolog = Popen(['/Program Files/swipl/bin/swipl.exe', '-q',
                            program_file], stdin=PIPE, stdout=PIPE, universal_newlines=True)
        occurence = {}
        self._symptom_occurence = occurence
        for s in self.get_all_symptoms():
            occurence[s] = 0
        for d in self.get_all_diseases():
            for symptoms in self.get_all_disease_symptoms(d):
                for s in symptoms:
                    occurence[s] += 1

    def query(self, query_string):
        # Send query to Prolog process
        self.prolog.stdin.write(query_string + '\n')
        self.prolog.stdin.flush()
        F.write(query_string + '\n')

        res = []
        while True:
            line = self.prolog.stdout.readline().strip()
            if line == '':
                break
            res.append(line)
        return '\n'.join(res)

    def get_symptom_occurence(self, symptom):
        return self._symptom_occurence.get(symptom, 0)

    def assert_symptom(self, symptom):
        self.query(f'ay({symptom}).')

    def assert_no_symptom(self, symptom):
        self.query(f'an({symptom}).')

    def assert_gender(self, gender):
        gender = 'male' if gender[0].lower() == 'm' else 'female'
        self.assert_symptom(gender)

    def assert_bmi(self, bmi):
        self.query(f'assert_bmi({bmi}).')

    def assert_age(self, age):
        self.query(f'assert_age({age}).')

    def get_all_diseases(self):
        # Lists all known diseases.
        return _parse_pl_list(self.query("d."))

    def get_yes_diseases(self):
        # Lists all diseases with 'yes' symptoms in the patient.
        return _parse_pl_list(self.query("yd."))

    def get_no_diseases(self):
        # Lists all diseases with 'no' symptoms in the patient.
        return _parse_pl_list(self.query("nd."))

    def get_unknown_diseases(self):
        # Lists all diseases with 'unknown' symptoms in the patient.
        return _parse_pl_list(self.query("ud."))

    def get_all_symptoms(self):
        # Lists all known symptoms.
        return _parse_pl_list(self.query("s."))

    def get_yes_symptoms(self):
        # Lists all symptoms marked as 'yes' in the patient.
        return _parse_pl_list(self.query("ys."))

    def get_no_symptoms(self):
        # Lists all symptoms marked as 'no' in the patient.
        return _parse_pl_list(self.query("ns."))

    def get_unknown_symptoms(self):
        # Lists all symptoms marked as 'unknown' in the patient.
        return _parse_pl_list(self.query("us."))

    def get_all_disease_symptoms(self, disease):
        # Lists all symptoms for a given disease.
        return _parse_pl_list(self.query(f"ds('{disease}')."))

    def get_yes_disease_symptoms(self, disease):
        # Lists of symptoms where disease resolves to 'yes'.
        return _parse_pl_list(self.query(f"yds('{disease}')."))

    def get_no_disease_symptoms(self, disease):
        # Lists of symptoms where disease resolves to 'no'.
        return _parse_pl_list(self.query(f"nds('{disease}')."))

    def get_unknown_disease_symptoms(self, disease):
        # Lists of symptoms where disease resolves to 'unknown'.
        return _parse_pl_list(self.query(f"uds('{disease}')."))

    def get_all_susceptible_diseases(self):
        return _parse_pl_list(self.query("susd."))

    def get_yes_susceptible_diseases(self):
        return _parse_pl_list(self.query("ysusd."))

    def get_no_susceptible_diseases(self):
        return _parse_pl_list(self.query("nsusd."))

    def get_unknown_susceptible_diseases(self):
        return _parse_pl_list(self.query("ususd."))

    def get_all_susceptible_disease_symptoms(self, disease):
        return _parse_pl_list(self.query(f"susds('{disease}')."))

    def get_yes_susceptible_disease_symptoms(self, disease):
        return _parse_pl_list(self.query(f"ysusds('{disease}')."))

    def get_no_susceptible_disease_symptoms(self, disease):
        return _parse_pl_list(self.query(f"nsusds('{disease}')."))

    def get_unknown_susceptible_disease_symptoms(self, disease):
        return _parse_pl_list(self.query(f"ususds('{disease}')."))

    def __del__(self):
        # Close the Prolog process when the wrapper is deleted
        self.prolog.stdin.write('halt.\n')
        self.prolog.stdin.flush()
        self.prolog.stdin.close()
        self.prolog.stdout.close()
        self.prolog.kill()
        F.close()
