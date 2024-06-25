# CarNeo_Client
## Table of Contents
1. [Introduction](#introduction)
2. [To Dos & Plans](#to-dos-&-plans)
3. [How To](#how-to)

## Introduction

## How To
Python 3 is required. <br>
1. Clone this repository `git clone https://github.com/kianwasabi/CarNeo_Client.git`.
2. Run `./setup.sh` to install all dependencies & activates the venv.
3. Run `python3 examples/carneo_client_example.py ` to run an example client application.

## 
Tested on MacOS 12.6.6 and Ubuntu 20.04.3 LTS. <br>
## Task
Für unser CarNEO-System stellen wir eine REST API zu Verfügung. <br>
Für die API soll ein Client entwickelt werden, der einen Minimalumfang von Funktionalität anderen Entwicklern zur Verfügung stellt. <br>
1. Authentifizierung
2. Abruf der eigenen Identität (GET /auth/own_identity)
3. Abruf der „Campaigns“ nach Organization und Project
4. Abruf einer einzelnen “Campaign” unter Zuhilfenahme der CampaignID
5. Erstellen eines „Projects“
 
Mit dem Begriff „Client“ ist keine UI gemeint, sondern Klassen bzw. eine Library, die von Entwicklern in ihrem Programm genutzt werden können. <br>
 
Die Kommunikation mit dem Backend erfolgt über REST-Mechanismen:

<img src="./docs/client_server_architecture.png" width="30%">

Die Authentifizierung erfolgt über einen Token-Exchange: <br>
Das Backend speichert einen Public-Key und der Client speichert einen Private-Key. <br>
Der Client muss mit dem Private-Key einen JWT-Token erzeugen und an das Backend schicken (Initialtoken). <br>
Anschließend erhält der Client einen Token, das für die restlichen API-Calls verwendet werden kann. <br>
 
Die Payload des Initialtokens beinhaltet die folgenden Claims:
 - „org“: Eine UUID, die einer Organisation in dem System zugeordnet ist.
- „acc“: Eine UUID, die einem Account in dem System zugeordnet ist.
- „key“: Eine UUID, die einem Public-Key in dem System zugeordnet ist.
- „iat“: Zeitstempel der Token-Erstellung
- „exp“: Zeitstempel an dem der Token ungültig wird (Max 1 Stunde)
 
Dieser Client soll in einer Programmiersprache Ihrer Wahl entwickelt werden. Die Nutzung von Dependencies ist zulässig, die Nutzung eines Code-Generators nicht.
 
Eine Dokumentation der REST-API kann hier eingesehen werden: https://api.dev.carneo.cloud/docs 

## To Dos
- [x] Authentification
- [] Authentification Test
- [x] Method Invokation
- [] Method Invokation Test
- [] Pagniation
- [] Pagniation Test
- [] Documentation

### Questions: 
- HS256 or RS256? <br>
- Where does the UUID come from? <br>
- get_identiy without barer token in header? <br>
- mhhh... „key“: Eine UUID, die einem Public-Key in dem System zugeordnet ist.


