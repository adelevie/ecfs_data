# FCC ECFS Data

Using Python to fetch (and one day analyze) data from the FCC's Electronic Comment Filing Service.

## Dependencies

You can run this code either with a Docker setup, or with a native setup. Either way, you'll need an API key from data.gov.

### Docker setup

- Docker
- docker-compose

Set up API key:

```sh
cp .env.example
```

Add your data.gov API key to `DATA_API_KEY`.

Build the container:

```sh
docker-compose build
```

Run tests:

```sh
docker-compose run test
```

Run `main.py`:

```sh

docker-compose run main
```

### Native setup

- Python 3
- pip

Set your data.gov API key to the environment variable `DATA_API_KEY`.

Setup:

```sh
pip install -r requirements.txt
```

Run tests:

```sh
pytest
```

Run `main.py`:

```sh
python main.py
```
