Kazakh-Tutor MINI — Intelligent Kazakh Vocabulary Trainer
1000 Words • Difficulty Levels • Machine Learning • User Statistics • Flask Web Application

Kazakh-Tutor MINI is a full-stack Python web application designed to help users learn Kazakh vocabulary effectively.
It includes a global dictionary of 1000 words, difficulty levels, an adaptive training system, machine learning prediction, user statistics, and a clean modern interface.

Features
1000-word global dictionary

Words are categorized into levels:

Beginner

A1

A2

B1

B2

Dictionary files:

tutor/data/global_1000_words.json  
tutor/data/words_Beginner.json  
tutor/data/words_A1.json  
tutor/data/words_A2.json  
tutor/data/words_B1.json  
tutor/data/words_B2.json  

Difficulty levels

Each user can select a level.
The level influences:

which words are imported

the difficulty of training

which words have priority

whether easier levels are included

Machine Learning (Logistic Regression)

A lightweight ML model analyzes the user’s performance and predicts the likelihood of answering each word correctly.

Features used:

time since last attempt

streak

accuracy

number of times shown

Words with lower predicted accuracy appear more frequently during training.

Statistics and visualization

The application generates analytical graphs:

overall accuracy

rolling accuracy (10-attempt window)

most difficult words

total attempts

Charts are generated using Matplotlib and stored in:

tutor/static/generated/

User account system

registration

login

personal word list

training history

difficulty level settings

Word import system

Users can import random words with one action.
Settings include:

number of words to import (50–300)

whether to include easier levels

Clean user interface

The web UI includes:

minimalistic dark theme

responsive layout

card-based design

clear navigation

structured forms and messages

Technologies Used

Backend:

Python

Flask

Flask-Login

SQLAlchemy

SQLite

Data and ML:

pandas

Matplotlib

scikit-learn

Frontend:

HTML

CSS

Installation
Windows (recommended)

Run:

run_windows.bat


This will create a virtual environment, install dependencies, and start the application.

Manual installation
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py


Open in the browser:

http://127.0.0.1:5000

Project Structure
kazakh-tutor-mini/
│ app.py
│ config.py
│ requirements.txt
│ README.md
│ run_windows.bat
│
├── tutor/
│   ├── templates/     
│   ├── static/        
│   ├── data/          
│   ├── models.py      
│   ├── services.py    
│   ├── dictionary.py  
│   ├── ml.py          
│   ├── stats.py       
│   ├── routes_web.py  
│   └── routes_api.py  
│
└── instance/kazakh_tutor.db

API Examples
Import random words:
POST /api/import
{
  "k": 100,
  "include_lower": true
}

Add a new word:
POST /api/words
{
  "prompt": "apple",
  "answer": "алма",
  "level": "Beginner"
}

Deployment

Compatible platforms:

Render

Railway

PythonAnywhere

Vercel (via Serverless WSGI)

Heroku-like environments

Purpose of the project

This project is intended to demonstrate:

full-stack Python development

integration of machine learning into a real application

working with databases and data processing

creation of a functional web application

UI/UX structure and user experience

building educational software tools

Author

Arslan Akhmet, Nauryzbek Temirlan CS-2429
Kazakh-Tutor MINI Project
