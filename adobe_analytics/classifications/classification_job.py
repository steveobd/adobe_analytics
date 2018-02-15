import more_itertools


class ClassificationJob:
    MAX_ROWS = 25000
    PAGE_SIZE = 500

    def __init__(self, client, job_id):
        self._client = client
        self.id = job_id

    def add_data(self, values):
        print("Adding data to job...")

        chunks = more_itertools.chunked(iterable=values, n=ClassificationJob.PAGE_SIZE)
        for index, chunk in enumerate(chunks):
            page_number = index + 1
            rows = self._to_labeled_rows(chunk)

            is_success = self._client.request(
                api="Classifications",
                method="PopulateImport",
                data={
                    "job_id": self.id,
                    "page": page_number,
                    "rows": rows
                }
            )
            assert is_success, "Failed to add data."

    @staticmethod
    def _to_labeled_rows(values):
        return [{"row": row} for row in values]

    def commit(self):
        print("committing job...")
        response = self._client.request(
            api="Classifications",
            method="CommitImport",
            data={
                "job_id": self.id
            }
        )
        return response

    def check_status(self):
        response = self._client.request(
            api="Classifications",
            method="GetStatus",
            data={
                "job_id": self.id
            }
        )
        status = response[0]["status"].lower()
        return status
