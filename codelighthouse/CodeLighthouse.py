import functools
from contextlib import ContextDecorator
from codelighthouse.CodeLighthouseWebHandler import CodeLighthouseWebHandler


class CodeLighthouse(ContextDecorator):
    @staticmethod
    def init(organization_name, x_api_key):
        CodeLighthouseWebHandler.organization_name = organization_name
        CodeLighthouseWebHandler.x_api_key = x_api_key

    @staticmethod
    def error_catcher(email: str):
        def _wrapper_outer(f):
            @functools.wraps(f)
            def _wrapper_inner(*args, **kw):
                try:
                    return f(*args, **kw)
                except BaseException as e:
                    arguments = CodeLighthouse.format_arguments(args, kw)
                    CodeLighthouseWebHandler.send_error(title=f"{type(e).__name__} @ {f.__name__}",
                                                        description=str(e),
                                                        email=email,
                                                        arguments=arguments)

            return _wrapper_inner

        return _wrapper_outer

    @staticmethod
    def format_arguments(args, kwargs):
        """
        Formats the arguments before sending them to the CodeLighthouse Backend

        :param args:
        :param kwargs:
        :return:
        """
        output = {"args": []}

        for arg in args:
            output["args"].append(arg)
        for key, value in kwargs.items():
            output[key] = value

        return output
