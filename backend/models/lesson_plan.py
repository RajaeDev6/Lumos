class LessonPlan:
    def __init__(self,
                 topic: str,
                 objectives: list,
                 activities: list,
                 assessments: list,
                 created_at=None):
        self.topic = topic
        self.objectives = objectives
        self.activities = activities
        self.assessments = assessments
        self.created_at = created_at

    def to_dict(self):
        return self.__dict__

