# ku-polls
The online polls web application

## 📦 Installation
```bash
$ git clone https://github.com/sirateek/ku-polls.git
$ pip3 install -r requirement.txt
$ python3 manage.py runserver
```
Note: If you just clone this repository and run the command as above. You are likely to run the django on the production mode which is **NOT recommended** for the one who want to serve it without a proper web server. See also [#12](https://github.com/sirateek/ku-polls/issues/12#issuecomment-922686620).

TLDR: I recommend for the one who want to serve it locally to set the `DEBUG=true` in the env config file as in the [instruction below](#-Config).

## 🔧 Config
The config file containing the Django config parameters for KU Polls app must be located in this directory `config/.env`

You can set the 3 parameters for the Django. Every keys are optional, They all have the default value.
```env
# The Django Secret Key.
# Type: string | Default: 'missing-secret-key'
SECRET_KEY=some_key

# The host that allow to connect to the Django.
# Type: list | Default: ["127.0.0.1", "localhost"]
ALLOWED_HOSTS=localhost

# The debug mode of the Django.
# Type: bool | Default: false
DEBUG=true
```

## Project Information
- [Wiki Home](../../wiki/Home)
- [Vision Statement](../../wiki/Vision%20Statement)
- [Requirement](../../wiki/Requirements)
- [Iteration 1 Plain](../../wiki/Iteration%201)
- [Iteration 2 Plain](../../wiki/Iteration%202)
