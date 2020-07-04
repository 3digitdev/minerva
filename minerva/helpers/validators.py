from ..categories.tags import Tag
from ..connectors.mongo import MongoConnector
from .exceptions import BadRequestError


def validate_tag_list(instance, attr, value) -> None:
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
