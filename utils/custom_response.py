from rest_framework.response import Response


def CustomResponse(data=None, status=None, template_name=None, headers=None, exception=False, content_type=None):
    if isinstance(data, dict) and next(iter(data)) == 'success':
        return Response(data, status=status, template_name=template_name, headers=headers, exception=exception,
                        content_type=content_type)
    tmpData = dict()
    tmpData['success'] = True
    if isinstance(data, dict):
        tmpData['result'] = data
    elif isinstance(data, list):
        list_data = {
            'results': data
        }
        tmpData['result'] = list_data
    return Response(tmpData, template_name=template_name, headers=headers, exception=exception,
                    content_type=content_type)
