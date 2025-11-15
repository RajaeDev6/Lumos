class PerformanceOverview:
    def __init__(self,
                 coverage: int,
                 syllabus_uploaded: bool,
                 test_papers_uploaded: bool,
                 weak_areas_count: int,
                 recommendations_count: int,
                 last_updated=None):
        self.coverage = coverage
        self.syllabus_uploaded = syllabus_uploaded
        self.test_papers_uploaded = test_papers_uploaded
        self.weak_areas_count = weak_areas_count
        self.recommendations_count = recommendations_count
        self.last_updated = last_updated

    def to_dict(self):
        return self.__dict__

