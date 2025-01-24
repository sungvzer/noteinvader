# NoteInvader

## What is NoteInvader?

[NoteInvader](https://noteinvader.sungvzer.com) is a social music platform that allows users to search for and save their favorite albums, connect with each other, and _snoop_ a bit on their friends!

## Tech stack

- Frontend

  - HTML
  - CSS
  - JavaScript

- Backend

  - Linux
  - Nginx
  - Python / Flask
  - MongoDB

- CI/CD:

  - GitHub Actions
  - Oracle Cloud Services

- External APIs
  - Last.FM API [(site)](https://www.last.fm/api)

## Instructions

Follow these instructions to run this project locally.

### Prerequisites

- Python 3.9 or higher [(site)](https://www.python.org/downloads/)
- Docker [(site)](https://docs.docker.com/engine/install/)
- Docker Compose [(site)](https://docs.docker.com/compose/install/)
- Git [(site)](https://git-scm.com/downloads)

Clone the project to your computer.

```bash
$ git clone https://github.com/sungvzer/tecweb-project.git
$ cd tecweb-project
```

Copy the `.env.example` file to `.env` and fill in the required environment variables.

```bash
$ cp .env.example .env
```

The most important variable is LASTFM_API_KEY, create an account on the Last.FM website and get an API key [here](https://www.last.fm/api/authentication)

### Running in Docker

This project uses Docker and Docker Compose to run the services. To start the services, run the following command:

```bash
$ docker compose up -d --build
```

Open the browser and go to `http://localhost:8080` to see the application running.

### Running locally

Create a virtual environment.

```bash
$ python3 -m venv .venv
$ # POSIX (Linux, MacOS, etc.)
$ source .venv/bin/activate
$ # Windows
$ .\.venv\Scripts\Activate.ps1
```

Install the required dependencies:

```bash
$ pip install -r requirements.txt
```

Start the database:

```bash
$ docker compose up -d db
```

Run the application:

```bash
$ flask run
```

Open the browser and go to `http://localhost:5000` to see the application running.

## Dependencies

- Flask: the web framework used to create the application
- Flask-PyMongo: used to connect to the MongoDB database
- Flask-WTF: used to create forms
- Flask-Login: used to manage user sessions
- bcrypt: used to hash passwords
- requests: used to make HTTP requests to the Last.FM API
- python-dotenv: used to load environment variables from a `.env` file
- black: used to format the code
- email_validator: used to validate email addresses

## Authors

- Salvatore Gargano
  - GitHub: [@sungvzer](https://github.com/sungvzer)
  - UniParthenope: 0124002839 - [salvatore.gargano001@studenti.uniparthenope.it](mailto:salvatore.gargano001@studenti.uniparthenope.it)
  - NoteInvader: [gargsalv](https://noteinvader.sungvzer.com/user/gargsalv)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
