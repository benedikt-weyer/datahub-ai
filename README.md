### Zielsetzung

Unser Ziel ist mithilfe des Einsatzes von LLM's die Datenbereitstellung im Bereich Public Health zu verbessern. Dabei möchten wir anhand der verfügbaren Daten wie bei DataHub einen ChatBot zu erstellen, welche die Exploration und Abfragen deiser Daten vereinfacht. Durch die Anwendung von LLM's, nämlich KI, ermöglichen wir nicht-technischen Fachleuten, wie Akteure aus der Forschung oder engagierte Menschen aus dem öffentlichen Gesundheitswesen und weiteren Bereichen, die Exploration der vorhandenen Daten durch natürliche Sprache!

### Teammitglieder und Rollen

Unser Team besteht aus 4 Personen aus 3 Disziplinen:

-   Benedikt Weyer, Angewandte Informatik, verantwortlich für die Software Entwicklung und Architektur
-   Michael German, Informatik Technischer Systeme, verantwortlich für die Software Entwicklung
-   Jan Biedasiek, Informatik Technischer Systeme, verantwortlich für die Testing unser System
-   Yunus Sözeri, Wirtschaftsinformatik, verantwortlich für die für die Benutzeroberfläche und Dokumentation

### Design

Unser Hauptvorteil ist, dass die Benutzeroberfläche mit Datahub-Interface integriert ist, weil uns Benutzerfreundlichkeit im Herzen liegt. Außedem die Design ist sehr intuitiv und gut dokumentiert, damit auch Leute mit wenigen technischen Verständnis das Projekt auch installieren können.

Hinter den Kullisen sieht es anders aus.Wir haben für eine Container-basierte Software-Design entschieden. Die Verantwortlichkeiten werden durch Containern getrennt und mithilfe Schnittstellen verbunden. Das bietet uns eine sinvolle und intuitive Abstraktion, was auch die Entwicklung neuer Features oder die Verbesserung existierende Features vereinfacht.
Haupteingangspunkt ist die in Datahub eingebettete Benutzeroberfläche. Daraus werden Anfragen an das Programm weitergeleitet und die anderen werden Container kommen dann zum Einsatz. Beispielsweise werden die Daten der eigenen Container gehostet und die Schnitstelle wird zur unser KI-Programm freigestellt, womit die KI die gegebene Anfrage bewerten kann und dementsprechend auf die nötigen Daten zugreifen kann und wenn nötig sogar Aggregationen bzw. mathematische Operationen durchführen kann.

### Datenakquisition

Unser Daten kommen aus Datahub-Datasnack. Datahub wird als Open-Source-Anwendung zur Verfügung gestellt. Wir haben uns aus dem Datenkatalog auf die Ghana-Daten konzentriert. Einmal installiert kann die Daten auf dem lokalen Infrastruktur immer zum Service bereitgestellt werden.

### Installationsanleitung

Für die Installationsanleitung, können wir ganz stolz auf unser [Dokumentation](https://github.com/benedikt-weyer/datahub-ai/wiki/Documentation) verweisen.

### Auswertung

Die Anforderungen wurden ziemlich gut getroffen. Unser App basiert auf einen lokal gehosteten LLM. Die App wird in das Django App von Datahub eingebettet bzw. die ChatBot kann man mittels der Datahub Interface erreichen. Mehr dazu in der [Dokumentation](https://github.com/benedikt-weyer/datahub-ai/wiki/Documentation). Unser Repository wird unter MIT-Lizenz bereitgestellt. Unser Entwicklung basiert auf die lokale Verwendbarkeit der Daten, was nur einmalig bei der Einrichtung Internetverbindung anfordert.

### Bekannte Fehler

SQL Generation bei generischen anfragen

### Erweiterung und Ausblick

Kubernetes
Github Issues
AUth
User Sessions
Feedback
