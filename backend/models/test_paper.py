class TestPaper:
    def __init__(self,
                 file_name: str,
                 file_url: str,
                 extracted_questions: list = None,
                 mapped_topics: list = None,
                 status: str = "pending",
                 upload_date=None):
        self.file_name = file_name
        self.file_url = file_url
        self.status = status
        self.extracted_questions = extracted_questions or []
        self.mapped_topics = mapped_topics or []
        self.upload_date = upload_date

    def to_dict(self):
        return self.__dict__

