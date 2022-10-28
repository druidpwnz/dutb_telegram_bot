import instaloader


# authorization disabled, because works incorrectly
def post_downloader(url: str):
    try:
        # need ig account
        # with open("auth_ig.txt", "r") as file:
        #     login = file.readline().strip()
        #     password = file.readline().strip()
        shortlink = url.lstrip("https://www.instagram.com/p/").rstrip("/")
        L = instaloader.Instaloader()
        # L.login(login, password)
        post = instaloader.Post.from_shortcode(L.context, shortlink)
        L.download_post(post, target="cache")
        return True
    except:
        return False


def profile_content_downloader(account_name: str):
    try:
        # with open("auth_ig.txt", "r") as file:
        #     login = file.readline().strip()
        #     password = file.readline().strip()
        L = instaloader.Instaloader()
        # L.login(login, password)
        L.download_profile(account_name)
        # default path /USERNAME/
        return True
    except:
        return False


def hashtag_downloader(hashtag: str):
    try:
        # with open("auth_ig.txt", "r") as file:
        #     login = file.readline().strip()
        #     password = file.readline().strip()
        L = instaloader.Instaloader()
        # L.login(login, password)
        counter = 0
        for post in instaloader.Hashtag.from_name(L.context, hashtag).get_posts():
            counter += 1
            L.download_post(post, target="cache")
            if counter == 10:
                break
        return True
    except:
        return False
