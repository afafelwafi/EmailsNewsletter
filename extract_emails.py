import json
from nylas import APIClient
import re
from bs4 import BeautifulSoup
import pandas as pd

whitelist = ["dan@tldrnewsletter.com", "towardsai@substack.com", "news@alphasignal.ai"]
nylas_querry = " OR ".join([f"from:{mail}" for mail in whitelist])
f = open("config.json")
nylas_config = json.load(f)

nylas = APIClient(
    nylas_config["CLIENT_ID"],
    nylas_config["CLIENT_SECRET"],
    nylas_config["ACCESS_TOKEN"],
)


def parse_message(message: dict) -> str:
    return BeautifulSoup(message.body, features="html.parser").body.get_text()


def clean_content(text):
    # remove new line/space/'
    cleaned_text = (
        text.replace("\n", " ")
        .replace("\t", " ")
        .replace('"', "'")
        .replace("_", "")
        .replace("|", " ")
    )
    # Remove non-breaking space characters
    cleaned_text = re.sub(" +", " ", cleaned_text)
    # Remove special characters (e.g., emojis)
    cleaned_text = re.sub(r"[^\x00-\x7F]+", "", cleaned_text)
    # Remove URLs
    cleaned_text = re.sub(r"http\S+", "", cleaned_text)
    # Remove email addresses
    cleaned_text = re.sub(r"\S+@\S+", "", cleaned_text)
    # Remove leading and trailing whitespace
    cleaned_text = cleaned_text.strip(" ")
    return cleaned_text


def remove_footer(text):
    text = ". ".join(text.split(". ")[:-3])
    return text


def format_csv(meassages, corpus):
    text_dict = []
    for i, text in enumerate(corpus):
        text_dict.append(
            {
                "received_at": meassages[i].received_at,
                "from": messages[i].from_[0]["name"],
                "text": text,
            }
        )
    return pd.DataFrame(text_dict)


if __name__ == "__main__":
    # Read your inbox and display the results
    messages = nylas.messages.search(nylas_querry)
    bodies = list(map(parse_message, messages))
    corpus = list(map(clean_content, bodies))
    corpus = list(map(remove_footer, corpus))
    corpus_df = format_csv(messages, corpus)
    corpus_df.to_csv("newsletters_corpus.csv", index=False)
