from prolog import PrologShell
import re
import itertools

pl = PrologShell('prolog.pl')

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
	return max(symptoms, key = lambda x: pl.get_symptom_occurence(x))

def confirm_symptom(s):
	y = input(f'Do you have ' + s.replace('_', ' ') + '? ').rstrip()
	if y[0].lower() == 'y':
		pl.assert_symptom(s)
	else:
		pl.assert_no_symptom(s)
if __name__ == "__main__":
	pl.assert_bmi(int(input('Enter bmi: ')))
	pl.assert_age(int(input('Enter age: ')))
	pl.assert_gender(input('Enter gender (m/f): '))
	symptoms = input('What symptoms are you currently experiencing?\n').strip()
	if symptoms:
		for s in map(lambda x: x.strip(), symptoms.split(',')):
			s = re.sub(r'\s+', '_', s)
			pl.assert_symptom(s)
	while True:
		unknown_diseases = pl.get_unknown_diseases()
		if not unknown_diseases:
			break
		symptoms = itertools.chain.from_iterable(
			map(pl.get_unknown_disease_symptoms, unknown_diseases)
		)
		to_confirm = find_symptom_to_confirm(symptoms)
		confirm_symptom(to_confirm)
	while True:
		unknown_sus = pl.get_unknown_susceptible_diseases()
		if not unknown_sus:
			break
		symptoms = itertools.chain.from_iterable(
			map(pl.get_unknown_susceptible_disease_symptoms, unknown_sus)
		)
		to_confirm = find_symptom_to_confirm(symptoms)
		confirm_symptom(to_confirm)

	print('You have:')
	for d in pl.get_yes_diseases():
		print('\t' + d)
	print('You are susceptible to:')
	for d in pl.get_yes_susceptible_diseases():
		print('\t' + d)
