# Gladitek

The best tool to not forget about your Epitech's events!

Using Intranet's API, it syncs every single event your have registered to (or assigned to, hello dear AER and Astek :wave:) to your Google Calendar.

Are you a student *and* part of the pedagogical team? Well, first, your a boss! You are in the right place, this tool lets you configure multiple calendar using multiple Epitech accounts!

## Installation

First, thanks to [navdeep-G](https://github.com/navdeep-G) for his [template setup.py](https://github.com/navdeep-G/setup.py)

To install Gladitek, simply run the following commands:

```bash
git clone https://github.com/Arthi-chaud/Gladitek Gladitek
cd Gladitek
python setup.py ##TODO not working
```

## Setup Gladitek

First of all, you'll need python3, an Epitech Intranet Access, and a Google Account

Then, in a folder that well call $GLADIR, we'll put some configuration files

- A 'credentials.json' file:

    To get it, you'll have to:

  - Go [there](https://console.cloud.google.com/home/dashboard) and create a project that will be dedicated to Gladitek
  - If it is not already, select the newly created project and go to `API & Services`.
  - Enable the `Google Calendar API` service
  - Configure OAuth consent screen (Don't spend too much time on it, only you will see that page)
  - Go to `Credentials`. Click `Create Credentials` -> `OAuth Client ID`. Select `Desktop App`. you can now download a JSON file. Put it in your $GLADIR, and name it `credentials.json`
  
- A 'gladitek.json' configuration file.

  Take a look at the provided `gladitek.example.json`. For each calendar to set up, do the following:

  - Set the 'calendar_id' key to the Google Calendar's ID (`My Calendars` -> `Settings and sharing` -> `Integrate calendar` -> `Calendar ID`)
  - Set the 'autologin' field with the Intra's autologin link (`Intranet` -> `Administration` -> `Generate autologin` -> What's after `auth-`)
  - Set the 'token_path' field with a name of the token to generate on first launch. It **must** be unique

## Usage

To sync your calendars:
```gladitek --gladir $GLADIR```

Note: the first time, you will be ask to authenticate vie OAuth2.

To re-dump your calendars:
```gladitek --gladir $GLADIR -redump```
