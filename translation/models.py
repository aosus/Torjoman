from django.db import models

from .utils import get_close_match


class Word(models.Model):
    word = models.CharField(max_length=255, unique=True)
    is_checked = models.BooleanField(default=False)

    class Meta:
        ordering = ["word"]

    @property
    def get_source_translations(self) -> list[str]:
        return self.sourcetranslation_set.objects.values_list("translation")

    @property
    def get_users_translations(self) -> list[str]:
        return self.usertranslation_set.objects.values_list("translation")

    def add_translation(self, translation: str) -> "UserTranslation":
        """add_translation Add new `UserTranslation` to word and increase score if similar translation was found.

        Args:
                translation (str): the translation to compare and add/increase score.

        Returns:
                UserTranslation: The new/similar translation object.
                None: if the translation was empty.
        """
        if (translation := translation.strip()) == "":
            return
        match = get_close_match(translation, self.get_users_translations())
        if match:
            t: UserTranslation = UserTranslation.objects.get(
                word=self, translation=match
            )
            t.score += 1
            t.save()
        else:
            t = UserTranslation(word=self, translation=translation)
            t.save()
        return t

    def __str__(self) -> str:
        return self.word


class TranslationBase(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    translation = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f"{self.word}-{self.translation}"


class SourceTranslation(TranslationBase):
    is_default = models.BooleanField(default=False)

    def save(self, *args, **kwargs) -> None:
        if self.is_default:
            try:
                last_default_translation = SourceTranslation.objects.get(
                    word=self.word, is_default=True
                )
                last_default_translation.is_default = False
                last_default_translation.save()
            except SourceTranslation.DoesNotExist:
                pass
        return super().save(*args, **kwargs)

    class Meta(TranslationBase.Meta):
        ordering = ("-is_default", "translation")


class UserTranslation(TranslationBase):
    score = models.PositiveIntegerField(default=0)

    class Meta(TranslationBase.Meta):
        ordering = ("-score", "translation")
