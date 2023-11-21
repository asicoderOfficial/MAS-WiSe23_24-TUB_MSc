from typing import Any, Dict, Union

class RecursiveDictConvert:
    """A class for creating objects with attributes."""

    def __init__(self, **kwargs: Any) -> None:
        """
        Initializes the RecursiveDictConvert object with provided keyword arguments.

        Args:
            **kwargs: Key-value pairs to set as attributes of the object.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

def object_to_dict(obj: Any) -> Union[Dict[str, Any], List[Any], Tuple[Any, ...], Any]:
    """
    Recursively converts an object into a dictionary.

    Args:
        obj (Any): The object to be converted.

    Returns:
        Union[Dict[str, Any], List[Any], Tuple[Any, ...], Any]: The converted object.

    Note:
        If the input object is an instance of a class, the function will recursively convert
        its attributes into a dictionary. If the input object is a list, tuple, or dictionary,
        it will recursively convert its elements/values. If the input object is not a container
        or an instance of a class, the original value is returned.

    Example:
        >>> obj = RecursiveDictConvert(name="John", age=25, address=RecursiveDictConvert(city="New York", zip_code="10001"))
        >>> result_dict = object_to_dict(obj)
        >>> print(result_dict)
        {'name': 'John', 'age': 25, 'address': {'city': 'New York', 'zip_code': '10001'}}
    """
    if hasattr(obj, '__dict__'):
        return {key: object_to_dict(value) if not callable(value) else None
                for key, value in obj.__dict__.items() if not key.startswith('__')}
    elif isinstance(obj, list):
        return [object_to_dict(item) for item in obj]
    elif isinstance(obj, tuple):
        return tuple(object_to_dict(item) for item in obj)
    elif isinstance(obj, dict):
        return {key: object_to_dict(value) for key, value in obj.items()}
    else:
        return obj

# Example usage:
obj = RecursiveDictConvert(name="John", age=25, address=RecursiveDictConvert(city="New York", zip_code="10001"))
result_dict = object_to_dict(obj)
print(result_dict)
