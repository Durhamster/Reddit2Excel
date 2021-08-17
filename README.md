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

Obtain Developer Keys for reddit and Twitter.

### To Obtain a Reddit Developer Key

> If you do not have a Reddit account you must first sign up for one.

1. Go to Reddit Apps.
2. Select “script” as the type of app.
3. Name your app and give it a description.
4. Set-up the redirect uri to be http://localhost:8080.
The redirect URI will be used to get your refresh token.
5. Once you click on “create app”, you will get a box showing you your client_id and client_secrets.
6. In the folder containing this README file (*the main folder for this project*)
    - Open the .env file and enter the client id and secret like the following
 ```bash
client_id = "YourClientIDHere"
client_secret = "YourClientSecretHere"
user_agent = "YourAppNameHere"
```
7. Save the file.
