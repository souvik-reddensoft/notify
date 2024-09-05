# Core Python

Steps needs to follow for Development environment:

1. Open docker file uncomment line 16 and change {PORT_NUMBER}

2. cp .env.example .env && chmod 664 .env

3. Open .env file and change {MONGO_CONNECTION_URI}, {MONGO_USER}, {MONGO_PASSWORD}, {SERVICE_MODULE_CODE} (As per your service)

4. [ * ] docker build . -t notify-img

5. [ ** ] docker run -p 5006:5006 -v $(pwd):/usr/src/app --name notify -d notify-img

6. [ *** ] docker logs -f notify 


# Run any Python file in docker as interactive mode (Ensure the container is running before executing any Python file)
1. [ ** ] docker exec -it <CONTAINER_ID> python <FILE_NAME.py>

Happy Coding :)