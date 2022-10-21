# TODO привязать парсеры через os: если после выполнения функции приходит тру - os ищет папку и передает ее контент в тг
# TODO попробовать забрать хештеги через промежутки времени
# from datetime import datetime
# from itertools import dropwhile, takewhile
import instaloader

def ig_post_downloader(postlink: str):
    try:
        shortlink = postlink.lstrip("https://www.instagram.com/p/").rstrip("/")
        L = instaloader.Instaloader()
        post = instaloader.Post.from_shortcode(L.context, shortlink)
        L.download_post(post, target=f"temp_{postlink}")
        return True
    except:
        return False


def ig_profilepic_downloader(username: str):
    try:
        L = instaloader.Instaloader()
        L.download_profile(username, profile_pic_only=True)
        # default path /USERNAME/
        return True
    except:
        return False


def ig_profile_photos_downloader(username: str):
    try:
        L = instaloader.Instaloader()
        L.download_profile(username)
        # default path /USERNAME/
        return True
    except:
        return False


def hashtag_downloader(hashtag: str):
    # take a while time
    # mb be work with timeperiods
    L = instaloader.Instaloader()
    for post in instaloader.Hashtag.from_name(L.context, hashtag).get_posts():
        L.download_post(post, target=f"#{hashtag}")


def get_comments(username: str):
    L = instaloader.Instaloader()
    posts = instaloader.Profile.from_username(L.context, username).get_posts()
    for post in posts:
        for comment in post.get_comments():
            print(f"comment id: {comment.id}")
            print(f"comment owner username: {comment.owner.username}")
            print(f"comment text: {comment.text}")
            print(f"comment time: {comment.created_at_utc}")
            print("************************************************")


# ig_post_downloader("https://www.instagram.com/p/CPv_JKhFJAX/")
# ig_profile_photos_downloader('kuzinwafel')
# get_comments('igor_nestorenko')
