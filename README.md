# FastAPI Boilerplate - psycopg2

## Configuración de entorno de desarrollo FastAPI

### Instalación de pip3

```shell
sudo apt install python3-pip
```

### Instalación de [pyenv](https://github.com/pyenv/pyenv) usando [pyenv-installer](https://github.com/pyenv/pyenv-installer)

```shell
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | zsh
```

### Instalación de virtualenv

```shell
pip3 install virtualenv
```

### Instalación de python 3.10.11 con pyenv

```shell
pyenv install <version_python>
pyenv install 3.10.11
```

### Cambiar entre versiones de python

> Establecer version en el directorio actual

```shell
pyenv local <version_python>
```

> Establecer version en el sistema

```shell
pyenv global <version_python>
```

> Establecer la version del sistema por defecto

```shell
pyenv global system
```

### Creación de entorno virtual con pyenv y virtualenv

```shell
pyenv virtualenv <version_python> <nombre_entorno>
pyenv virtualenv 3.10.11 fastapi-auth
```

> Activar el entorno virtual creado

```shell
pyenv activate <nombre_entorno>
```

> Desactivar el entorno virtual

```shell
pyenv deactivate
```

### Instalaciones FastAPI

> Instalación minimas para ejecutar la aplicación

```shell
pip3 install fastapi
pip3 install "uvicorn[standard]"
pip3 install sqlalchemy
pip3 install pydantic-settings
pip3 install psycopg2-binary
pip3 install "pydantic[email]"
pip3 install python-jose
pip3 install "passlib[bcrypt]"
pip3 install python-multipart
```

### Creación del archivo requirements.txt

```shell
pip3 freeze > requirements.txt
```
