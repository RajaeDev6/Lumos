class Recommendation:
    def __init__(self,
                 index: int,
                 recommendation: str,
                 topic: str,
                 created_at=None):
        self.index = index
        self.recommendation = recommendation
        self.topic = topic
        self.created_at = created_at

    def to_dict(self):
        return self.__dict__

