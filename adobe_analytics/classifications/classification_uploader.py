import time
import more_itertools
import pandas as pd

from adobe_analytics.classifications.classification_job import ClassificationJob


class ClassificationUploader:
    def __init__(self, client, suite_ids, variable_id, data, email, description="",
                 check_suite_compatibility=True, export_results=False, overwrite_conflicts=True):
        self._validate_data(data)

        self._client = client
        self.suite_ids = suite_ids
        self.variable_id = variable_id
        self.header, self.values = self._header_and_values(data)

        self.email = email
        self.description = description
        self.export_results = export_results
        self.check_suite_compatibility = check_suite_compatibility
        self.overwrite_conflicts = overwrite_conflicts

    @staticmethod
    def _validate_data(data):
        assert isinstance(data, pd.DataFrame), "Please pass data in form of a pandas DataFrame."
        assert data.columns[0] == "Key", "First column must correspond to the variable and be called 'Key'."
        assert data.isnull().sum().sum() == 0, "DataFrame must not contain missing values."

    @staticmethod
    def _header_and_values(data):
        header = list(data.columns)
        values = data.values.tolist()
        return header, values

    def upload(self):
        chunks = more_itertools.chunked(iterable=self.values, n=ClassificationJob.PAGE_SIZE)
        for chunk in chunks:
            self._upload_job(values=chunk)

    def _upload_job(self, values):
        job = self._create_import()
        print("Job ID:", job.id)

        job.add_data(values)
        job.commit()
        self.check_status_until_finished(job)

    def _create_import(self):
        print("Creating job for upload...")

        response = self._client.request(
            api="Classifications",
            method="CreateImport",
            data={
                "rsid_list": self.suite_ids,
                "element": self.variable_id,
                "header": self.header,
                "description": self.description,
                "email_address": self.email,
                "check_divisions": int(self.check_suite_compatibility),
                "export_results": int(self.export_results),
                "overwrite_conflicts": int(self.overwrite_conflicts)
            }
        )
        job_id = response["job_id"]
        return ClassificationJob(client=self._client, job_id=job_id)

    @staticmethod
    def check_status_until_finished(job, sleep_interval=10):
        status = job.check_status()
        while "completed" not in status:
            time.sleep(sleep_interval)
            status = job.check_status()
        print(status)
