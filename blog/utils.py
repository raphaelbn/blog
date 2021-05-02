def get_default_error_messages(min_length=None):
    return {
        'required': '"(field_name)" is required',
        'invalid': '"(field_name)" is not valid',
        'blank': '"(field_name)" is not allowed to be empty',
        'min_length': f'"(field_name)" length must by {min_length} long',
    }
