import more_itertools


DEFAULT_CHUNK_SIZE = 500
MAX_ROWS_PER_JOB = 25000


class AAClassificationJob:
    def __init__(self, client, job_id):
        self._client = client
        self.id = job_id

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

    def add_data(self, values):
        print("Adding data...")
        self._check_max_size(values)

        chunks = more_itertools.chunked(iterable=values, n=DEFAULT_CHUNK_SIZE)
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
    def _check_max_size(values):
        error_message = "Max {}k rows of data per job permitted." \
                        "Please use multiple jobs.".format(int(MAX_ROWS_PER_JOB / 1000))
        assert len(values) <= MAX_ROWS_PER_JOB, error_message

    @staticmethod
    def _to_labeled_rows(values):
        return [{"row": row} for row in values]

    def commit(self):
        print("committing...")
        response = self._client.request(
            api="Classifications",
            method="CommitImport",
            data={
                "job_id": self.id
            }
        )
        return response
