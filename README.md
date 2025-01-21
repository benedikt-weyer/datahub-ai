### Zielsetzung

Unser Ziel ist mithilfe des Einsatzes von KI die Datenbereitstellung im Bereich Public Health zu verbessern. Speziell fokussieren wir uns hier auf das Datahub. Unsere Lösung ist ein ChatBot, welcher die Exploration und Abfragen von Daten aus dem DataHub vereinfacht. Durch die Anwendung von KI ermöglichen wir nicht-technischen Fachleuten, wie Akteuren aus der Forschung oder engagierten Menschen aus dem öffentlichen Gesundheitswesen, die Exploration der vorhandenen Daten durch natürliche Sprache!

### Teammitglieder und Rollen

Unser Team besteht aus 4 Personen aus 3 Disziplinen:

-   Benedikt Weyer, Angewandte Informatik, verantwortlich für die Software Entwicklung und Architektur
-   Michael German, Informatik Technischer Systeme, verantwortlich für die Software Entwicklung
-   Jan Biedasiek, Informatik Technischer Systeme, verantwortlich für das Testen unserer Systeme
-   Yunus Sözeri, Wirtschaftsinformatik, verantwortlich für die Benutzeroberfläche und Dokumentation

### Design

Unser Hauptvorteil ist, dass die Benutzeroberfläche mit Datahub-Interface integriert ist, weil uns Benutzerfreundlichkeit am Herzen liegt. Außerdem ist das Design sehr intuitiv und gut dokumentiert, damit auch Leute mit wenig technischem Verständnis das Projekt installieren können.

Hinter den Kulissen sieht es anders aus. Wir haben uns für ein containerbasiertes Software-Design entschieden. Die Verantwortlichkeiten werden durch Container getrennt und mithilfe von Schnittstellen verbunden. Das bietet uns eine sinnvolle und intuitive Abstraktion, was auch die Entwicklung neuer Features oder die Verbesserung existierender Features vereinfacht.

Haupteingangspunkt ist die in Datahub eingebettete Benutzeroberfläche. Daraus werden Anfragen an das Programm weitergeleitet und die anderen Container kommen dann zum Einsatz. Beispielsweise werden die Daten der eigenen Container gehostet und die Schnittstelle wird unserem KI-Programm bereitgestellt, womit die KI die gegebene Anfrage bewerten kann und dementsprechend auf die nötigen Daten zugreifen kann und wenn nötig sogar Aggregationen bzw. mathematische Operationen durchführen kann.

### Datenakquisition

Unsere Daten kommen aus Datahub-Datasnack. Datahub wird als Open-Source-Anwendung zur Verfügung gestellt. Wir haben uns aus dem Datenkatalog auf die Ghana-Daten konzentriert.

### Installationsanleitung

Für die Installationsanleitung, verweisen wir gerne auf unser [Dokumentation](https://github.com/benedikt-weyer/datahub-ai/wiki/Documentation).

### Auswertung

Die Anforderungen wurden gut getroffen. Unser App basiert auf einen lokal gehosteten LLM. Die App wird in das Django App von Datahub eingebettet bzw. die ChatBot kann man mittels der Datahub Interface erreichen. Mehr dazu in der [Dokumentation](https://github.com/benedikt-weyer/datahub-ai/wiki/Documentation). Unser Repository wird unter MIT-Lizenz bereitgestellt. Unser Entwicklung basiert auf die lokale Verwendbarkeit der Daten, was nur einmalig bei der Einrichtung Internetverbindung anfordert.

### Bekannte Fehler

Wenn etwas schief gehen kann, wird es auch schief gehen. In unserem Fall können wir derzeit nicht verhindern, dass der LLM versucht, generische Fragen durch SQL-Abfragen zu beantworten.
Das macht uns einige Dinge schwer, nämlich die natürlichere, menschenähnliche Interaktion mit dem Bot und vielleicht die Robustheit gegenüber Anfragen, die Fehler enthalten

### Erweiterung und Ausblick

In Zukunft möchten wir unser Produkt in Kubernetes einsetzen können. Das hat bis zu einem gewissen Grad funktioniert, aber es sind noch einige Konfigurationen für die Infrastruktur und das Ressourcenmanagement erforderlich. Andererseits müssen wir die Abfragen immer mit zusätzlichen Informationen anreichern, um die Abfrageleistung und -qualität zu erhöhen. Wir arbeiten derzeit an einer flexibleren Möglichkeit, dies zu tun.
Optimalerweise würden wir eine Benutzerauthentifizierung und eine Benutzersitzungsfunktion einführen, um die persönliche Nutzung zu verbessern. Obwohl das Produkt für die lokale Nutzung konzipiert ist, würde ein Benutzer über eine Kontextsensitivität verfügen, die die kurzfristige Qualität drastisch verbessern würde.
Darüber hinaus würden wir gerne eine Art Feedback-Mechanismus für das Modell einführen, der im laufenden Betrieb arbeitet und das LLM langfristig verbessert, so dass sich die Qualität über die Zeit der Nutzung selbst verbessert.
