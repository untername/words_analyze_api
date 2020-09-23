from textblob import TextBlob, Word
from textblob.exceptions import NotTranslated
from typing import Dict, Union, Tuple, List, Callable
import operator


def translater(func: Callable) -> Callable:

    """ Декоратор, создающий инстанс класса TextBlob и переводящий текст. Это необходимо для всех методов. """

    def wrapper(*args: Tuple, **kwargs: Dict) -> Union[Callable, str]:

        targs = TextBlob(*args)

        if targs.detect_language() != 'en':
            try:
                targs = targs.translate(to='en')
            except NotTranslated:
                return """Unfortunately, the language could not be determined.
                Perhaps the text contains words from several languages. If so, check them separately."""
        return func(targs, **kwargs)
    return wrapper


@translater
def wordcount(text: TextBlob) -> Dict[str, str]:

    """ Функция, подсчитывающая частотность слов. Отбрасывает ненужные символы и сортирует результат. """

    result = sorted(
        {x: [y] for x in text.word_counts.items() for y in text.word_counts.items()},
        key=operator.itemgetter(1), reverse=True)

    return dict(result)


@translater
def text_polarity(text: TextBlob) -> Union[str, Dict[str, str]]:

    """
    Функция, анализирующая полярность и субъективность полученного текста.

    Для корректной работы все переводится на английский язык, а уже потом анализируется.
    """

    result = {
        "Polariry": str(text.sentiment.polarity),
        "Subjectivity": str(text.sentiment.subjectivity)}

    return result


@translater
def get_correct(text: TextBlob) -> Dict[str, str]:

    """ Функция, возвращающая текст без ошибок. """

    corrected_word = text.correct()

    return {"corrected": str(corrected_word)}


@translater
def get_definitions(text: TextBlob) -> Dict[str, Union[List, str]]:

    """ Функция для нахождения определений конкретных слов. """

    words: List = []
    definitions: List = []

    for x in text.words:
        word = Word(x)
        defins: List = [z for z in word.definitions]

        if len(defins) > 0:
            words.append(x)
            definitions.append(defins)

    couple = dict(zip(words, definitions))
    return couple


@translater
def get_synonyms(text: TextBlob) -> Dict[str, List[str]]:

    """
    Функция, находящая синонимы каждого слова в полученном тексте.

    Для корректной работы текст изначально переводится на английский.
    """

    words: List = []
    synonims: List = []

    for x in text.words:
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


@translater
def get_antonyms(text: TextBlob) -> Dict[str, str]:

    """ Функция, возвращающая список антонимов. """

    words: List = []
    antonyms: List = []

    for x in text.words:

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
