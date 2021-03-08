from bs4 import BeautifulSoup


def serialize_abstact(data):
    pages = data["query"]["pages"].values()
    pages_iterator = iter(pages)
    return next(pages_iterator)["extract"]


def serialize_info_box(data):
    dom = data["parse"]["text"]["*"]
    soup = BeautifulSoup(dom, "html.parser")
    headers = soup.find_all("th")

    all_ideologies = []

    for header in headers:
        text: str = header.text
        text = text.replace(u"\xa0", " ")
        if text == "Politisk ideologi":
            parent = header.next_sibling
            if parent is not None:
                for ideology in parent.children:
                    if ideology.name == "a":
                        all_ideologies.append(ideology.text)

    return all_ideologies
