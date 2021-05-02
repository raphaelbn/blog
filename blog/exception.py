from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None and response.status_code == 400:
        response_data = []
        for field_name in response.data.keys():
            response_data.append({"message": str(response.data[field_name][0]).replace('(field_name)', field_name)})
        response.data = response_data

    return response
