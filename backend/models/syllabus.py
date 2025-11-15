class Syllabus:
    def __init__(self,
                 file_name: str,
                 file_url: str,
                 extracted_topics: list = None,
                 status: str = "pending",
                 academic_year: str = "",
                 upload_date=None):
        self.file_name = file_name
        self.file_url = file_url
        self.extracted_topics = extracted_topics or []
        self.status = status
        self.academic_year = academic_year
        self.upload_date = upload_date

    def to_dict(self):
        return self.__dict__

