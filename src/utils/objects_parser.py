from typing import Union, List, Tuple, Dict

class RecursiveDictConvert:
    """A class for creating objects with attributes."""

    def __init__(self, **kwargs):
        """
        Initializes the RecursiveDictConvert object with provided keyword arguments.

        Args:
            **kwargs: Key-value pairs to set as attributes of the object.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)


def object_to_dict(obj: Union[RecursiveDictConvert, List, Tuple, Dict, int, str, float]) -> Union[Dict, List, Tuple, int, str, float]:
    """
    Recursively converts an object into a dictionary.

    Args:
        obj (Union[RecursiveDictConvert, List, Tuple, Dict, int, str, float]): The object to be converted.

    Returns:
        Union[Dict, List, Tuple, int, str, float]: The converted object.

    Note:
        If the input object is an instance of RecursiveDictConvert, the function will recursively convert
        its attributes into a dictionary. If the input object is a list, tuple, or dictionary, it will
        recursively convert its elements/values. If the input object is not a container or RecursiveDictConvert,
        the original value is returned.

    Example:
        >>> obj = RecursiveDictConvert(name="John", age=25, address=RecursiveDictConvert(city="New York", zip_code="10001"))
        >>> result_dict = object_to_dict(obj)
        >>> print(result_dict)
        {'name': 'John', 'age': 25, 'address': {'city': 'New York', 'zip_code': '10001'}}
    """
    if isinstance(obj, RecursiveDictConvert):
        return {key: object_to_dict(value) if isinstance(value, RecursiveDictConvert) else value
                for key, value in obj.__dict__.items()}
    elif isinstance(obj, list):
        return [object_to_dict(item) if isinstance(item, (RecursiveDictConvert, list, tuple, dict)) else item for item in obj]
    elif isinstance(obj, tuple):
        return tuple(object_to_dict(item) if isinstance(item, (RecursiveDictConvert, list, tuple, dict)) else item for item in obj)
    elif isinstance(obj, dict):
        return {key: object_to_dict(value) if isinstance(value, (RecursiveDictConvert, list, tuple, dict)) else value
                for key, value in obj.items()}
    else:
        return obj
