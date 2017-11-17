class MandatoryKeyError(Exception):

    def __init__(self, key):

        self.key = key

    def __str__(self):
        return 'Не хватает обязательного атрибута {}'.format(self.key)