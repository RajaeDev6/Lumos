class Teacher:
    def __init__(self,
                 name: str,
                 email: str,
                 syllabus_status: str = "not_uploaded",
                 test_paper_status: str = "not_uploaded",
                 coverage: int = 0,
                 total_topics: int = 0,
                 weak_areas_count: int = 0):
        self.name = name
        self.email = email
        self.syllabus_status = syllabus_status
        self.test_paper_status = test_paper_status
        self.coverage = coverage
        self.total_topics = total_topics
        self.weak_areas_count = weak_areas_count

    def to_dict(self):
        return self.__dict__

