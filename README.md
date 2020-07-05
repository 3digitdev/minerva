# Minerva

_A self-hosted personal database_

The name is derived from the Roman goddess of wisdom.

## What is this

Minerva is a WIP "personal database" designed to track all kinds of things in your life for you.

It is intended to be self-hosted, since much of the information stored will be private.
Access is provided via API keys to the API serving up the data, and the data can be stored in
a number of various DBs (initially supporting **MongoDB**).

Interfacing with the data will be done via various UIs (mobile, webapp, TUI, etc.)

The entire system has tagging enabled, which allows for powerful filters of information quickly.

The system is based on a set of "categories" of object/relational information.

## Categories

- **Notes**:  Generic text notes to keep
- **Dates**:  Important dates.  Could be anniversaries, or birthdays, or just days to remember.  Typically meant for _past_ dates -- not intended to be used as a scheduler.
- **Passwords**:  Self explanatory.  Planned to also include security questions.
  - **Due to the sensitivity of such information, it is recommended that you review the security and take precautions.**
- **Employment History**:  Information about past employers -- dates, titles, contact info, etc.
- **Housing History**:  Similar to ^^^, but for apartments/houses.
- **Recipes**:  Recipes grouped by type, with ingredients, instructions, and links
- **Links**:  Generic links.  Basically just bookmarked sites.

## Why do this?

While none of this is groundbreaking, I felt that in order to do all of this I would need to share this (sometimes very personal) information with other webapps and sites that I may or may not trust with it.

As a result, I wanted to make a dirt-simple self-hosted version.  The intention for this is **not** to be some omni-replacement for things like 1Password, Notion.so, Basecamp, or other things.  I intend this to be merely **self-hosted storage and search**, so that any number of extensions can be built on it.

Interfaces, app integrations (browser extensions etc.), and other things can (and probably will) be added, but don't need to be in order to get started with this.

## Security Notes

- **It is expected that any frontend encrypts sensitive data before sending via API.**  The backend does **zero** encryption -- it is merely a storage mechanism.
- **You will need to create an API Key for your frontend (app, script, or otherwise).**  It is recommended that you make a different one for each consumer of the API.
  - This API key will need to be added to the DB yourself.  Instructions will be in the **Installation** section.

## Installation

**TODO**

## TODO

- Add pagination query params to "get all" endpoints
- Code cleanup + comments (docstrings, etc)
- Figure out how to build Mongo so it adds indices automatically on creation
  - Commands:
    - `db.tags.createIndex({"name": 1}, {unique: true})`
    - `db.access_logs.createIndex({"created_at": 1}, {expireAfterSeconds: 604800})`
  - Needed for Docker image eventually