import os
from os import environ
from time import sleep, time
from datetime import datetime
import sys
import praw
import pandas as pd
from tqdm import tqdm


# --- Functions go here ---

#Converts seconds at the end to show how long the scrapeing process took.
def convert_time(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%d:%02d:%02d" % (hour, minutes, seconds)

#Load a text file as a list.
def load(file):
    try:
        with open(file) as in_file:
            loaded_txt = in_file.read().strip().split("\n")
            loaded_txt = [x.lower() for x in loaded_txt]
            return loaded_txt
    except IOError as e:
        print(
            "{}\nError opening {}.".format(e, file),
            file=sys.stderr,
        )
        sys.exit(1)

# returns dates in a readable format
def get_date(created):
    return datetime.fromtimestamp(created)

# searches by keyword
def keysearch(keyword):
    for submission in allsubs.search(
        keyword, sort="top", syntax="lucene", time_filter=datatime, limit=30
    ):
        reddit_dict["title"].append(submission.title)
        reddit_dict["subreddit"].append(submission.subreddit)
        reddit_dict["keyword"].append(str(keyword))
        reddit_dict["score"].append(submission.score)
        reddit_dict["comments"].append(submission.num_comments)
        reddit_dict["post url"].append("https://www.reddit.com/" + str(submission.id))
        reddit_dict["url"].append(submission.url)
        reddit_dict["created"].append(submission.created)
        reddit_dict["engagement"].append(submission.score + submission.num_comments)
        reddit_dict["code"].append(" ")
    sleep(2)

# formats spreadsheet
def formatsheet(df):
    # Setup writer and options
    writer = pd.ExcelWriter(
        reddit_file, engine="xlsxwriter", options={"strings_to_urls": False}
    )
    df.to_excel(writer, sheet_name=file_name, encoding="utf-8", index=False)
    workbook = writer.book
    worksheet = writer.sheets[file_name]
    worksheet.freeze_panes(1, 0)
    worksheet.autofilter("A1:J1")

    # Formats
    top_row = workbook.add_format(
        {"bg_color": "black", "font_color": "white"}
    )  # sets the top row colors
    num_format = workbook.add_format({"num_format": "#,##0"})

    # Sets the worksheet to the proper formats and column widths
    worksheet.set_column("A:A", 53.5)
    worksheet.set_column("B:B", 20)
    worksheet.set_column("C:C", 17.5)
    worksheet.set_column("D:D", 10, num_format)
    worksheet.set_column("E:E", 16, num_format)
    worksheet.set_column("F:F", 16)
    worksheet.set_column("G:G", 16)
    worksheet.set_column("H:H", 18)
    worksheet.set_column("I:I", 16, num_format)
    worksheet.set_column("J:J", 18)

    # Sets the top row/header font and color
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, top_row)

    writer.save()

# Fetching the keywords we will be searching and subreddits we want filtered
keywords = load("Keywords&Lists/reddit_keywords.txt")
filtered_subreddits = load("Keywords&Lists/filtered_subreddits.txt")

# Excel file name
file_name = input(
    "\nPlease enter what you want the file to be called. (Do not include .xlsx):\n"
)

while "." in file_name:
    file_name = input(
        "\nPlease enter what you want the file to be called. (Do not include .xlsx):\n"
    )
    if "." not in file_name:
        continue

reddit_file = f"{os.getcwd()}/ScrapedData/{file_name}.xlsx"

# Determines timeframe user wants to grab data (day, week, month, or year)
reddit_time = " "
while reddit_time not in (range(1, 6)):
    reddit_time = int(
        input(
            "How far back to do you want to fetch data for?:\n 1) Day\n 2) Week\n 3) Month\n 4) Year\n 5) All Time\n"
        )
    )
    if reddit_time in (range(1, 6)):
        # Counts how long script takes
        start_time = time()
        continue

time_list = ["day", "week", "month", "year", "all"]
datatime = time_list[reddit_time - 1]

if datatime != "all":
    print(
        f"Scraping the past {datatime} on reddit for {(len(keywords))} keywords and phrases...\n"
    )
else:
    print(
        f"Scraping for all time on reddit for {(len(keywords))} keywords and phrases...\n"
    )

# Gets API information
client_id = environ.get("client_id")
client_secret = environ.get("client_secret")
user_agent = environ.get("user_agent")

# API Information
reddit = praw.Reddit(
    client_id=client_id, client_secret=client_secret, user_agent=user_agent
)

# All subreddits Subreddits
allsubs = reddit.subreddit("all")

# Dict to put all our data
reddit_dict = {
    "title": [],
    "subreddit": [],
    "keyword": [],
    "score": [],
    "comments": [],
    "post url": [],
    "url": [],
    "created": [],
    "engagement": [],
    "code": [],
}

# Searches all the keywords and displays TQDM progress bar
with tqdm(total=len(keywords), file=sys.stdout) as pbar:
    for i in range(1):
        for terms in keywords:
            keysearch(terms)
            pbar.update(1)

# Creates DataFrame
df = pd.DataFrame(reddit_dict)
df["created"] = df["created"].apply(get_date)

# Drop all rows with the list of filtered subreddits
for filtered_subreddit in filtered_subreddits:
    df.drop(df[df["subreddit"] == filtered_subreddit].index, inplace=True)

# Drop all rows with less than 50 engagment
print("Cleaning the data...\n")
df.drop(df[df["engagement"] <= 50].index, inplace=True)
df.drop_duplicates(subset=["post url"], keep="first", inplace=True)
sorted_df = df.sort_values(by=["engagement"], ascending=False)

formatsheet(sorted_df)
print("Job completed in", convert_time(round(time() - start_time, 2)))
print(f"Data saved to {reddit_file}\n")

# Asks user if they want to open the cleaned file
opensheet = input("Do you want to open the excel file? (y or n): \n").lower()

if opensheet == "y":
    os.startfile(f"{reddit_file}")
else:
    pass
