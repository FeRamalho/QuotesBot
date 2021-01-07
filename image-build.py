import configparser
from PIL import Image, ImageFont, ImageDraw 
import textwrap
import random
import os
import tweepy
import time
import logging

def main():
    # Authenticate to Twitter
    api = twitter_authentication()

    rand_img = get_random_image("/home/fernanda/Workspace/QuotesBot/images")
    my_image = Image.open(rand_img)

    test = "\"aqui está um texto com vários caracteres, queria dizer que isso é muito estranho, imagino que não seja tanto assim, thunder, ele repete muito essa palavra, não gosto de músicas que\""
    test = "\"I love woooo\""
    #test = "\"iraaaa isso é muuuito estranho, imagino que não\""

    margin = 611
    offset = 14

    if len(test) <= 100:
        offset = 212

    title_font = ImageFont.truetype('fonts/Roboto-Regular.ttf', 50)
    italic_font = ImageFont.truetype('fonts/Roboto-Italic.ttf', 50)

    image_editable = ImageDraw.Draw(my_image)

    text = "\n".join(textwrap.wrap(test, width=23))

    image_editable.text((margin, offset), text, (241, 19, 38), font=title_font)

    offset += (title_font.getsize(text)[1] * len(textwrap.wrap(test, width=23)))

    character = "-Supergirl"
    image_editable.text((margin, offset), character, (178, 30, 42), font=italic_font)

    my_image.save("result.png")

    since_id = check_mentions(api, 1)

    api.update_with_media("result.png")

def check_mentions(api, since_id):
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            continue
        api.update_status(
            status="@" + tweet.in_reply_to_screen_name + " olar",
            in_reply_to_status_id=tweet.id_str,
        )
    return new_since_id

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

def get_random_image(folder):
    media_list = []
    for dirpath, dirnames, files in os.walk(folder):
        for f in files:
            media_list.append(os.path.join(dirpath, f))
    media = random.choice(media_list)
    return media

if __name__ == "__main__":
    main()




#250 caracteres
#183 caracteres sem precisar mudar a fonte
#212 -> -100caracteres
#cortar a frase se tiver mais de 183 chars
#cor -> (245, 232, 230)