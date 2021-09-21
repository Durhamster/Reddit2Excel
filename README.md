# Reddit2Excel

# ![Reddit](https://img.shields.io/badge/Reddit-FF4500?style=for-the-badge&logo=reddit&logoColor=white) ➡️ ![Microsoft Excel](https://img.shields.io/badge/Microsoft_Excel-217346?style=for-the-badge&logo=microsoft-excel&logoColor=white)

![Python Version](https://img.shields.io/pypi/pyversions/praw?style=for-the-badge)
![License](https://img.shields.io/github/license/Durhamster/Reddit2Excel?style=for-the-badge)

A simple tool to scrape a list of keywords from Reddit into a neatly formatted .xlsx file.

# Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required libraries.

```bash
pip install -r requirements.txt
```

Obtain Developer Keys for Reddit.

# Obtaining a Reddit Developer Key

> If you do not have a Reddit account you must first sign up for one.

1. Go to Reddit Apps.
2. Select “script” as the type of app.
3. Name your app and give it a description.
4. Set-up the redirect uri to be http://localhost:8080.
   The redirect URI will be used to get your refresh token.
5. Once you click on “create app”, you will get a box showing you your client_id and client_secrets.
6. In the folder containing this README file (_the main folder for this project_)
   - Open the .env file and enter the client id and secret like the following

```bash
client_id = "YourClientIDHere"
client_secret = "YourClientSecretHere"
user_agent = "YourAppNameHere"
```

7. Save the file.

# Search Keywords & Phrases

## Adding/Removing Keywords & Phrases

To change the list of phrases and keywords, open the keywords.txt file under the Keywords&Lists directory.

Keywords and phrases must be similar like this:

```bash
This is an example phrase
KeywordExample
YouGetTheIdea
```
## Changing the Number of Posts Scraped

By default this script will scrape the top 100 posts for each keyword or phrase for the chosen time period.
To adjust this you can adjust the limit under the keysearch function.

```bash
def keysearch(keyword):
    for submission in allsubs.search(
        keyword, sort="top", syntax="lucene", time_filter=data_time, limit=100):
```
Doing so may result in hitting the API request limit. The maximum allowed is 1000, which can be achieved by setting limit to <i>none</i>.

More information on this can be found in the [praw api docs](https://praw.readthedocs.io/en/v7.4.0/getting_started/quick_start.html?highlight=request%20limit).

# Filtering Subreddits

You can filter out results from specific subreddits by opening the filtered_subreddits.txt file under the Keywords&Lists directory.

List the undesired subreddits like this:

```bash
exampleSubreddit
UGetTheIdea
IhOpe
```
