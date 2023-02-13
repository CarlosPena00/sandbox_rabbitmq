# My Rabbitmq Sandbox

```sh
mamba env create
mamba activate rabbitmq
pip-sync requirements-dev.txt
pre-commit install

# After update `setup.cfg`
pip-compile setup.cfg --resolver backtracking -o requirements.txt
pip-compile setup.cfg --resolver backtracking -o requirements-dev.txt --extra dev
```

## Run
```sh
# start docker:
sh scripts/00_start.sh
```

## RabbitMQ
```
User: guest
Password: quest
Url: http://localhost:15672/
```
