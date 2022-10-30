from datetime import datetime

import requests

from translation.models import Word

from .models import Translator


def send_words():
    now = datetime.now()
    users = Translator.objects.filter(send_time=f"{now.hour}:{now.minute}")
    print(f"Sending for {users.count()} users")
    for user in users:
        words: list[Word] = (
            Word.objects.filter(pullrequest=None)
            .exclude(translators__in=[user])
            .order_by("word")[: user.number_of_words]
        )
        if words.count() < 1:
            continue
        for platform in user.platform_set.filter(is_active=True):
            data = {
                "uuid": str(user.uuid),
                "words": [
                    {"word": word.word, "translations": word.get_source_translations}
                    for word in words
                ],
            }
            res = requests.post(f"{platform.base_url}/get_words", json=data)
