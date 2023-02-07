from difflib import SequenceMatcher
from heapq import nlargest as _nlargest

import pyarabic.araby as araby  # Language specific module

def get_close_match(word: str, possibilities: list[str], cutoff: float=0.8) -> str | None:
    """Use SequenceMatcher to return a list of the indexes of the best "good enough" matches.

    Args:
        word (str):  A sequence for which close matches are desired.
        possibilities (list[str]): A list of sequences against which to match word.
        cutoff (float, optional): Possibilities that don't score at least that similar to word are ignored. Defaults to 0.8.

    Raises:
        ValueError: if cutoff not between 0 and 1.

    Returns:
        str | Nore : the best match if found else None.
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
        return None


def normalize_translation(translation: str) -> str:
    """normalize_translation Changes the translation before comparing it with saved translations

    Args:
      translation (str): the translation to normalize

    Returns:
      str: the normalized translation
    """
    return araby.strip_harakat(
        araby.strip_tatweel(translation)
    )  # remove the harakat and tatweel from the translation
