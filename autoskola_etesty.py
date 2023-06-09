# https://github.com/RxiPland/autoskola-eTesty-API

import requests
import re



USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"

def get_question(url: str) -> dict:
    """
    Function will return dictionary with question based on full question URL
    """

    PATTERN_VALID_URL = r"https?:\/\/w{0,3}\.?autoskola-testy\.cz\/prohlizeni_otazek\.php\?otazka=\d+-[a-zA-Z_0-9]+"

    if re.match(PATTERN_VALID_URL, url) == None:
        raise Exception("URL is not valid!")
    

    PATTERN_QUESTION_TEXT = r"\"question-text\".+>(.+)\n*\t*<\/p>"
    PATTERN_QUESTION_MEDIA = r"src=\"(\/img\/[a-zA-z0-9\/]+.[a-zA-Z0-9]+)"

    PATTERN_CORRECT = r"\"answer otazka_spravne\".+\n*\t*.+<p>(.+)<\/p>"
    PATTERN_WRONG = r"\"answer otazka_spatne\".+\n*\t*.+<p>(.+)<\/p>"

    PATTERN_QUESTION_ID = r"má kód (\d+)"
    PATTERN_POINTS = r"za její správné zodpovězení v testech se získá.+(\d) body?"
    PATTER_QUESTION_TOPIC_ID = r"Tato otázka ze skupiny .+\?okruh=(\d)+"


    question_text = str()
    question_media = str()
    correct_text = str()
    correct_media = str()
    wrong1_text = str()
    wrong1_media = str()
    wrong2_text = str()
    wrong2_media = str()
    question_id = str()
    points = str()
    question_topic_id = -1


    response = requests.get(url, headers={"User-Agent": USER_AGENT})
    response_html = response.text

    if "/img/single" in response_html:

        # QUESTION TEXT
        question_text: list[str] = re.findall(PATTERN_QUESTION_TEXT, response_html)

        if len(question_text) > 0:
            question_text = question_text[0].strip()
        else:
            question_text = str()
        
        # QUESTION MEDIA
        question_media: list[str] = re.findall(PATTERN_QUESTION_MEDIA, response_html)

        if len(question_media) > 0:
            question_media = question_media[0].strip()
            question_media = "https://www.autoskola-testy.cz" + question_media
        else:
            question_media = str()

        # CORRECT ANSWER TEXT
        correct_text: list[str] = re.findall(PATTERN_CORRECT, response_html)

        if len(correct_text) > 0:
            correct_text = correct_text[0].strip()
        else:
            correct_text = str()

        # WRONG ANSWER #1 TEXT
        wrong1_text: list[str] = re.findall(PATTERN_WRONG, response_html)

        if len(wrong1_text) > 0:
            wrong1_text = wrong1_text[0].strip()
        else:
            wrong1_text = str()

        # WRONG ANSWER #2 TEXT
        wrong2_text: list[str] = re.findall(PATTERN_WRONG, response_html)

        if len(wrong2_text) > 1:
            wrong2_text = wrong2_text[1].strip()
        else:
            wrong2_text = str()


    elif "/img/tripple/" in response_html:

        # QUESTION TEXT
        question_text: list[str] = re.findall(PATTERN_QUESTION_TEXT, response_html)

        if len(question_text) > 0:
            question_text = question_text[0].strip()
        else:
            question_text = str()

        # CORRECT ANSWER MEDIA
        correct_media: list[str] = re.findall(PATTERN_CORRECT, response_html)

        if len(correct_media) > 0:
            correct_media: str = correct_media[0].strip()
            correct_media = correct_media.lstrip("<img src=\"")
            correct_media = correct_media.rstrip("\">")
            correct_media = "https://www.autoskola-testy.cz" + correct_media

        else:
            correct_media = str()

        # WRONG ANSWER #1 MEDIA
        wrong1_media: list[str] = re.findall(PATTERN_WRONG, response_html)

        if len(wrong1_media) > 0:
            wrong1_media: str = wrong1_media[0].strip()
            wrong1_media = wrong1_media.lstrip("<img src=\"")
            wrong1_media = wrong1_media.rstrip("\">")
            wrong1_media = "https://www.autoskola-testy.cz" + wrong1_media

        else:
            wrong1_media = str()

        # WRONG ANSWER #2 MEDIA
        wrong2_media: list[str] = re.findall(PATTERN_WRONG, response_html)

        if len(wrong2_media) > 1:
            wrong2_media: str = wrong2_media[1].strip()
            wrong2_media = wrong2_media.lstrip("<img src=\"")
            wrong2_media = wrong2_media.rstrip("\">")
            wrong2_media = "https://www.autoskola-testy.cz" + wrong2_media

        else:
            wrong2_media = str()

    else:

        # QUESTION TEXT
        question_text: list[str] = re.findall(PATTERN_QUESTION_TEXT, response_html)

        if len(question_text) > 0:
            question_text = question_text[0].strip()
        else:
            question_text = str()

        # CORRECT ANSWER TEXT
        correct_text: list[str] = re.findall(PATTERN_CORRECT, response_html)

        if len(correct_text) > 0:
            correct_text = correct_text[0].strip()
        else:
            correct_text = str()

        # WRONG ANSWER TEXT #1
        wrong1_text: list[str] = re.findall(PATTERN_WRONG, response_html)

        if len(wrong1_text) > 0:
            wrong1_text = wrong1_text[0].strip()
        else:
            wrong1_text = str()

        # WRONG ANSWER TEXT #2
        wrong2_text: list[str] = re.findall(PATTERN_WRONG, response_html)

        if len(wrong2_text) > 1:
            wrong2_text = wrong2_text[1].strip()
        else:
            wrong2_text = str()


    # QUESTION ID
    question_id: list[str] = re.findall(PATTERN_QUESTION_ID, response_html)

    if len(question_id) > 0:
        question_id = question_id[0].strip()
    else:
        question_id = str()
    
    # POINTS
    points: list[str] = re.findall(PATTERN_POINTS, response_html)

    if len(points) > 0:
        points = points[0].strip()
    else:
        points = str()

    # QUESTION TOPIC ID
    question_topic_id: list[str] = re.findall(PATTER_QUESTION_TOPIC_ID, response_html)

    if len(question_topic_id) > 0:
        question_topic_id = question_topic_id[0].strip()

        try:
            question_topic_id = int(question_topic_id)
        except:
            question_topic_id = -1

    else:
        question_topic_id = -1


    return {
        "question_text": question_text,
        "question_media": question_media,

        "correct_text": correct_text,
        "correct_media": correct_media,

        "wrong1_text": wrong1_text,
        "wrong1_media": wrong1_media,

        "wrong2_text": wrong2_text,
        "wrong2_media": wrong2_media,

        "question_id": question_id,
        "topic_id": question_topic_id,
        "points": points
    }


def get_random_question(question_topic_id: int) -> dict:
    """
    Function will return dictionary with random question based on topic ID (1-7)
    """

    if question_topic_id < 1 or question_topic_id > 7:
        raise Exception("Question topic ID integer must be between 1 and 7")
    
    URL = "https://www.autoskola-testy.cz/prohlizeni_otazek.php?random="

    PATTERN_QUESTION_TEXT = r"\"question-text\".+>(.+)\n*\t*<\/p>"
    PATTERN_QUESTION_MEDIA = r"src=\"(\/img\/[a-zA-z0-9\/]+.[a-zA-Z0-9]+)"

    PATTERN_CORRECT = r"\"answer otazka_spravne\".+\n*\t*.+<p>(.+)<\/p>"
    PATTERN_WRONG = r"\"answer otazka_spatne\".+\n*\t*.+<p>(.+)<\/p>"

    PATTER_QUESTION_ID = r"má kód (\d+)"
    PATTER_POINTS = r"za její správné zodpovězení v testech se získá.+(\d) body?"


    question_text = str()
    question_media = str()
    correct_text = str()
    correct_media = str()
    wrong1_text = str()
    wrong1_media = str()
    wrong2_text = str()
    wrong2_media = str()
    question_id = str()
    points = str()


    response = requests.get(URL + str(question_topic_id), headers={"User-Agent": USER_AGENT, "Referer": URL + str(question_topic_id)})
    response_html = response.text

    if "/img/single" in response_html:

        # QUESTION TEXT
        question_text: list[str] = re.findall(PATTERN_QUESTION_TEXT, response_html)

        if len(question_text) > 0:
            question_text = question_text[0].strip()
        else:
            question_text = str()
        
        # QUESTION MEDIA
        question_media: list[str] = re.findall(PATTERN_QUESTION_MEDIA, response_html)

        if len(question_media) > 0:
            question_media = question_media[0].strip()
            question_media = "https://www.autoskola-testy.cz" + question_media
        else:
            question_media = str()

        # CORRECT ANSWER TEXT
        correct_text: list[str] = re.findall(PATTERN_CORRECT, response_html)

        if len(correct_text) > 0:
            correct_text = correct_text[0].strip()
        else:
            correct_text = str()

        # WRONG ANSWER #1 TEXT
        wrong1_text: list[str] = re.findall(PATTERN_WRONG, response_html)

        if len(wrong1_text) > 0:
            wrong1_text = wrong1_text[0].strip()
        else:
            wrong1_text = str()

        # WRONG ANSWER #2 TEXT
        wrong2_text: list[str] = re.findall(PATTERN_WRONG, response_html)

        if len(wrong2_text) > 1:
            wrong2_text = wrong2_text[1].strip()
        else:
            wrong2_text = str()


    elif "/img/tripple/" in response_html:

        # QUESTION TEXT
        question_text: list[str] = re.findall(PATTERN_QUESTION_TEXT, response_html)

        if len(question_text) > 0:
            question_text = question_text[0].strip()
        else:
            question_text = str()

        # CORRECT ANSWER MEDIA
        correct_media: list[str] = re.findall(PATTERN_CORRECT, response_html)

        if len(correct_media) > 0:
            correct_media: str = correct_media[0].strip()
            correct_media = correct_media.lstrip("<img src=\"")
            correct_media = correct_media.rstrip("\">")
            correct_media = "https://www.autoskola-testy.cz" + correct_media

        else:
            correct_media = str()

        # WRONG ANSWER #1 MEDIA
        wrong1_media: list[str] = re.findall(PATTERN_WRONG, response_html)

        if len(wrong1_media) > 0:
            wrong1_media: str = wrong1_media[0].strip()
            wrong1_media = wrong1_media.lstrip("<img src=\"")
            wrong1_media = wrong1_media.rstrip("\">")
            wrong1_media = "https://www.autoskola-testy.cz" + wrong1_media

        else:
            wrong1_media = str()

        # WRONG ANSWER #2 MEDIA
        wrong2_media: list[str] = re.findall(PATTERN_WRONG, response_html)

        if len(wrong2_media) > 1:
            wrong2_media: str = wrong2_media[1].strip()
            wrong2_media = wrong2_media.lstrip("<img src=\"")
            wrong2_media = wrong2_media.rstrip("\">")
            wrong2_media = "https://www.autoskola-testy.cz" + wrong2_media

        else:
            wrong2_media = str()

    else:

        # QUESTION TEXT
        question_text: list[str] = re.findall(PATTERN_QUESTION_TEXT, response_html)

        if len(question_text) > 0:
            question_text = question_text[0].strip()
        else:
            question_text = str()

        # CORRECT ANSWER TEXT
        correct_text: list[str] = re.findall(PATTERN_CORRECT, response_html)

        if len(correct_text) > 0:
            correct_text = correct_text[0].strip()
        else:
            correct_text = str()

        # WRONG ANSWER TEXT #1
        wrong1_text: list[str] = re.findall(PATTERN_WRONG, response_html)

        if len(wrong1_text) > 0:
            wrong1_text = wrong1_text[0].strip()
        else:
            wrong1_text = str()

        # WRONG ANSWER TEXT #2
        wrong2_text: list[str] = re.findall(PATTERN_WRONG, response_html)

        if len(wrong2_text) > 1:
            wrong2_text = wrong2_text[1].strip()
        else:
            wrong2_text = str()


    # QUESTION ID
    question_id: list[str] = re.findall(PATTER_QUESTION_ID, response_html)

    if len(question_id) > 0:
        question_id = question_id[0].strip()
    else:
        question_id = str()
    
    # POINTS
    points: list[str] = re.findall(PATTER_POINTS, response_html)

    if len(points) > 0:
        points = points[0].strip()
    else:
        points = str()


    return {
        "question_text": question_text,
        "question_media": question_media,

        "correct_text": correct_text,
        "correct_media": correct_media,

        "wrong1_text": wrong1_text,
        "wrong1_media": wrong1_media,

        "wrong2_text": wrong2_text,
        "wrong2_media": wrong2_media,

        "question_id": question_id,
        "topic_id": question_topic_id,
        "points": points
    }


def get_questions_urls(questions_topic_id: int) -> list[tuple]:
    """
    Function will return list of tuples -> (question ID, question URL) of all questions based on topic id (1-7)
    """

    if questions_topic_id < 1 or questions_topic_id > 7:
        raise Exception("Question topic ID integer must be between 1 and 7")
    
    URL = "https://www.autoskola-testy.cz/prohlizeni_otazek.php?okruh="

    PATTERN_QUESTIONS_URLS = r"kód (\d+), <a href=\"(\S+)\">"


    final: list[tuple] = list()

    response = requests.get(URL + str(questions_topic_id), headers={"User-Agent": USER_AGENT, "Referer": "https://www.autoskola-testy.cz/prohlizeni_otazek.php"})
    response_html = response.text

    regex_temp: list[str] = re.findall(PATTERN_QUESTIONS_URLS, response_html)

    for found in regex_temp:

        final.append(tuple([found[0], "https://www.autoskola-testy.cz/prohlizeni_otazek.php" + found[1]]))


    return final
