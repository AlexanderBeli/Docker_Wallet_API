
## First steps

Let's watch how to start application development, based on this template. First, we need to get the [Docker]('https://www.docker.com/get-started/').


Second, we need to get the sources:

```shell
$ git clone https://github.com/AlexanderBeli/Docker_Wallet_API.git
$ cd ./Docker_Wallet_API
```
Then we need to launch it:

```shell
$ docker-compose up -d --build
```

Create the superuser

```shell
$ docker-compose exec web python3 manage.py createsuperuser
```

Open the browser and open the localhost:

```shell
http://localhost:8000/api/v1/
```

Here you can add some data 

Also you can install httpie, open bash and play with API, for example:
```shell
$ http POST http://127.0.0.1:8000/api/v1/<YOUR_DATA_UUID>/operation/ operationType='WITHDRAW' amount=300
```


## License

This project is open-sourced software licensed under the [MIT license](https://opensource.org/licenses/MIT).

