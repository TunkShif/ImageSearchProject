from rest_framework.renderers import JSONRenderer


class ResponseFormatRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context['response'].status_code
        response = {
            "code": status_code,
            "data": data,
        }

        return super(ResponseFormatRenderer, self).render(response, accepted_media_type, renderer_context)