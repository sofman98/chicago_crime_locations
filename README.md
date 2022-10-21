# Chicago crime locations display
Display of the location of crimes that happened in Chicago in a map. The number of crimes is limited to a maximum of 100 for practical purposes.
## How to run the code
You need Docker and Docker-compose installed on your machine.
Copy your Google Cloud credentials file into ```server```, then on ```docker-compose.yml``` update ```services.environment.GOOGLE_APPLICATION_CREDENTIALS``` to the path to your file.

Build the Docker containers for the API and Dashboard using Docker-compose with the command:

```
$docker compose build
```

Run the docker containers (in the background with the ```-d``` argument) with the command:
```
$docker compose up -d
```

You can now access the dashboard on your local machine on ```http://localhost:8501/```.
You can also directly interact with the API on ```http://localhost:80/```.

Terminate the Docker containers with the command:
```
$docker compose down
```

It is possible that you may need to add ```sudo``` at the beginning of each command.