# FakeArchitectureOrchestrator

L'obiettivo di questo progetto è creare facilmente un'infrastruttura "fake" partendo da un diagramma architetturale e istanziare un container Docker per ogni tipo di risorsa individuata attraverso la creazione di un "terraform plan" adeguato.

La soluzione proposta soddisfa tutte le specifiche di progetto richieste, consentendo all'utente di scegliere se fornire il diagramma architetturale tramite un opportuno file ".xml" o tramite un'immagine in formato ".png" o ".jpeg".

Il progetto è stato realizzato in **Python** utilizzando **PyCharm CE** come IDE. Inoltre, sono stati necessari strumenti aggiuntivi come **Docker**, **Terraform**, **YoloV5**, e **Roboflow** (questi ultimi necessari per il modello di rete neurale per analizzare i file immagine).

## Strumenti Utilizzati
- **Python**: Linguaggio di programmazione principale.
- **PyCharm CE**: Ambiente di sviluppo integrato.
- **Docker**: Piattaforma per lo sviluppo, la distribuzione e l'esecuzione di applicazioni in container.
- **Terraform**: Strumento per la creazione e la gestione dell'infrastruttura come codice.
- **YoloV5**: Framework per l'addestramento di reti neurali per l'analisi di immagini.
- **Roboflow**: Piattaforma per la gestione di dataset e modelli per l'elaborazione delle immagini.

## Modalità di Fornitura del Diagramma Architetturale
L'utente può fornire il diagramma architetturale tramite:
- Un file ".xml"
- Un'immagine in formato ".png" o ".jpeg"

## Istruzioni per l'Esecuzione
1. Clone il repository.
2. Seleziona il tipo di diagramma architetturale e fornisci il file corrispondente.
3. Esegui il "terraform plan" per istanziare l'infrastruttura.

Seguendo questi passaggi, l'infrastruttura "fake" sarà creata con successo.

Per ulteriori dettagli e istruzioni dettagliate, consulta la documentazione del progetto.
