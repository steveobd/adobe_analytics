from adobe_analytics.report_definition import ReportDefinition


class Report:
    def __init__(self, definition=None, report_id=None):
        assert definition or report_id, "Provide either report_definition or report_id."
        assert "reportSuiteID" in definition, "Must provide report suite id."

        self.definition = definition
        self.report_id = report_id
        self.raw_response = None

        self.dimensions = None
        self.metrics = None
        self.data = None
        self.dataframe = None

    @classmethod
    def from_universal_definition_and_suite(cls, definition, suite):
        report_definition = ReportDefinition.assert_dict(definition)
        report_definition["reportSuiteID"] = suite.id
        return Report(definition=report_definition)

    def parse(self):
        assert self.raw_response is not None, "Download report data first."
        self.parse_header()
        self.parse_data()

    def parse_header(self):
        report = self.raw_response['report']
        self.dimensions = [entry["name"] for entry in report["elements"]]
        self.metrics = [entry["name"] for entry in report["metrics"]]

    def parse_data(self, row, level=0, upper_levels=None):
        """ This method is recursive. """
        data = dict()
        data_set = list()

        # merge in the upper levels
        if upper_levels is not None:
            data.update(upper_levels)

        if isinstance(row, list):
            for r in row:
                # on the first call set add to the empty list
                pr = self.parse_data(r, level, data.copy())
                if isinstance(pr, dict):
                    data_set.append(pr)
                # otherwise add to the existing list
                else:
                    data_set.extend(pr)

        # pull out the metrics from the lowest level
        if isinstance(row, dict):
            # pull out any relevant data from the current record
            # Handle datetime isn't in the elements list for trended reports
            if level == 0 and self.type == "trended":
                element = "datetime"
            elif self.type == "trended":
                if hasattr(self.elements[level - 1], 'classification'):
                    # handle the case where there are multiple classifications
                    element = str(self.elements[level - 1].id) + ' | ' + str(
                        self.elements[level - 1].classification)
                else:
                    element = str(self.elements[level - 1].id)
            else:
                if hasattr(self.elements[level], 'classification'):
                    # handle the case where there are multiple classifications
                    element = str(self.elements[level].id) + ' | ' + str(self.elements[level].classification)
                else:
                    element = str(self.elements[level].id)

            if element == "datetime":
                data[element] = datetime(int(row.get('year', 0)), int(row.get('month', 0)), int(row.get('day', 0)),
                                         int(row.get('hour', 0)))
                data["datetime_friendly"] = str(row['name'])
            else:
                try:
                    data[element] = str(row['name'])

                # If the name value is Null or non-encodable value, return null
                except:
                    data[element] = "null"

            # parse out any breakdowns and add to the data set
            if 'breakdown' in row and len(row['breakdown']) > 0:
                data_set.extend(self.parse_data(row['breakdown'], level + 1, data))
            elif 'counts' in row:
                for index, metric in enumerate(row['counts']):
                    # decide what type of event
                    if self.metrics[index].decimals > 0 or metric.find('.') > -1:
                        data[str(self.metrics[index].id)] = float(metric)
                    else:
                        data[str(self.metrics[index].id)] = int(metric)

        if len(data_set) > 0:
            return data_set
        else:
            return data

    def to_dataframe(self):
        import pandas as pd

        if self.data is not None:
            return pd.DataFrame.from_dict(self.data)
        return None
