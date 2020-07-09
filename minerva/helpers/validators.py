from ..categories.tags import Tag
from ..connectors.mongo import MongoConnector
from .exceptions import BadRequestError


def validate_tag_list(instance, attr, value) -> None:
    """
    This is a helper function for making sure that when you add a Tag to a Category
    record, there is a matching Tag object in the datastore already.  Also performs
    basic type validation.  This is a method as defined by `attr` for "Validators".
    :param instance: IGNORED
    :param attr: IGNORED
    :param value: The value to be validated.  Should be a list of strings
    :return: N/A
    """
    if isinstance(value, list):
        with MongoConnector(Tag) as db:
            all_tags = [tag.name for tag in db.find_all_no_limit() if isinstance(tag, Tag)]
            for tag in value:
                if tag not in all_tags:
                    raise BadRequestError(
                        f"Could not find a tag named [{tag}].  Please create the tag first."
                    )
    else:
        raise BadRequestError(f"Expected a list of strings but got [{value.__class__.__name__}]")


def day_validator(instance, attr, value) -> None:
    """
    Validate a given day number for a date.  Only does basic range validation for now
    :param instance: IGNORED
    :param attr: IGNORED
    :param value: The day number to be validated.  Assumed to be a valid integer
    :return: N/A
    """
    try:
        day_num = int(value)
        if not (1 <= day_num <= 31):
            raise BadRequestError(f"'day' must be a valid value between 1-31, got [{day_num}]")
        # TODO:  Validate combo of Month/Day
    except ValueError:
        raise BadRequestError(f"Could not convert 'day' value of '{value}' to an integer")


def month_validator(instance, attr, value) -> None:
    """
    Validate a given month number for a date.  Only does basic range validation.
    :param instance: IGNORED
    :param attr: IGNORED
    :param value: The month number to be validated.  Assumed to be a valid integer
    :return: N/A
    """
    try:
        month_num = int(value)
        if not (1 <= month_num <= 12):
            raise BadRequestError(f"'month' must be a valid value between 1-12, got [{month_num}]")
    except ValueError:
        raise BadRequestError(f"Could not convert 'month' value of '{value}' to an integer")


def year_validator(instance, attr, value) -> None:
    """
    Validates the year number.  This is simply a super basic integer conversion check.
    Since the year is possible to be "optional", we also allow it to be an empty string
    :param instance: IGNORED
    :param attr: IGNORED
    :param value: The year number to be validated.
    :return: N/A
    """
    if value == "":
        # This is here so that the year can be an "optional"
        # value without needing a default integer value.
        return
    try:
        int(value)
    except ValueError:
        raise BadRequestError(f"Could not convert 'year' value of '{value}' to an integer")
