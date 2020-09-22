from textblob import TextBlob, Word
from textblob.exceptions import NotTranslated
from typing import Dict, Union, Tuple, List
import operator


def wordcount(text: str) -> Dict[str, str]:

    """ Функция, подсчитывающая частотность слов. Отбрасывает ненужные символы и сортирует результат. """

    textb: TextBlob = TextBlob(text)

    result = sorted(
        {x: [y] for x in textb.word_counts.items() for y in textb.word_counts.items()},
        key=operator.itemgetter(1), reverse=True)

    return dict(result)


def text_polarity(text: str) -> Union[str, Dict[str, str]]:

    """
    Функция, анализирующая полярность и субъективность полученного текста.

    Для корректной работы все переводится на английский язык, а уже потом анализируется.
    """

    textb: TextBlob = TextBlob(text)

    if textb.detect_language() != "en":
        try:
            textb = textb.translate(to="en")
        except NotTranslated:
            return """Unfortunately, the language could not be determined.
            Perhaps the text contains words from several languages. If so, check them separately."""

    result = {
        "Polariry": str(textb.sentiment.polarity),
        "Subjectivity": str(textb.sentiment.subjectivity)}

    return result


def get_synonyms(text: str) -> Dict[str, List[str]]:

    """
    Функция, находящая синонимы каждого слова в полученном тексте.

    Для корректной работы текст изначально переводится на английский.
    """

    textb = TextBlob(text)

    if textb.detect_language() != "en":
        textb = textb.translate(to="en")

    words: List = []
    synonims: List = []

    for x in textb.words:
        syns = set()  # Дабы не было повторений.
        item = Word(x)
        for synset in item.synsets:
            for lem in synset.lemmas():
                syns.add((lem.name().replace('_', ' ').capitalize()))

        synsy = list(syns)

        if len(synsy) >= 2:
            words.append(x.capitalize())
            synonims.append(synsy)

    result = dict(zip(words, synonims))
    return result


def get_antonyms(text: str) -> Dict[str, str]:

    """ Функция, возвращающая список антонимов. """

    btext = TextBlob(text)

    if btext.detect_language() != "en":
        btext = btext.translate(to="en")

    words: List = []
    antonyms: List = []

    for x in btext.words:

        xword = Word(x)
        x_antonyms: List = []

        for synset in xword.synsets:
            for lemmas in synset.lemmas():
                try:
                    _ = lemmas.antonyms()[0]
                except IndexError:
                    continue
                else:
                    word_ant = lemmas.antonyms()
                    x_antonyms.append((word_ant[0].name().replace('_', ' ').capitalize()))

        if len(x_antonyms) >= 1:
            words.append(x.capitalize())
            antonyms.append(x_antonyms)

    result = dict(zip(words, antonyms))
    return result


def get_definitions(text: str) -> Dict[str, Union[List, str]]:

    """ Функция для нахождения определений конкретных слов. """

    b_text = TextBlob(text)

    if b_text.detect_language() != 'en':
        b_text.translate(to='en')

    words: List = []
    definitions: List = []

    for x in b_text.words:
        word = Word(x)
        defins: List = [z for z in word.definitions]

        if len(defins) > 0:
            words.append(x)
            definitions.append(defins)

    couple = dict(zip(words, definitions))
    return couple


def translate(text: str) -> Union[str, Tuple[str, str]]:

    """ Ничего необычного. Функция, переводящая с русского на английский или наоборот. """

    btext: TextBlob = TextBlob(text)
    try:
        if btext.detect_language() == "en":
            response = btext.translate(to="ru")
        elif btext.detect_language() == "ru":
            response = btext.translate(to="en")
        else:
            response = "Sorry, so far the translation function is only available for Russian and English"
    except NotTranslated:
        return """Unfortunately, the language could not be determined.
        Perhaps the text contains words from several languages. If so, check them separately."""
    else:
        return text, str(response)


def get_correct(text: str) -> Dict[str, str]:

    """ Функция, возвращающая текст без ошибок. """

    b_text = TextBlob(text)

    if b_text.detect_language() != 'en':
        b_text.translate(to='en')

    corrected_word = b_text.correct()

    return {"corrected": str(corrected_word)}
