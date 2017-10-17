# Coffee, Tea, or Me?
A Telegram Bot for coffee runs.

`simple_kopi.py`: simple demo to learn how to work with python-telegram-bot library

`kopi.py`: a simple kopi orders bot

`advanced_kopi.py`: a full-fledged kopi orders bot. Future enhancements will focus solely on this file.

## Setting up your development environment
Install Homebrew by pasting the following in your terminal:
```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

To install pyenv, run the following commands in terminal:

1. `brew update`

2. `brew install pyenv`


After installation, add the following at the bottom of your profile (~/.bash_profile or ~/.zshrc).

```
if which pyenv > /dev/null; then eval "$(pyenv init -)"; fi
```

Restart your terminal, then install Python 3.6.3 by running `pyenv install 3.6.3`.

Once installed, run `pyenv global 3.6.3`.

Restart your terminal, then run `python --version`. You should see Python 3.6.3 show up in your terminal.

Create a project directory, e.g. `coffee-tea-or-me`.

In the project directory, run `pip install python-telegram-bot`.

In the project root folder, create a file called `config.json` with the following content:

```
{
    "bot_token": "<your telegram bot token here>"
}
```
Do not worry about the telegram bot token, I will go through how you can get it during the chapter day.
