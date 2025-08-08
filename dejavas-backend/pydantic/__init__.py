from typing import Any, Dict, List, Type, TypeVar, get_args, get_origin, get_type_hints

__all__ = ["BaseModel"]


T = TypeVar("T", bound="BaseModel")


class BaseModel:
    def __init__(self, **data: Any) -> None:
        hints = get_type_hints(self.__class__)
        for field, typ in hints.items():
            value = data.get(field)
            origin = get_origin(typ)
            if value is not None:
                if origin is list:
                    inner = get_args(typ)[0]
                    if isinstance(inner, type) and issubclass(inner, BaseModel):
                        value = [inner.parse_obj(v) for v in value]
                elif isinstance(typ, type) and issubclass(typ, BaseModel):
                    value = typ.parse_obj(value)
            setattr(self, field, value)

    @classmethod
    def parse_obj(cls: Type[T], obj: Dict[str, Any]) -> T:
        return cls(**obj)

    def dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        hints = get_type_hints(self.__class__)
        for field, typ in hints.items():
            value = getattr(self, field)
            if isinstance(value, list):
                result[field] = [v.dict() if isinstance(v, BaseModel) else v for v in value]
            elif isinstance(value, BaseModel):
                result[field] = value.dict()
            else:
                result[field] = value
        return result
