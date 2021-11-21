# ku-polls

[![Django CI](https://github.com/sirateek/ku-polls/actions/workflows/django.yml/badge.svg)](https://github.com/sirateek/ku-polls/actions/workflows/django.yml)
[![codecov](https://codecov.io/gh/sirateek/ku-polls/branch/master/graph/badge.svg?token=1YYGRMFOA3)](https://codecov.io/gh/sirateek/ku-polls)

The online polls web application that have flexibility on open and close the poll's question. Also, User can view the polls result anytime in form of pie chart.

## 📦 Installation

```bash
$ git clone https://github.com/sirateek/ku-polls.git
$ pip3 install -r requirements.txt
$ python3 manage.py runserver
```

Note: If you just clone this repository and run the command as above. You are likely to run the django on the production mode which is **NOT recommended** for the one who want to serve it without a proper web server. See also [#12](https://github.com/sirateek/ku-polls/issues/12#issuecomment-922686620).

TLDR: I recommend for the one who want to serve it locally to also set the `DEBUG=True` in the env config file as in the [instruction below](#-Configuration).

## 🔧 Configuration

I have used the package `django-environ` to externalize the sensitive config of Django.

The env config file containing the Django config parameters for this app must be located in this directory `config/.env`

You can set the 3 parameters for the Django. _Every keys are optional, They all have the default value._

```env
# The Django Secret Key.
# Type: string | Default: 'missing-secret-key'
SECRET_KEY=some_key

# The host that allow to connect to the Django.
# Type: list | Default: ["127.0.0.1", "localhost"]
ALLOWED_HOSTS=localhost

# The debug mode of the Django.
# Type: bool | Default: False
DEBUG=True
```

### Defaut user you can use:

| Username | Password |
| -------- | -------- |
| demo1    | Vote4me! |
| demo2    | Vote4me2 |

## Project Information

- [Wiki Home](../../wiki/Home)
- [Vision Statement](../../wiki/Vision%20Statement)
- [Requirement](../../wiki/Requirements)
- [Iteration 1 Plain](../../wiki/Iteration%201)
- [Iteration 2 Plain](../../wiki/Iteration%202)
- [Iteration 3 Plain](../../wiki/Iteration%203)
