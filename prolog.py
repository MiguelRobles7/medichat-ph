from subprocess import Popen, PIPE

def _parse_list(str, depth):
	if depth == 0:
		return str
	depth -= 1
	res = []
	for s in map(lambda x: x.strip(), str[1:-1].split(',')):
		res.append(_parse_list(s, depth))
	return res
def _parse_pl_list(str, depth = 1):
	return _parse_list(str[:str.index('\n')], depth)

class PrologShell:
	def __init__(self, program_file):
		self.prolog = Popen(['/Applications/SWI-Prolog.app/Contents/MacOS/swipl', '-q', program_file], stdin=PIPE, stdout=PIPE, universal_newlines=True)
		
	def query(self, query_string):
		# Send query to Prolog process
		self.prolog.stdin.write(query_string + '\n')
		self.prolog.stdin.flush()

		res = []
		while True:
			line = self.prolog.stdout.readline().strip()
			if line == '':
				break
			res.append(line)
		return '\n'.join(res)
		
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

	def get_all_symptoms_for_disease(self, disease):
		# Lists all symptoms for a given disease.
		return _parse_pl_list(self.query(f"ds('{disease}')."), 2)

	def get_yes_symptoms_for_disease(self, disease):
		# Lists of symptoms where disease resolves to 'yes'.
		return _parse_pl_list(self.query(f"yds('{disease}')."), 2)

	def get_no_symptoms_for_disease(self, disease):
		# Lists of symptoms where disease resolves to 'no'.
		return _parse_pl_list(self.query(f"nds('{disease}')."), 2)

	def get_unknown_symptoms_for_disease(self, disease):
		# Lists of symptoms where disease resolves to 'unknown'.
		return _parse_pl_list(self.query(f"uds('{disease}')."), 2)

	def get_all_susceptible_diseases(self):
		return _parse_pl_list(self.query("susd."))

	def get_yes_susceptible_diseases(self):
		return _parse_pl_list(self.query("ysusd."))

	def get_no_susceptible_diseases(self):
		return _parse_pl_list(self.query("nsusd."))

	def get_unknown_susceptible_diseases(self):
		return _parse_pl_list(self.query("ususd."))

	def get_all_susceptible_disease_symptoms(self, disease):
		return _parse_pl_list(self.query(f"susds('{disease}')."), 2)

	def get_yes_susceptible_disease_symptoms(self, disease):
		return _parse_pl_list(self.query(f"ysusds('{disease}')."), 2)

	def get_no_susceptible_disease_symptoms(self, disease):
		return _parse_pl_list(self.query(f"nsusds('{disease}')."), 2)

	def get_unknown_susceptible_disease_symptoms(self, disease):
		return _parse_pl_list(self.query(f"ususds('{disease}')."), 2)
		
	def __del__(self):
		# Close the Prolog process when the wrapper is deleted
		self.prolog.stdin.write('halt.\n')
		self.prolog.stdin.flush()
		self.prolog.stdin.close()
		self.prolog.stdout.close()
		self.prolog.kill()
