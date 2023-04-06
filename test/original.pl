%this is the original implementation
%1 no symptom means that the entire symptom list is false

:- dynamic has/1.
:- dynamic has_no/1.
:- dynamic age/1.
:- dynamic bmi/1.

yes_symp(X) :- symptom(X), unknown(X), asserta(has(X)), !.
no_symp(X) :- symptom(X), unknown(X), asserta(has_no(X)), !.
assert_age(A) :- number(A), \+ age(_), asserta(age(A)), !.
assert_bmi(A) :- number(A), \+ bmi(_), asserta(bmi(A)), !.

%definitions
yes(X) :- once(has(X)).
no(D) :- has_no(D), !.
no(D) :- disease(D),
    forall((
			clause(has(D), B),
			symptom_list(B, L)
		),
        once((member(S, L), no(S)))
	).
unknown(X) :- \+yes(X), \+no(X).
ysus(D) :- disease(D), yes(D), once(sus(D)).
nsus(D) :- (\+disease(D); no(D)), !.
nsus(D) :- 
    forall((
           clause(sus(D), B),
           symptom_list(B, L)
        ),
        once((member(S, L), no(S)))
	).
usus(D) :- \+ysus(D), \+nsus(D).


%query functions for disease
all_d(X) :- findall(D, disease(D), X).
all_yd(X) :- findall(D, (disease(D), yes(D)), X).
all_nd(X) :- findall(D, (disease(D), no(D)), X).
all_ud(X) :- findall(D, (disease(D), unknown(D)), X).

%query functions for symptoms
all_s(X) :- findall(S, symptom(S), X).
all_ys(X) :- findall(S, (symptom(S), yes(S)), X).
all_ns(X) :- findall(S, (symptom(S), no(S)), X).
all_us(X) :- findall(S, (symptom(S), unknown(S)), X).

%query functions for symptoms of a disease
all_ds(D, X) :- disease(D),
    findall(L, (
   		clause(has(D), B),
	    symptom_list(B, L)
	), X).
all_yds(D, X) :- disease(D),
    findall(L, (
        clause(has(D), B),
        symptom_list(B, L),
		forall(member(S, L), yes(S))
    ), X).
all_nds(D, X) :- disease(D),
    findall(L, (
		clause(has(D), B),
		symptom_list(B, L),
		once((member(S, L), no(S)))
    ), X).
all_uds(D, X) :- disease(D),
    findall(L, (
		clause(has(D), B),
		symptom_list(B, L),
		\+once((member(S, L), no(S))),
		\+forall(member(S, L), yes(S))
    ), X).

%query functions for susceptible diseases
all_susd(X) :-
    findall(A, (disease(A), clause(sus(A), _)), L),
    sort(L, X).
all_ysusd(X) :- findall(D, (disease(D), ysus(D)), X).
all_nsusd(X) :- findall(D, (disease(D), nsus(D)), X).
all_ususd(X) :- findall(D, (disease(D), usus(D)), X).

%query functions for symptoms of a susceptible disease
all_susds(D, X) :- disease(D),
    findall(L, (
		clause(sus(D), B),
		symptom_list(B, L)
	), X).
all_ysusds(D, X) :- disease(D),
    findall(L, (
		clause(sus(D), B),
		symptom_list(B, L),
		forall(member(S, L), yes(S))
	), X).
all_nsusds(D, X) :- disease(D),
    findall(L, (
		clause(sus(D), B),
		symptom_list(B, L),
		once((member(S, L), no(S)))
	), X).
all_ususds(D, X) :- disease(D),
    findall(L, (
		clause(sus(D), B),
		symptom_list(B, L),
		\+once((member(S, L), no(S))),
		\+forall(member(S, L), yes(S))
	), X).

%typing is hard
%python query functions
ay(S) :- yes_symp(S). % Asserts a 'yes' symptom into the knowledge base. This is used to mark a symptom as present in the patient.
an(S) :- no_symp(S). % Asserts a 'no' symptom into the knowledge base. This is used to mark a symptom as absent in the patient.
d :- all_d(X), write(X), nl. % Lists all known diseases.
yd :- all_yd(X), write(X), nl. % Lists all diseases with 'yes' symptoms in the patient.
nd :- all_nd(X), write(X), nl. % Lists all diseases with 'no' symptoms in the patient.
ud :- all_ud(X), write(X), nl. % Lists all diseases with 'unknown' symptoms in the patient.
s :- all_s(X), write(X), nl. % Lists all known symptoms.
ys :- all_ys(X), write(X), nl. % Lists all symptoms marked as 'yes' in the patient.
ns :- all_ns(X), write(X), nl. % Lists all symptoms marked as 'no' in the patient.
us :- all_us(X), write(X), nl. % Lists all symptoms marked as 'unknown' in the patient.
ds(D) :- all_ds(D, X), write(X), nl. % Lists all symptoms for a given disease.
yds(D) :- all_yds(D, X), write(X), nl. % Lists of symptoms where disease resolves to 'yes'.
nds(D) :- all_nds(D, X), write(X), nl. % Lists of symptoms where disease resolves to 'no'.
uds(D) :- all_uds(D, X), write(X), nl. % Lists of symptoms where disease resolves to 'unknown'.
susd :- all_susd(X), write(X), nl. % Lists all diseases that can be susceptible
ysusd :- all_ysusd(X), write(X), nl. % Lists all diseases the user is susceptible to
nsusd :- all_nsusd(X), write(X), nl. % Lists all diseases the user is not susceptible to
ususd :- all_ususd(X), write(X), nl. % Lists all diseases with unknown susceptibility
susds(D) :- all_susds(D, X), write(X), nl. % Lists all symptoms for a specific susceptible disease
ysusds(D) :- all_ysusds(D, X), write(X), nl. % Lists all symptoms the user has for a specific susceptible disease
nsusds(D) :- all_nsusds(D, X), write(X), nl. % Lists all symptoms the user doesn't have for a specific susceptible disease
ususds(D) :- all_ususds(D, X), write(X), nl. % Lists all symptoms with unknown status for a specific susceptible disease


%helpers
symptom_list(has(Term), [Term]).
symptom_list((has(Term1), Term2), [Term1|List]) :- 
    symptom_list(Term2, List), !.



%knowledge base
has(malaria) :- has(fever), has(sweats), has(chills), has(headache), has(malaise), has(muscle_aches), has(nausea), has(vomiting), has(myalgias).

has(tuberculosis) :- has(cough), has(coughing_blood_mucus), has(chest_pain), has(painful_breathing), has(night_sweats), has(weight_loss), has(no_appetite), has(tiredness).

has(dengue) :- has(fever), has(nausea), has(vomiting).
has(dengue) :- has(fever), has(rash).
has(dengue) :- has(fever), has(eye_pain).
has(dengue) :- has(fever), has(muscle_aches).
has(dengue) :- has(fever), has(joint_pain).
has(dengue) :- has(fever), has(bone_pain).

has(type_1_diabetes) :- has(unusually_more_thirsty), has(urinating_often), has(weight_loss), has(tiredness), has(irritability), has(blurry_vision), has(frequent_infections).
has(type_1_diabetes) :- has(nausea), has(vomiting), has(stomach_pains), has(weight_loss).

has(type_2_diabetes) :- has(prediabetes), has(overweight), has(gestational_diabetes), has(given_birth_to_9_pound_baby).
has(type_2_diabetes) :- has(yeast_infections), has(slow_healing_sores_cuts), has(pain_numbness_in_feat_legs).

has(gestational_diabetes) :- has(given_birth_to_9_pound_baby), has(overweight), has(polycystic_ovary_syndrome).

has(hypertension) :- has(severe_headache), has(chest_pain), has(dizziness), has(difficulty_breathing), has(nausea).
has(hypertension) :- has(vomiting), has(blurry_vision), has(anxiety), has(confusion), has(buzzing_ears), has(nosebleeds), has(abnormal_heart_rhythm).

has(stroke) :- has(numbness_face), has(numbness_arm), has(numbness_leg), has(numbness_one_side_body), has(sudden_confusion), has(trouble_speaking), has(difficulty_understanding_speech), has(blurry_vision), has(trouble_walking), has(dizziness), has(loss_of_balance), has(lack_of_coordination), has(sudden_severe_headache).

has(asthma) :- has(difficulty_breathing), has(chest_pain), has(wheezing), has(trouble_sleeping), has(cough), has(respiratory_virus).

has(leptospirosis) :- has(high_fever), has(headache), has(chills), has(muscle_aches), has(vomiting), has(jaundice), has(red_eyes), has(stomach_pains), has(diarrhea), has(rash).

has(pneumonia) :- has(low_body_temperature), has(coughing_blood_mucus_green_yellow), has(fever), has(sweats), has(chills), has(difficulty_breathing), has(chest_pain), has(no_appetite), has(low_energy), has(fatigue), has(nausea), has(vomiting), has(confusion).

has(diarrhea) :- has(stomach_pains), has(bloating), has(nausea), has(vomiting), has(fever), has(blood_in_stool), has(mucus_in_stool), has(urgent_bowel_movement).

%numeric symptoms
has(obese) :- bmi(B), B >= 30.
has(overweight) :- bmi(B), B >= 25.
has(underweight) :- bmi(B), B =< 18.5.
has(elder) :- age(A), A >= 65.
has(early_old) :- age(A), A >= 45.
has(mid_age) :- age(A), A >= 25.
has(teen) :- age(A), A >= 13, A =< 19.
has(child) :- age(A), A =< 12.
has(infant) :- age(A), A =< 1.
%this is required else has_no will always be false even if they are true
has_no(obese) :- bmi(B), B < 30.
has_no(overweight) :- bmi(B), B < 25.
has_no(underweight) :- bmi(B), B > 18.5.
has_no(elder) :- age(A), A < 65.
has_no(early_old) :- age(A), A < 45.
has_no(mid_age) :- age(A), A < 25.
has_no(teen) :- age(_), \+has(teen).
has_no(child) :- age(A), A > 12.
has_no(infant) :- age(A), A > 1.

%diseases
disease(malaria).
disease(tuberculosis).
disease(dengue).
disease(type_1_diabetes).
disease(type_2_diabetes).
disease(gestational_diabetes).
disease(hypertension).
disease(stroke).
disease(asthma).
disease(leptospirosis).
disease(pneumonia).
disease(diarrhea).

%symptoms of diseases
symptom(fever).
symptom(sweats).
symptom(chills).
symptom(headache).
symptom(malaise).
symptom(muscle_aches).
symptom(nausea).
symptom(vomiting).
symptom(myalgias).
symptom(cough).
symptom(coughing_blood_mucus).
symptom(chest_pain).
symptom(painful_breathing).
symptom(night_sweats).
symptom(weight_loss).
symptom(no_appetite).
symptom(tiredness).
symptom(rash).
symptom(eye_pain).
symptom(joint_pain).
symptom(bone_pain).
symptom(unusually_more_thirsty).
symptom(urinating_often).
symptom(irritability).
symptom(blurry_vision).
symptom(frequent_infections).
symptom(stomach_pains).
symptom(prediabetes).
symptom(overweight).
symptom(gestational_diabetes).
symptom(given_birth_to_9_pound_baby).
symptom(yeast_infections).
symptom(slow_healing_sores_cuts).
symptom(pain_numbness_in_feat_legs).
symptom(polycystic_ovary_syndrome).
symptom(severe_headache).
symptom(dizziness).
symptom(difficulty_breathing).
symptom(anxiety).
symptom(confusion).
symptom(buzzing_ears).
symptom(nosebleeds).
symptom(abnormal_heart_rhythm).
symptom(numbness_face).
symptom(numbness_arm).
symptom(numbness_leg).
symptom(numbness_one_side_body).
symptom(sudden_confusion).
symptom(trouble_speaking).
symptom(difficulty_understanding_speech).
symptom(trouble_walking).
symptom(loss_of_balance).
symptom(lack_of_coordination).
symptom(sudden_severe_headache).
symptom(wheezing).
symptom(trouble_sleeping).
symptom(respiratory_virus).
symptom(high_fever).
symptom(jaundice).
symptom(red_eyes).
symptom(diarrhea).
symptom(low_body_temperature).
symptom(coughing_blood_mucus_green_yellow).
symptom(low_energy).
symptom(fatigue).
symptom(bloating).
symptom(blood_in_stool).
symptom(mucus_in_stool).
symptom(urgent_bowel_movement).

%symptoms for susceptibility
symptom(early_old).
symptom(mid_age).
symptom(allergic_condition).
symptom(underweight).
symptom(malnourished).
symptom(type_2_diabetes).
symptom(severe_kidney_disease).
symptom(works_wt_animals).
symptom(elder).
symptom(teen).
symptom(high_intake_of_alcohol).
symptom(weak_immune_system).
symptom(inactive_lifestyle).
symptom(chemotherapy).
symptom(organ_transplant_medications).
symptom(child).
symptom(psoriasis).
symptom(infant).
symptom(smoke_exposure).
symptom(pregnant).
symptom(intestine_removal_surgery).
symptom(smoker).
symptom(type_1_diabetes).
symptom(frequent_water_activites).
symptom(unvaccinated_for_pneumonia).
symptom(lives_near_stagnant_water).
symptom(immediate_family_wt_type_2_diabetes).
symptom(lives_in_urban).
symptom(non_immunes).
symptom(gestational_diabetes).
symptom(cancer_drugs).
symptom(lactose_intolerant).
symptom(obese).
symptom(hiv_aids).
symptom(neck_cancer).
symptom(girl).
symptom(gallbladder_removal_surgery).
symptom(high_salt_diet).
symptom(works_outdoors).
symptom(head_cancer).
symptom(hereditary).
symptom(chronic_illness).
symptom(crohns_disease).
symptom(antibiotics).
symptom(overweight).
symptom(long_term_steroids).
symptom(antacids_wt_magnesium).


%susceptible
sus(malaria) :- has(elder).
sus(malaria) :- has(pregnant).
sus(malaria) :- has(non_immunes).
sus(malaria) :- has(chronic_illness).
sus(tuberculosis) :- has(smoker).
sus(tuberculosis) :- has(hiv_aids).
sus(tuberculosis) :- has(type_1_diabetes).
sus(tuberculosis) :- has(type_2_diabetes).
sus(tuberculosis) :- has(gestational_diabetes).
sus(tuberculosis) :- has(severe_kidney_disease).
sus(tuberculosis) :- has(head_cancer), has(neck_cancer).
sus(tuberculosis) :- has(chemotherapy).
sus(tuberculosis) :- has(underweight).
sus(tuberculosis) :- has(malnourished).
sus(tuberculosis) :- has(crohns_disease).
sus(tuberculosis) :- has(psoriasis).
sus(tuberculosis) :- has(organ_transplant_medications).
sus(dengue) :- has(infant).
sus(dengue) :- has(pregnant).
sus(dengue) :- has(lives_near_stagnant_water).
sus(type_1_diabetes) :- has(child).
sus(type_1_diabetes) :- has(teen).
sus(type_2_diabetes) :- has(early_old).
sus(type_2_diabetes) :- has(immediate_family_wt_type_2_diabetes).
sus(type_2_diabetes) :- has(inactive_lifestyle).
sus(gestational_diabetes) :- has(pregnant).
sus(gestational_diabetes) :- has(girl), has(mid_age).
sus(gestational_diabetes) :- has(girl), has(immediate_family_wt_type_2_diabetes).
sus(hypertension) :- has(elder).
sus(hypertension) :- has(hereditary).
sus(hypertension) :- has(overweight).
sus(hypertension) :- has(obese).
sus(hypertension) :- has(inactive_lifestyle).
sus(hypertension) :- has(high_salt_diet).
sus(hypertension) :- has(high_intake_of_alcohol).
sus(stroke) :- has(pregnant).
sus(stroke) :- has(smoker).
sus(stroke) :- has(overweight).
sus(stroke) :- has(inactive_lifestyle).
sus(stroke) :- has(type_1_diabetes).
sus(stroke) :- has(type_2_diabetes).
sus(stroke) :- has(high_intake_of_alcohol).
sus(asthma) :- has(hereditary).
sus(asthma) :- has(allergic_condition).
sus(asthma) :- has(lives_in_urban).
sus(asthma) :- has(smoke_exposure).
sus(asthma) :- has(overweight).
sus(asthma) :- has(obese).
sus(leptospirosis) :- has(works_outdoors).
sus(leptospirosis) :- has(works_wt_animals).
sus(leptospirosis) :- has(frequent_water_activites).
sus(pneumonia) :- has(unvaccinated_for_pneumonia).
sus(pneumonia) :- has(smoker).
sus(pneumonia) :- has(smoke_exposure).
sus(pneumonia) :- has(infant).
sus(pneumonia) :- has(elder).
sus(pneumonia) :- has(weak_immune_system).
sus(pneumonia) :- has(hiv_aids).
sus(pneumonia) :- has(organ_transplant_medications).
sus(pneumonia) :- has(chemotherapy).
sus(pneumonia) :- has(long_term_steroids).
sus(diarrhea) :- has(antibiotics).
sus(diarrhea) :- has(cancer_drugs).
sus(diarrhea) :- has(antacids_wt_magnesium).
sus(diarrhea) :- has(lactose_intolerant).
sus(diarrhea) :- has(gallbladder_removal_surgery).
sus(diarrhea) :- has(intestine_removal_surgery).
sus(diarrhea) :- has(child), has(malnourished).
