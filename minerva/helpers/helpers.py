from typing import Dict, Any, List, TypeVar, Optional
from helpers.exceptions import *

# --- Custom Types --- #
SingleMongoRecord = Dict[str, Any]
MultiMongoRecord = List[SingleMongoRecord]
JsonData = Dict[str, Any]
T = TypeVar("T")
Maybe = Optional[T]
# -------------------- #

# --- API Helpers --- #
def verify_request_body(body: JsonData, required: List[str] = []) -> None:
    for field in required:
        if field not in body:
            raise BadRequestError(f"Invalid request -- missing field {field}")


# ------------------- #
