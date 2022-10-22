import instaloader


def post_downloader(url: str):
    try:
        # need ig account
        with open("auth_ig.txt", "r") as file:
            login = file.readline().strip()
            password = file.readline().strip()
        shortlink = url.lstrip("https://www.instagram.com/p/").rstrip("/")
        L = instaloader.Instaloader()
        L.login(login, password)
        post = instaloader.Post.from_shortcode(L.context, shortlink)
        L.download_post(post, target="temp_ig")
        return True
    except:
        return False


def profile_pic_downloader(username: str):
    try:
        L = instaloader.Instaloader()
        L.download_profile(username, profile_pic_only=True)
        # default path /USERNAME/
        return True
    except:
        return False


def profile_photos_downloader(username: str):
    try:
        L = instaloader.Instaloader()
        L.download_profile(username)
        # default path /USERNAME/
        return True
    except:
        return False


def hashtag_downloader(hashtag: str):
    # take a while time
    L = instaloader.Instaloader()
    for post in instaloader.Hashtag.from_name(L.context, hashtag).get_posts():
        L.download_post(post, target=f"#{hashtag}")
