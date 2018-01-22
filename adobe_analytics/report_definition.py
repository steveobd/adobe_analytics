import copy
import datetime


class ReportDefinition:
    GRANULARITIES = ["hour", "day", "week", "month", "quarter", "year"]

    def __init__(self, metrics, dimensions, segments=None, date_from=None,
                 date_to=None, last_days=None, granularity=None, **kwargs):
        # mandatory fields
        self.dimensions = dimensions
        self.metrics = metrics
        self.segments = segments

        self.date_from = date_from
        self.date_to = date_to
        self._determine_dates(last_days)

        # optional fields
        self.granularity = granularity
        self.kwargs = kwargs

    def _prepare_metrics(self):
        return self._prepare_abstract(variable=self.metrics, name="metrics", func=self._format_id)

    def _prepare_segments(self):
        return self._prepare_abstract(variable=self.segments, name="segments", func=self._format_id)

    def _prepare_dimensions(self):
        return self._prepare_abstract(variable=self.dimensions, name="dimensions", func=self._clean_dimension)

    @staticmethod
    def _prepare_abstract(variable, name, func):
        error_msg = "{} must be str or list.".format(name)
        assert isinstance(variable, (str, list)), error_msg

        if isinstance(variable, str):
            variable = [variable]
        return[func(entry) for entry in variable]

    def _clean_dimension(self, dimension):
        if isinstance(dimension, str):
            return self._format_id(dimension)
        elif isinstance(dimension, dict):
            return dimension
        else:
            raise ValueError("Unexpected type of dimension. Please use str or dict.")

    @staticmethod
    def _format_id(dimension_id):
        return {"id": dimension_id}

    def _determine_dates(self, last_days):
        self._validate_date_input(last_days)

        if last_days:
            self._calculate_dates_from_relative(last_days)

    def _validate_date_input(self, last_days):
        dates_are_relative = last_days is not None
        dates_are_absolute = (self.date_from is not None) or (self.date_to is not None)

        assert dates_are_relative or dates_are_absolute, "No time range specified."
        assert not (dates_are_relative and dates_are_absolute), "Either absolute dates or relative dates."

    def _calculate_dates_from_relative(self, last_days):
        self.date_from = self._date_days_ago(days=last_days)
        self.date_to = self._date_days_ago(days=1)

    @staticmethod
    def _date_days_ago(days):
        date = datetime.date.today() - datetime.timedelta(days=days)
        return date.isoformat()

    def _validate_granularity_input(self):
        assert self.granularity in self.GRANULARITIES, "Granularity must be in: {}.".format(self.GRANULARITIES)

    def as_dict(self):
        report_definition = self._base_definition()
        report_definition = self._inject_optional_fields(report_definition)
        return report_definition

    def _base_definition(self):
        report_definition = {
            "reportSuiteID": None,  # will be replaced
            "elements": self._prepare_dimensions(),
            "metrics": self._prepare_metrics(),
            "dateFrom": self.date_from,
            "dateTo": self.date_to
        }
        return report_definition

    def _inject_optional_fields(self, report_definition):
        if self.segments is not None:
            report_definition["segments"] = self._prepare_segments()

        if self.granularity is not None:
            self._validate_granularity_input()
            report_definition["dateGranularity"] = self.granularity

        if self.kwargs:
            report_definition.update(self.kwargs)
        return report_definition

    @staticmethod
    def inject_suite_id(report_definition, suite_id):
        report_definition = copy.deepcopy(report_definition)
        report_definition["reportSuiteID"] = suite_id
        return report_definition

    @staticmethod
    def assert_dict(report_definition):
        if isinstance(report_definition, ReportDefinition):
            return report_definition.as_dict()
        return report_definition
