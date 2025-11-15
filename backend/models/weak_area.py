class WeakArea:
    def __init__(self,
                 topic_name: str,
                 mastery: int,
                 difficulty: str,
                 last_updated=None):
        self.topic_name = topic_name
        self.mastery = mastery
        self.difficulty = difficulty
        self.last_updated = last_updated

    def to_dict(self):
        return self.__dict__

