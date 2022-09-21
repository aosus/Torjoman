from difflib import SequenceMatcher
from heapq import nlargest as _nlargest

import pyarabic.araby as araby  # Language specific module


def get_close_match(word, possibilities, cutoff=0.8) -> (str | tuple[()]):
    """Use SequenceMatcher to return a list of the indexes of the best
    "good enough" matches. word is a sequence for which close matches
    are desired (typically a string).
    possibilities is a list of sequences against which to match word
    (typically a list of strings).
    Optional arg cutoff (default 0.8) is a float in [0, 1].  Possibilities
    that don't score at least that similar to word are ignored.
    """

    if not 0.0 <= cutoff <= 1.0:
        raise ValueError("cutoff must be in [0.0, 1.0]: %r" % (cutoff,))
    result = []
    s = SequenceMatcher()
    s.set_seq2(word)
    for idx, x in enumerate(possibilities):
        s.set_seq1(x)
        if (
            s.real_quick_ratio() >= cutoff
            and s.quick_ratio() >= cutoff
            and s.ratio() >= cutoff
        ):
            result.append((s.ratio(), idx))

    # Move the best scorers to head of list
    result = _nlargest(1, result)

    # Strip scores for the best n matches
    if result:
        return possibilities[result[0][1]]
    else:
        return ()


def modify_translation(translation: str) -> str:
    """modify_translation Changes the translation before comparing it with saved translations

    Args:
      translation (str): the translation to modify

    Returns:
      str: the modified translation
    """
    return araby.strip_harakat(
        araby.strip_tatweel(translation)
    )  # remove the harakat and tatweel from the translation
