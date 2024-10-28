# DataHub ChatBot LLM

This is a combination of a [Data Hub](https://github.com/datasnack/datahub) instance and a Chat-Bot powered by an LLM for interaction.

The Data Hub is a geographic information system (GIS) featuring a data fusion engine designed for data harmonization, alongside an interactive dashboard for effective data exploration and collaboration. Its key objective is to merge data of multiple formats and sources across temporal and spatial axes, allowing users to combine, analyze, and interpret the data.


## Installation

We do not yet provide a ready to use Docker image of the Data Hub, so for now you need to first build the base image yourself. For this first step follow these instructions:

- Clone the [Data Hub repository](https://github.com/datasnack/datahub) to your computer: `$ git clone https://github.com/yunussozeri/dh-chatbot-llm.git`
- Inside this folder build the Docker container with `$ docker build -t datahub:latest .`


No we can clone the Ghana Hub instance (this repository) into a new folder:

- Clone the repository `$ git clone https://github.com/datasnack/datahub.git`
- Copy the `.env.example` to `.env`: `$ cp .env.example .env`
- Open the `.env` file and make sure the following variables are set `SECRET_KEY`, `DATAHUB_NAME` (instructions are inside the `.env` file)
- Run `$ docker compose up -d`
- Wait/check until [http://localhost:8000/](http://localhost:8000/) shows the Data Hub interface

After this you can start/stop the system with:

    $ docker compose start
    $ docker compose stop

If you change the `.env` file run the following command to apply the changes:

    $ docker compose up -d

Now either import an existing data dump, or create a new instance.

### Ollama Setup

To download the required model run: `$ docker compose exec ollama ollama pull dolphin-llama3:latest`

### Import Data

We provide ready-to-use database export for Ghana that you can use to directly see and use the system without the need to download and process the raw data on your local machine.

Go to the [releases](https://github.com/datasnack/dh-ghana/releases) page and download the latest `*.dump` file and place it in the `./data/` folder.

Run the following command from the root of the repository:

    $ docker compose exec datahub python manage.py restore ./data/<downloaded *.dump file>


### Create Super-User

Run the following command to create a new user with which you can log in into the backend ([http://localhost:8000/admin](http://localhost:8000/)):

    $ docker compose exec datahub python manage.py createsuperuser


### Create dump

In case you need to export the data use: `$ docker compose exec datahub python manage.py dump`. An export file will be created in the `./data/` directory.


## Customization

Create custom app to add new functionality and/or overload templates (i.e., start page).

    mkdir ./src/<name>
    docker compose exec datahub python manage.py startapp <name> ./src/<name>

Then add it in the `.env` to the key `INSTALLED_USER_APPS` (comma separated list) like `src.<name>`.

Finally, inside the created app in `src/<name>/apps.py` change `name = <name>` to `name = src.<name>`.

After that you need to rebuild/start the container with `docker compose up -d`.
