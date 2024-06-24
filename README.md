# CarNeo_Client

Programmierung:
Für unser CarNEO-System stellen wir eine REST API zu Verfügung. Für die API soll ein Client entwickelt werden, der einen Minimalumfang von Funktionalität anderen Entwicklern zur Verfügung stellt:
 
1.      Authentifizierung
2.      Abruf der eigenen Identität (GET /auth/own_identity)
3.      Abruf der „Campaigns“ nach Organization und Project
4.      Abruf einer einzelnen “Campaign” unter Zuhilfenahme der CampaignID
5.      Erstellen eines „Projects“
 
Mit dem Begriff „Client“ ist keine UI gemeint, sondern Klassen bzw. eine Library, die von Entwicklern in ihrem Programm genutzt werden können.
 
Die Kommunikation mit dem Backend erfolgt über REST-Mechanismen:

![image002](https://github.com/kianwasabi/CarNeo_Client/assets/55065075/597a14fb-b147-4f1b-a595-90d607b5d466)


Die Authentifizierung erfolgt über einen Token-Exchange: Das Backend speichert einen Public-Key und der Client speichert einen Private-Key. Der Client muss mit dem Private-Key einen JWT-Token erzeugen und an das Backend schicken (Initialtoken). Anschließend erhält der Client einen Token, das für die restlichen API-Calls verwendet werden kann.
 
Die Payload des Initialtokens beinhaltet die folgenden Claims:
 
·         „org“: Eine UUID, die einer Organisation in dem System zugeordnet ist
·         „acc“: Eine UUID, die einem Account in dem System zugeordnet ist
·         „key“: Eine UUID, die einem Public-Key in dem System zugeordnet ist
·         „iat“: Zeitstempel der Token-Erstellung
·         „exp“: Zeitstempel an dem der Token ungültig wird (Max 1 Stunde)
 
Dieser Client soll in einer Programmiersprache Ihrer Wahl entwickelt werden. Die Nutzung von Dependencies ist zulässig, die Nutzung eines Code-Generators nicht.
 
Eine Dokumentation der REST-API kann hier eingesehen werden: https://api.dev.carneo.cloud/docs 
