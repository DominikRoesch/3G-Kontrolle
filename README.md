# 3G-Kontrolle

## Introduction
The purpose of the present program is to easily check the presence and 3G-status at events. It was developed for religious events, where the regulation was that every person older than 18 years has to fulfill 3G-requirements. However, the existing program can easily be extended to other use cases. The two main tasks of the program are
- to collect the data for an attendance list,
- to document, that the 3G-status has been checked.

## Features
### General principle
Overall, there exists a GUI, where the user (e.g. the inspector) is able to enter all relevant information. The usual attendants are stored in a .csv database (*teilnehmerliste_demo.csv*). The attendance list is automatically created in a .csv list with todays date as filename. A 2G-status can be stored in the .csv database, such that there is no need to check it every time.
### "Eingabe der Anwesenheit und 3G-Kontrolle"
All family-IDs from the *teilnehmerliste_demo.csv* can be selected in the dropdown menu ore written in with autocompletition. Pressing "Daten anzeigen" displays all family members. "anwesend" is selected by default. If the person is less than 18 years old, "3G kontrolliert" is disabled (no need to check). It is also disabled, if the database already contains information about an existing 2G-status of the corresponding person. "Eingabe speichern" saves the data and clears all entries.
### "2G-Status in Datenbank einpflegen"
Here, the 2G-status can be stored in the database. Therefore, state the date until the 2G-status is active and press "2G-status speichern".
### "Anwesenheit Gast dokumentieren"
This section provides the possibility to document the presence of a person, that is not contained in the *teilnehmerliste_demo.csv*. Choose, whether the person is less than 18 years or whether you checked the 3G-status.

## How to run the program
There are two main possibilities, how to run the program. 
- Simply run the *3G_Kontrolle.exe* file. Make sure that it is in the same folder as *teilnehmerliste_demo.csv* and *images*. 
- Run the *3G_Kontrolle.py* file with python. Required packages can be installed from the *requirements.txt* file. Also make sure, that you run it from the directory where *teilnehmerliste_demo.csv* and *images* are located.

## Author
The code is written by Dominik Rösch. © Copyright 2022.
