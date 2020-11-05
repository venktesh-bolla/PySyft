# stdlib
from collections import OrderedDict
from typing import KeysView
from typing import List
from typing import Union
from typing import ValuesView

# third party
from google.protobuf.reflection import GeneratedProtocolMessageType
from loguru import logger

# syft relative
from . import ObjectStore
from ...decorators import syft_decorator
from ..common.storeable_object import AbstractStorableObject
from ..common.uid import UID


class MemoryStore(ObjectStore):
    """
    Class that implements an in-memory ObjectStorage, backed by a dict.

    Attributes:
        _objects (dict): the dict that backs the storage of the MemoryStorage.
        _search_engine (ObjectSearchEngine): the objects that handles searching by using tags or
        description.
    """

    __slots__ = ["_objects", "_search_engine"]

    def __init__(self) -> None:
        super().__init__()
        self._objects: OrderedDict[UID, AbstractStorableObject] = OrderedDict()
        self._search_engine = None
        self.post_init()

    def get_object(self, id: UID) -> Union[AbstractStorableObject, None]:
        return self._objects.get(id, None)

    def get_objects_of_type(self, obj_type: type) -> List[AbstractStorableObject]:
        return [obj for obj in self.values() if isinstance(obj.data, obj_type)]

    @syft_decorator(typechecking=True)
    def __sizeof__(self) -> int:
        return self._objects.__sizeof__()

    @syft_decorator(typechecking=True)
    def __str__(self) -> str:
        return str(self._objects)

    @syft_decorator(typechecking=True)
    def __len__(self) -> int:
        return len(self._objects)

    @syft_decorator(typechecking=True)
    def keys(self) -> KeysView[UID]:
        return self._objects.keys()

    @syft_decorator(typechecking=True)
    def values(self) -> ValuesView[AbstractStorableObject]:
        return self._objects.values()

    @syft_decorator(typechecking=True, prohibit_args=False)
    def __contains__(self, key: UID) -> bool:
        return key in self._objects.keys()

    @syft_decorator(typechecking=True, prohibit_args=False)
    def __getitem__(self, key: UID) -> AbstractStorableObject:
        try:
            return self._objects[key]
        except Exception as e:
            logger.trace(f"MemoryStore get item error {key} {e}")
            raise e

    @syft_decorator(typechecking=True, prohibit_args=False)
    def __setitem__(self, key: UID, value: AbstractStorableObject) -> None:
        self._objects[key] = value

    @syft_decorator(typechecking=True, prohibit_args=False)
    def __delitem__(self, key: UID) -> None:
        del self._objects[key]

    @syft_decorator(typechecking=True)
    def clear(self) -> None:
        self._objects.clear()

    def _object2proto(self) -> GeneratedProtocolMessageType:
        pass

    @staticmethod
    def _proto2object(proto: GeneratedProtocolMessageType) -> "MemoryStore":
        pass

    def __repr__(self) -> str:
        return self._objects.__repr__()
