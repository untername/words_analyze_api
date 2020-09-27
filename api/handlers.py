from typing import Union, Dict, Tuple, Set
from .analyzers import text_polarity, wordcount, get_synonyms, translate, get_antonyms, get_definitions, get_correct


def text_handler(choice: Set[str], text: str) -> Dict[str, Union[str, Tuple, Dict]]:

    """
    Функция, обрабатывающая текст, введенный в текстовое поле или отправленный в файле.

    Возвращает список результатов анализа, в зависимости от выбора.
    """

    response: Dict = {}

    if 'translate' in choice:
        translate_response = translate(text)
        response['translate'] = translate_response
    if 'definitions' in choice:
        define_resp = get_definitions(text)
        response['definitions'] = define_resp
    if 'correct' in choice:
        corr_resp = get_correct(text)
        response['correct'] = corr_resp
    if 'emocolor' in choice:
        emocolor_response = text_polarity(text)
        response['emotional-color'] = emocolor_response
    if 'count-words' in choice:
        count_response = wordcount(text)
        response['count-words'] = count_response
    if 'synonyms' in choice:
        syn_response = get_synonyms(text)
        response['synonyms'] = syn_response
    if 'antonyms' in choice:
        ant_response = get_antonyms(text)
        response['antonyms'] = ant_response

    return response
