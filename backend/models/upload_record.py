class UploadRecord:
    def __init__(self,
                 file_name: str,
                 file_type: str,
                 file_url: str,
                 upload_date=None):
        self.file_name = file_name
        self.file_type = file_type
        self.file_url = file_url
        self.upload_date = upload_date

    def to_dict(self):
        return self.__dict__

