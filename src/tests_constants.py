# ---- Column keys ----
# Student id
STUDENT_ID_KEY = "_student_id"
# Quel est l’affichage produit par le programme ci-dessous lorsqu’il est lancé ?  
Q1_KEY = "_Q1"
# Le programme ci-dessous doit afficher « Bla Bla Bla Bla Bla » lorsqu’il est lancé :    Quelle valeur donner au code manquant ? 
Q2_KEY = "_Q2"
# Quel est l’affichage produit par le programme ci-dessous lorsqu’il est lancé ?
Q3_KEY = "_Q3"
# Quel est l’affichage produit par le programme ci-dessous lorsqu’il est lancé ?  Pour information, l'opérateur * permet d’effectuer une multiplication.   
Q4_KEY = "_Q4"
#  Quel est l’affichage produit par le programme ci-dessous lorsqu’il est lancé ?   
Q5_KEY = "_Q5"
# Le programme ci-dessous doit afficher « Adulte » lorsqu’il est lancé :    Quel est le code manquant ? 
Q6_KEY = "_Q6"
# Le programme ci-dessous doit calculer le périmètre d’un cercle à l’aide de la formule suivante :P=2×?×R   avec ??3,14 et R le rayon du cercle.    Quel est le code manquant ?
Q7_KEY = "_Q7"
# Que fait le programme ci-dessous lorsqu’il est lancé ?   
Q8_KEY = "_Q8"
# Quel est l’affichage produit par le programme ci-dessous lorsqu’il est lancé ?   
Q9_KEY = "_Q9"
# Est-ce que tu as trouvé les aides utiles pour progresser dans le jeu ?
QA_KEY = "_QA"
# Est-ce que tu as trouvé les aides utiles pour apprendre à programmer en Python ?
QB_KEY = "_QB"
# Est-ce que tu aimerais encore avoir de l'aide d'un assistant numérique dans le futur ?
QC_KEY = "_QC"
# Est-ce que tu as trouvé les aides faciles à comprendre ?
QD_KEY = "_QD"
# Est-ce que tu as trouvé que les aides étaient correctes (sans erreurs) ?
QE_KEY = "_QE"
# Explique ce que tu as le plus aimé et le moins aimé à propos des aides.[Le plus aimé]
QF_KEY = "_QF"
# Explique ce que tu as le plus aimé et le moins aimé à propos des aides.[Le moins aimé]
QG_KEY = "_QG"
# Si tu le veux bien, tu peux nous indiquer ton genre : [mod B/C]
QH_KEY = "_QH" # Merged in GENDER_KEY
# Est-ce que tu as trouvé que les ressources disponibles dans le jeu (consignes + mémo de programmation) étaient suffisantes pour progresser ?
QI_KEY = "_QI"
# Est-ce que tu aurais aimé avoir plus d’aide dans le jeu ?
QJ_KEY = "_QJ"
# Si tu le veux bien, tu peux nous indiquer ton genre : [mod A]
QK_KEY = "_QK" # Merged in GENDER_KEY
# Date de lancement du questionnaire (format 06/10/2025 13:25)
T1_KEY = "_T1"
# Date de soumission du questionnaire
T2_KEY = "_T2"
# Added during processing
GAME_ID_KEY = "_game_id"
GROUP_ID_KEY = "_group_id"
GENDER_KEY = "_gender" # Merge of QH_KEY and QK_KEY

PROGRAMMING_QUESTIONS = [
    Q1_KEY,
    Q2_KEY,
    Q3_KEY,
    Q4_KEY,
    Q5_KEY,
    Q6_KEY,
    Q7_KEY,
    Q8_KEY,
    Q9_KEY,
]

VAR_NOTION_QUESTIONS = [Q1_KEY, Q4_KEY, Q7_KEY]
FOR_LOOP_NOTION_QUESTIONS =  [Q2_KEY, Q5_KEY, Q8_KEY]
COND_NOTION_QUESTIONS = [Q3_KEY, Q6_KEY, Q9_KEY]

ASSISTANT_NUM_QUESTIONS = [
    QA_KEY,
    QB_KEY,
    QD_KEY,
    QE_KEY,
    QC_KEY,
]

ASSISTANT_QUAL_QUESTIONS = [
    QF_KEY,
    QG_KEY,
]

HELP_QUESTIONS = [
    QI_KEY,
    QJ_KEY,
]
GENDER_QUESTIONS = [
    QH_KEY,
    QK_KEY,
]
TIME_INFO = [
    T1_KEY,
    T2_KEY,
]

PRE_TEST_KEYS = \
    [STUDENT_ID_KEY] \
    + PROGRAMMING_QUESTIONS \
    + TIME_INFO

POST_TEST_KEYS = \
    [STUDENT_ID_KEY]  \
    + PROGRAMMING_QUESTIONS \
    + ASSISTANT_NUM_QUESTIONS \
    + ASSISTANT_QUAL_QUESTIONS \
    + HELP_QUESTIONS \
    + GENDER_QUESTIONS \
    + TIME_INFO

# ---- Column values ----

GENDER_MALE = "M";
GENDER_FEMALE = "F";
GENDER_OTHER = "O";
GENDER_NO_ANSWER = "NA";

GROUP_A="A"
GROUP_B="B"
GROUP_C="C"

ANSWERS_SCORES = {
    Q1_KEY : {
        "A": 0,
        "B": 0,
        "C": 0,
        "D": 1,
        "E": 0,
    },
    Q2_KEY : {
        "A": 0,
        "B": 0,
        "C": 0,
        "D": 0,
        "E": 1,
    },
    Q3_KEY : {
        "A": 0,
        "B": 0,
        "C": 0,
        "D": 0,
        "E": 1,
    },
    Q4_KEY : {
        "A": 0,
        "B": 0,
        "C": 0,
        "D": 0,
        "E": 1,
    },
    Q5_KEY : {
        "A": 1,
        "B": 0,
        "C": 0,
        "D": 0,
        "E": 0,
    },
    Q6_KEY : {
        "A": 1,
        "B": 0,
        "C": 0,
        "D": 0,
        "E": 0,
    },
    Q7_KEY : {
        "A": 0,
        "B": 1,
        "C": 0,
        "D": 0,
        "E": 0,
    },
    Q8_KEY : {
        "A": 0,
        "B": 0,
        "C": 0,
        "D": 1,
        "E": 0,
    },
    Q9_KEY : {
        "A": 0,
        "B": 0,
        "C": 0,
        "D": 1,
        "E": 0,
    },
}