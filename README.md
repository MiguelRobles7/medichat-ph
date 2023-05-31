# medichat-ph

Major Course Output 2 for CSINTSY (Intelligent Systems) class at De La Salle University. An online medical diagnosis chatbot using Flask and Prolog.

## **WARNING**
This project was made mainly to showcase the students' skills in using Prolog for a real life scenario, **NOT for actual use.**

## Handled Diseases 
- malaria
- tuberculosis
- dengue fever
- diabetes
  - type 1
  - type 2
  - gestational
- hypertension
- stroke
- asthma
- leptospirosis
- pneumonia
- diarrhea

## **Prerequisites**

Install `Python => version 3.11` & `Pip3`

## **Developing**

Starting Off, in Powershell

```bash
  git clone https://github.com/MiguelRobles7/medical-chatbot & cd medical-chatbot
  pip install virtualenv
  python -m virtualenv env
  .\env\Scripts\activate.ps1
  pip install -r requirements.txt
```

## **Running Project**

```bash
  flask --app app.py --debug run
```

Then access the project with the given link

## Troubleshooting

- **PrologShell object has no attribute 'prolog'** - By default the app points to Swi-Prolog's default install path, if it is somewhere else on your device, find the path to `swipl.exe` and replace line 16 in `medical-chatbot/prolog.py`
- **Error on `.\env\Scripts\activate.ps1`** - This has something to do with windows' default execution policy. Try running `Set-ExecutionPolicy Unrestricted -Scope Process` in an admin powershell. Read more [here.](https://stackoverflow.com/questions/18713086/virtualenv-wont-activate-on-windows)

- **`flask --app app.py --debug run` isn't working** - Make sure you are inside the virtual environment by running `.\env\Scripts\activate.ps1`

- **High memory usage on Mac** - For some reason virtualenv consumes a lot of memory on Mac, in this case, while not recommended, running without a virtual environment is the only alternative. Simply run `pip install -r requirements.txt`

## Screenshots

![App Screenshot](https://github.com/MiguelRobles7/medichat-ph/blob/main/screenshots/home.png)
![App Screenshot](https://github.com/MiguelRobles7/medichat-ph/blob/main/screenshots/initial_questions.png)
![App Screenshot](https://github.com/MiguelRobles7/medichat-ph/blob/main/screenshots/symptoms_questions.png)
![App Screenshot](https://github.com/MiguelRobles7/medichat-ph/blob/main/screenshots/results.png)


## Developers
- [@MiguelRobles7]()
- [@qwerttyuiiop1](https://github.com/qwerttyuiiop1)
