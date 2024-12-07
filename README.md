# API BUGBURGER

## Configurar e instalar o projeto
1o passo
```sh
python -m venv .venv
```
2o passo
```sh
.venv/scripts/activate
```
> Windows
```sh
source .venv/bin/activate
```
> Linux

3o passo
```sh
pip install poetry
```
4o passo
```sh
poetry install
```

## Iniciar aplicação
```sh
fastapi dev
```

## Poetry Extras
### Exportar requirements
```sh
poetry export --without-hashes --format=requirements.txt > requirements.txt
```