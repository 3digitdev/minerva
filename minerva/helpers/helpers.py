from typing import Dict, Any, List, TypeVar, Optional

# --- Custom Types --- #
SingleMongoRecord = Dict[str, Any]
MultiMongoRecord = List[SingleMongoRecord]
JsonData = Dict[str, Any]
T = TypeVar("T")
Maybe = Optional[T]
# -------------------- #


# --- API Helpers --- #
# ------------------- #
