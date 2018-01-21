import datetime
import dateutil.relativedelta


class ReportDefinition:
    GRANULARITIES = ["hour", "day", "week", "month", "quarter", "year"]

    def __init__(self, metrics, dimensions, segments=None,
                 date_from=None, date_to=None, last_days=None, last_months=None, granularity=None,
                 sort_by=None, source="standard", **kwargs):
        self.dimensions = dimensions
        self.metrics = metrics
        self.segments = segments

        self.date_from = date_from
        self.date_to = date_to
        self._determine_dates(last_days, last_months)

        self.granularity = granularity
        self._validate_granularity_input()

        self.sort_by = sort_by
        self.source = source

        self.kwargs = kwargs

    def _prepare_dimensions(self):
        assert isinstance(self.dimensions, list), "dimensions must be a list."
        return [self._clean_dimension(entry) for entry in self.dimensions]

    def _clean_dimension(self, dimension):
        if isinstance(dimension, str):
            return self._format_id(dimension)
        elif isinstance(dimension, dict):
            return dimension
        else:
            raise ValueError("Unexpected type of dimension. Please use str or dict.")

    def _prepare_metrics(self):
        assert isinstance(self.metrics, list), "metrics must be a list."
        return [self._format_id(metric_id) for metric_id in self.metrics]

    def _prepare_segments(self):
        assert isinstance(self.segments, list), "segments must be a list."
        return [self._format_id(segment_id) for segment_id in self.metrics]

    @staticmethod
    def _format_id(dimension_id):
        return {"id": dimension_id}

    def _determine_dates(self, last_days, last_months):
        self._validate_date_input(last_days, last_months)

        if last_days or last_months:
            self._calculate_dates_from_relative(last_days, last_months)

    def _validate_date_input(self, last_days, last_months):
        dates_are_relative = (last_days is not None) or (last_months is not None)
        dates_are_absolute = (self.date_from is not None) or (self.date_to is not None)

        assert dates_are_relative or dates_are_absolute, "No time range specified."
        assert not (dates_are_relative and dates_are_absolute), "Either absolute dates or relative dates."

    def _calculate_dates_from_relative(self, last_days, last_months):
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        offset = dateutil.relativedelta.relativedelta(days=last_days, months=last_months)

        self.date_to = yesterday.isoformat()
        self.date_from = (yesterday - offset).isoformat()

    def _validate_granularity_input(self):
        assert self.granularity in self.GRANULARITIES, "Granularity must be one of: {}.".format(self.GRANULARITIES)

    def as_dict(self):
        report_definition = {
            "reportSuiteID": None,  # will be filled when report is requested
            "elements": self._prepare_dimensions(),
            "metrics": self._prepare_metrics(),
            "segments": self._prepare_segments(),
            "dateFrom": self.date_from,
            "dateTo": self.date_to,
            "dateGranularity": self.granularity,
            "sortBy": self.sort_by,
            "source": self.source
        }
        if self.kwargs:
            report_definition.update(self.kwargs)
        return report_definition
