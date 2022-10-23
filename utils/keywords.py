from __future__ import annotations

import yake


def get_keywords_from_text(text, number_of_keywords=10):
    """
    Automatically return a number of keywords using the package yake
    Link: https://github.com/LIAAD/yake
    """

    if text is None or text == "":
        return ""

    language = "en"
    max_ngram_size = 1
    deduplication_thresold = 0.9
    deduplication_algo = "seqm"
    windowSize = 1

    custom_kw_extractor = yake.KeywordExtractor(
        lan=language,
        n=max_ngram_size,
        dedupLim=deduplication_thresold,
        dedupFunc=deduplication_algo,
        windowsSize=windowSize,
        top=number_of_keywords,
        features=None,
    )
    list_of_keywords = custom_kw_extractor.extract_keywords(text)
    keywords = ", ".join([x[0] for x in list_of_keywords])
    return keywords
