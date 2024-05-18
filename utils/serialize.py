import json
import dataclasses

@dataclasses.dataclass
class Serializable:
    """
    A utility class that allows deep/nested conversion between JSON and Python dataclasses.

    To use, inherit this class in the dataclass you want to serialize, and make sure all
    properties of the dataclass are type annotated (even the ones with default values)
    """
    def __init__(self, **_):
        pass


    def to_json(self, **kwargs) -> str:
        """
        Convert this serializable object to a JSON string.
        Raises ``TypeError`` if object is not fully serializable.
        Keyword arguments are passed to ``json.dumps``.
        """
        return json.dumps(dataclasses.asdict(self), **kwargs)


    @classmethod
    def from_json(cls, s: str, *, strict=False, **kwargs):
        """
        Create a new instance of this serializable class from a JSON string.
        Raises ``ValueError`` if the given JSON format does not match the class properties.
        Keyword arguments are passed to ``json.loads``.
        """
        return cls.__from_json_rec(json.loads(s, **kwargs), strict=strict)


    @classmethod
    def __from_json_rec(cls, d: dict, *, strict=False):
        props = {field.name: field.type for field in dataclasses.fields(cls)}

        if strict and len(dif := props.keys() - d.keys()) > 0:
            raise TypeError(f'Deserialization failed: '
                            f'Missing expected properties for type {cls.__name__}: {dif}')
        if strict and len(dif := d.keys() - props.keys()) > 0:
            raise TypeError(f'Deserialization failed: '
                            f'Unexpected properties for type {cls.__name__}: {dif}')

        outd = {}
        for argname, argtype in props.items():
            if argname not in d:
                continue
            if isinstance(d[argname], dict) and issubclass(argtype, Serializable):
                outd[argname] = argtype.__from_json_rec(d[argname])
            elif not isinstance(d[argname], argtype):
                if strict:
                    raise TypeError(
                        f'Deserialization failed: '
                        f'Invalid type for {cls.__name__}.{argname}: '
                        f'expected {argtype.__name__}, got {type(d[argname]).__name__}'
                    )
            else:
                outd[argname] = d[argname]

        return cls(**outd)
