import requests
from bs4 import BeautifulSoup
import lxml


def get_free_proxy():
    links = []
    result_list = []
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
        "accept": "* / *",
    }

    for offset in range(0, 9216, 64):
        link = f"https://hidemy.name/en/proxy-list/?start={offset}"
        links.append(link)

    try:
        for link in links:
            html = requests.get(url=link, headers=headers)
            soup = BeautifulSoup(html.text, "lxml")
            ip = soup.find("tbody").find_all("tr")
            port = soup.find("tbody").find_all("tr")
            for i, p in zip(ip, port):
                result_list.append(
                    f"{i.find_all('td')[0].text}:{p.find_all('td')[1].text} \n"
                )
    except Exception as _ex:
        print(_ex)
        return False

    with open("proxy_list.txt", "w", encoding="utf-8") as file:
        for proxy in result_list:
            file.write(proxy)
        return True
