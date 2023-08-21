The Epsilion War [captcha solver](http://t.me/epsa_captcha_bot).
========
[![tests](https://github.com/esemi/epsa-captcha-bot/actions/workflows/tests.yml/badge.svg?branch=master)](https://github.com/esemi/epsa-captcha-bot/actions/workflows/tests.yml)
[![linters](https://github.com/esemi/epsa-captcha-bot/actions/workflows/linters.yml/badge.svg?branch=master)](https://github.com/esemi/epsa-captcha-bot/actions/workflows/linters.yml)

The bot is designed to fast solve in-game captchas in [the Epsilion War MMORPG](https://t.me/epsilionwarbot?start=ref-537453818)

### Local setup
```shell
$ git clone git@github.com:esemi/epsa-captcha-bot.git
$ cd epsa-captcha-bot
$ python3.11 -m venv venv
$ source venv/bin/activate
$ pip install -U poetry
$ poetry install
```

### Run tests
```bash
$ pytest --cov=app
```

### Run linters
```bash
$ poetry run mypy app/
$ poetry run flake8 app/
```

### Run Telegram bot
```bash
python -m app.bot
```
