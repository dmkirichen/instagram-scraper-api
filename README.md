# Instagram Scraper API

### Build

You can run and build this project on any system that has docker using:

```
docker-compose up --build
```

Finish work by pressing `Ctrl+C` and then running:
http://localhost:8000/posts

```
docker-compose down
```

### Run

Basically, you can control the process using 2 endpoints:

##### POST - http://localhost:8000/fetch-latest

This one will start the process of scraping instagram (which will take approximately 10-30 seconds). After that you can fetch last updated information using next endpoint.

##### GET - http://localhost:8000/posts

You can get scraped info using this endpoint
