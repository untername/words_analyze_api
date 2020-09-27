from textblob import TextBlob, Word
from textblob.exceptions import NotTranslated
from typing import Dict, Union, Tuple, List, Callable
import operator


def formalizer(translate: bool = True) -> Callable:

    """
    'Фабрика' декораторов. В зависимости от значения аргумента translate, текст переводится или нет.

    По умолчанию - True.
    """

    def decor(func: Callable) -> Callable:

        def wrapper(*args: Tuple[str]) -> Union[Callable, str]:

            targs = TextBlob(*args)
            if translate:
                if targs.detect_language() != 'en':
                    targs = targs.translate(to='en')

            return func(targs)
        return wrapper
    return decor


@formalizer(False)
def wordcount(text: TextBlob) -> Dict[str, str]:

    """ Функция, подсчитывающая частотность слов. Отбрасывает ненужные символы и сортирует результат. """

    result = sorted(
        {x: [y] for x in text.word_counts.items() for y in text.word_counts.items()},
        key=operator.itemgetter(1), reverse=True)

    return dict(result)


@formalizer()
def text_polarity(text: TextBlob) -> Union[str, Dict[str, str]]:

    """
    Функция, анализирующая полярность и субъективность полученного текста.

    Для корректной работы все переводится на английский язык, а уже потом анализируется.
    """

    result = {
        "Polariry": str(text.sentiment.polarity),
        "Subjectivity": str(text.sentiment.subjectivity)}

    return result


@formalizer()
def get_correct(text: TextBlob) -> Dict[str, Union[str, Dict]]:

    """ Функция, возвращающая текст без ошибок и варианты правильного написания слов. """

    corrected_word = text.correct()
    correctly_vars: Dict = {x: str(Word(x).spellcheck()[0][0]) for x in text.words}

    return {
        "corrected": str(corrected_word),
        "correctly words": correctly_vars}


@formalizer()
def get_definitions(text: TextBlob) -> Dict[str, Union[List, str]]:

    """ Функция для нахождения определений конкретных слов. """

    words: List = []
    definitions: List = []

    for x in text.words:
        defins: List = [z for z in Word(x).definitions]

        if len(defins) > 0:
            words.append(x)
            definitions.append(defins)

    couple = dict(zip(words, definitions))
    return couple


@formalizer()
def get_synonyms(text: TextBlob) -> Dict[str, List[str]]:

    """
    Функция, находящая синонимы каждого слова в полученном тексте.

    Для корректной работы текст изначально переводится на английский.
    """

    words: List = []
    synonims: List = []

    for x in text.words:
        syns = set()
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


@formalizer()
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
