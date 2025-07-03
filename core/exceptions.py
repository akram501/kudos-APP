from rest_framework.response import Response
from rest_framework.views import exception_handler


def flatten_errors(errors):
    """
    Recursively flatten DRF validation errors into a list of strings.
    """
    flat_list = []
    if isinstance(errors, list):
        for item in errors:
            flat_list.extend(flatten_errors(item))
    elif isinstance(errors, dict):
        for key, value in errors.items():
            flat_list.extend(flatten_errors(value))
    else:
        flat_list.append(str(errors))
    return flat_list


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        errors = []
        if isinstance(response.data, dict):
            errors = flatten_errors(response.data)
        else:
            errors = [str(response.data)]

        return Response({
            "status": False,
            "message": ", ".join(errors),
            "data": {}
        }, status=response.status_code)

    return response
