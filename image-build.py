import configparser
from PIL import Image, ImageFont, ImageDraw 
import textwrap
import random
import os
import tweepy
import time
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def main():
    # Authenticate to Twitter
    api = twitter_authentication()

    since_id = check_mentions(api, 1)

    # api.update_with_media("result.png")

def check_mentions(api, since_id):
    logger.info("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            continue
        exclude_text = ['@' + tweet.in_reply_to_screen_name]
        text_tweet = [x for x in tweet.text.split() if x not in exclude_text]
        text_tweet = ' '.join(text_tweet)

        build_image(text_tweet)

        logger.info(f"Answering to {tweet.user.name}")
        api.update_with_media(
            filename= "result.png",
            in_reply_to_status_id=tweet.id,
            auto_populate_reply_metadata=True,
        )
    return new_since_id

def get_random_image(folder):
    media_list = []
    for dirpath, dirnames, files in os.walk(folder):
        for f in files:
            media_list.append(os.path.join(dirpath, f))
    media = random.choice(media_list)
    return media

def build_image(text):
    margin = 611
    offset = 14

    text = "\"" + text + "\""

    img_path = get_random_image("/home/fernanda/Workspace/QuotesBot/images")
    img_result = Image.open(img_path)

    if len(text) <= 100:
        offset = 212

    title_font = ImageFont.truetype('fonts/Roboto-Regular.ttf', 50)
    italic_font = ImageFont.truetype('fonts/Roboto-Italic.ttf', 50)

    draw_image = ImageDraw.Draw(img_result)

    text_image = "\n".join(textwrap.wrap(text, width=23))

    draw_image.text((margin, offset), text_image, (241, 19, 38), font=title_font)

    offset += (title_font.getsize(text_image)[1] * len(textwrap.wrap(text, width=23)))

    character_name = re.split('/|-', img_path)[-1]
    character_name = character_name.split('.')[0]
    character_name = '-' + character_name.replace('_', ' ')

    draw_image.text((margin, offset), character_name, (178, 30, 42), font=italic_font)

    img_result.save("result.png")

def twitter_authentication():
    config = configparser.ConfigParser()
    config.read('config.ini')
    twitter_config = config['TWITTER']
    api_key = twitter_config['api_key']
    api_secret = twitter_config['api_secret']
    oauth_token = twitter_config['oauth_token']
    oauth_token_secret = twitter_config['oauth_token_secret']
    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(oauth_token, oauth_token_secret)
    api = tweepy.API(auth)
    try:
        api.verify_credentials()
        print("Authentication OK")
        return api
    except:
        print("Error during authentication")

if __name__ == "__main__":
    main()




#250 caracteres
#183 caracteres sem precisar mudar a fonte
#212 -> -100caracteres
#cortar a frase se tiver mais de 183 chars
#cor -> (245, 232, 230)