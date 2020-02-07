This is a simple Flask site used to test integrations using the [TransactID Python Library][1].

There are two options for running this.  You can use docker or you can run a local copy of Flask.

####Dock Instructions
Ensure that you have [Docker][2] installed.

1. run: `docker run --rm --name transactid-python -p 5000:5000 -d netkicorporate/transactid-python:latest`
2. stop: `docker stop transactid-python`

Once this is up and running you can access the endpoints using the base URL of http://localhost:5000/.  This URL
also has directions on how to use the different endpoints.


####Python Instructions
It is highly recommended that you create a virtual environment for this and the steps here will take that into account.

1. create a virtual environment using your manager of choice
2. activate the environment and run `pip install -r requirements.txt` from within the directory this repos was downloaded to.
3. export the FLASK_APP variable: `export FLASK_APP=echo.py`
4. run the built in Flask server: `flask run`

Once this is up and running you can access the endpoints using the base URL of http://localhost:5000/.  This URL
also has directions on how to use the different endpoints.

Included in this repo is a very basic [Postman][3] collection that you can import and use for testing. 

[1]: https://github.com/netkicorp/transactid-library-python
[2]: https://www.docker.com/
[3]: https://www.postman.com/
