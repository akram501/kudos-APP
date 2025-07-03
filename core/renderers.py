from rest_framework.renderers import JSONRenderer
from collections.abc import Mapping


class CustomResponseRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response_data = {}

        if isinstance(data, dict) and set(data.keys()) >= {"status", "message", "data"}:
            return super().render(data, accepted_media_type, renderer_context)

        # Normal wrapping
        if isinstance(data, Mapping) and (data.get('errors') or data.get('detail') or 'non_field_errors' in data):
            response_data['status'] = False
            if 'detail' in data:
                response_data['message'] = str(data['detail'])
            elif 'errors' in data:
                response_data['message'] = ', '.join([str(v) for val in data['errors'].values() for v in (val if isinstance(val, list) else [val])])
            else:
                messages = []
                for field, field_errors in data.items():
                    if isinstance(field_errors, list):
                        messages.extend(field_errors)
                    else:
                        messages.append(str(field_errors))
                response_data['message'] = ', '.join(messages)
            response_data['data'] = {}
        else:
            response_data['status'] = True
            response_data['message'] = 'Success'
            response_data['data'] = data if data is not None else {}

        return super().render(response_data, accepted_media_type, renderer_context)
