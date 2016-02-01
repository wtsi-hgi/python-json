from typing import Any

from hgijson.serialization import Serializer, Deserializer
from hgijson.types import PrimitiveJsonSerializableType


class PrimitiveSerializer(Serializer):
    """
    Serializer for primitive values - just returns them.
    """
    def __init__(self, *args, **kwargs):
        super().__init__((), *args, **kwargs)

    def serialize(self, serializable: Any):
        return serializable

    def _create_serializer_of_type(self, serializer_type: type):
        assert False

    def _create_serialized_container(self) -> Any:
        assert False


class PrimitiveDeserializer(Deserializer):
    """
    Deserializer for primitive values - just returns them.
    """
    def __init__(self, *args, **kwargs):
        super().__init__((), object)

    def deserialize(self, object_property_value_dict: PrimitiveJsonSerializableType):
        return object_property_value_dict

    def _create_deserializer_of_type(self, deserializer_type: type):
        assert False