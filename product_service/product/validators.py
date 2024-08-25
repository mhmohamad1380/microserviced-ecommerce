from django.core.exceptions import ValidationError

def validate_product_details(value):
    """
    Validate that each item in the list is a dictionary with the required keys.
    """
    required_keys = {'price', 'size', 'color', 'count'}
    
    if not isinstance(value, list):
        raise ValidationError("The field should be a list of dictionaries.")
    
    for item in value:
        if not isinstance(item, dict):
            raise ValidationError("Each item must be a dictionary.")
        if not required_keys.issubset(item.keys()):
            raise ValidationError(f"Each dictionary must contain the keys: {required_keys}")