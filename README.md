# Gladitek

The best tool to not forget about your Epitech's events!

Using Intranet's API, it syncs every single event your have registered to (or are assigned to, hello dear AER and Astek :wave:) to your Google Calendar.

Are you a student *and* part of the pedagogical team? Well, first, you're a boss! You are in the right place, this tool lets you configure multiple calendar using multiple Epitech accounts!

It manages multiple events from the same activity, avoid duplicates and can be used with a daemon like cron, systemd, and launchd

## Installation

Clone this repository, and at its path to your `PATH` environment variable
Install the Google Calendar API Module:

```bash
pip install gcsa python-dateutil
```

## Setup Gladitek

First of all, you'll need python3, an Epitech Intranet Access, and a Google Account

We recommend to dedicate one Google Calendar per Intra Calendar

Then, in a folder that well call `$GLADIR`, we'll put some configuration files

- A 'credentials.json' file:

    To get it, you'll have to:

  - Go [there](https://console.cloud.google.com/home/dashboard) and create a project that will be dedicated to Gladitek
  - If it is not already, select the newly created project and go to `API & Services`.
  - Enable the `Google Calendar API` service
  - Configure OAuth consent screen (Don't spend too much time on it, only you will see that page)
  - Go to `Credentials`. Click `Create Credentials` -> `OAuth Client ID`. Select `Desktop App`. you can now download a JSON file. Put it in your $GLADIR, and name it `credentials.json`
  - Add your google account to authorized testers: (`OAuth Consent Screen` -> `Test users`)
  
- A 'gladitek.json' configuration file.

  Take a look at the provided `gladitek.example.json`. For each calendar to set up, do the following:

  - Set the 'calendar_id' key to the Google Calendar's ID (`My Calendars` -> `Settings and sharing` -> `Integrate calendar` -> `Calendar ID`)
  - Set the 'autologin' field with the Intra's autologin link (`Intranet` -> `Administration` -> `Generate autologin` -> What's after `auth-`)
  - Set the 'token_path' field with a name of the token to generate on first launch. It **must** be unique
  - Set the 'pedago' field with with a boolean: `true` if you are part of the pedagogical team, `false`otherwise

## Usage

To sync your calendars with events starting from today:

```bash
gladitek --gladir $GLADIR
```

To sync your calendars with events before and from today:

```bash
gladitek --gladir $GLADIR --full
```

**Warning**: If you are a pedago, the use of this option should be minimied
Note: the first time, you will be ask to authenticate via OAuth2.

To clear your calendars:

```bash
gladitek --gladir $GLADIR --clear
```

**Warning** This will erase all events in the calendars. It might take some time

## Contributions

Issues and pull requests are welcome :smile:
