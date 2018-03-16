import dicttoxml


def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.csv', '.xlsx', '.xls']
    if ext.lower() in valid_extensions:
    	xml = dicttoxml.dicttoxml(value)
    	return xml
    else:
        raise ValidationError(u'Unsupported file extension.')

