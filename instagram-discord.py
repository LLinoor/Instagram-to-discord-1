import json
import requests
import os
import time
import datetime

os.environ["firstCheck"] = "True"
os.environ["WEBHOOK_URL"] = ""
users = [""]
os.environ["TIME_INTERVAL"] = "300"

def get_profile_picture(html):
    return html.json()["graphql"]["user"]["profile_pic_url_hd"]

def get_last_publication_url(html):
    return html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["shortcode"]

def isVideo(html, selector):
    mediaType = html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][selector]["node"]["is_video"]
    if(mediaType == True):
        mediaType = "video"
    else:
        mediaType = "pic"
    return(mediaType)

def get_embed(html, selector):
    embed = {}
    embed["color"] = 15077485
    embed["title"] = "@" + INSTAGRAM_USERNAME + " posted a new " + isVideo(html, selector)
    embed["url"] = "https://www.instagram.com/p/" + html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][selector]["node"]["shortcode"] +"/"
    try:
        embed["description"] = html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][selector]["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"]
    except:
        embed["description"] = ""
    embed["image"] = {"url": html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][selector]["node"]["thumbnail_src"]}
    embed["author"] = {"name":f"@{INSTAGRAM_USERNAME} (from Instagram)", "url":f"https://instagram.com/{INSTAGRAM_USERNAME}/", "icon_url":get_profile_picture(html)}
    dt_object = datetime.datetime.fromtimestamp(html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][selector]["node"]["taken_at_timestamp"])
    time = dt_object.strftime("%m/%d at %H:%M")
    embed["footer"] = {"text": "• " + time + " (UTC Time)", "icon_url": "https://i.imgur.com/TqD7E3m.png"}
    return embed

def webhook(webhook_url, html, selector):
    data = {}
    data["embeds"] = []
    data["embeds"].append(get_embed(html, selector))
    result = requests.post(webhook_url, data=json.dumps(
        data), headers={"Content-Type": "application/json"})
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Image successfully posted in Discord, code {}.".format(
            result.status_code))


def get_instagram_html(INSTAGRAM_USERNAME):
    headers = {
        "Host": "www.instagram.com",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
    }
    html = requests.get("https://www.instagram.com/" +
                        INSTAGRAM_USERNAME + "/channel/?__a=1", headers=headers)
    try:
        test_json = html.json()["graphql"]
    except:
        html = requests.get("https://www.instagram.com/" +
                        INSTAGRAM_USERNAME + "/feed/?__a=1", headers=headers)
        try:
            test_json = html.json()["graphql"]
        except:
            print("JSON Error")
    return html


def main():
    try:
        html = get_instagram_html(INSTAGRAM_USERNAME)
        if(os.environ["firstCheck"] == "True"):
            print("First check, skipping the post")
            os.environ[f"LAST_IMAGE_ID_{INSTAGRAM_USERNAME}"] = get_last_publication_url(html)
        elif(os.environ.get(f"LAST_IMAGE_ID_{INSTAGRAM_USERNAME}") == get_last_publication_url(html)):
            print("Not new image to post in discord.")
        else:
            print("New image to post in discord.")
            i = 0
            delete = True
            for id_post in html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]:
                id_post = id_post["node"]["shortcode"]
                if(delete == True):
                    if(id_post == os.environ[f"LAST_IMAGE_ID_{INSTAGRAM_USERNAME}"]):
                        delete = False
                    else:
                        delete = True
                else:
                    pass
            for post in html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]:
                post = post["node"]["shortcode"]
                if(post == os.environ[f"LAST_IMAGE_ID_{INSTAGRAM_USERNAME}"] or delete == True):
                    os.environ[f"LAST_IMAGE_ID_{INSTAGRAM_USERNAME}"] = get_last_publication_url(html)
                    return
                else:
                    webhook(os.environ.get("WEBHOOK_URL"), get_instagram_html(INSTAGRAM_USERNAME), i)
                    i = i + 1

    except Exception as e:
        print(e)


if __name__ == "__main__":
    if os.environ.get('WEBHOOK_URL') != None:
        while True:
            for user in users:
                INSTAGRAM_USERNAME = user
                main()
            if(os.environ["firstCheck"] == "True"):
                os.environ["firstCheck"] = "False"
            time.sleep(float(os.environ.get('TIME_INTERVAL') or 300))
    else:
        print('Please configure environment variables properly!')