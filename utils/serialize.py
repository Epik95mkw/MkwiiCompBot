import json
import dataclasses

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
        def default(o):
            if isinstance(o, Serializable):
                return o.__dict__
            raise TypeError(f'Object of type {self.__class__.__name__} is not fully serializable. '
                            f'Make sure all contained types are either serializable by default '
                            f'or subclasses of the Serializable type.')
        return json.dumps(self, default=default, **kwargs)


    @classmethod
    def from_json(cls, s: str, **kwargs):
        """
        Create a new instance of this serializable class from a JSON string.
        Raises ``ValueError`` if the given JSON format does not match the class properties.
        Keyword arguments are passed to ``json.loads``.
        """
        return cls.__from_json_rec(json.loads(s, **kwargs))


    @classmethod
    def __from_json_rec(cls, d: dict):
        # noinspection PyDataclass
        props = {field.name: field.type for field in dataclasses.fields(cls)}

        if len(dif := props.keys() - d.keys()) > 0:
            raise ValueError(f'Deserialization failed: '
                             f'Missing expected properties for type {cls.__name__}: {dif}')
        if len(dif := d.keys() - props.keys()) > 0:
            raise ValueError(f'Deserialization failed: '
                             f'Unexpected properties for type {cls.__name__}: {dif}')

        for argname, argtype in props.items():
            if isinstance(d[argname], dict) and issubclass(argtype, Serializable):
                d[argname] = argtype.__from_json_rec(d[argname])
            if not isinstance(d[argname], argtype):
                raise ValueError(f'Deserialization failed: '
                                 f'Invalid type for {cls.__name__}.{argname}: '
                                 f'expected {argtype.__name__}, got {type(d[argname]).__name__}')
        return cls(**d)
