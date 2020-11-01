import functools
from contextlib import ContextDecorator
from codelighthouse.CodeLighthouseWebHandler import CodeLighthouseWebHandler
import traceback


class CodeLighthouse(ContextDecorator):
    web_handler = CodeLighthouseWebHandler
    resource_name = None
    resource_group = None
    github_repo = None

    def __init__(self, organization_name, x_api_key, environment="prod", resource_group: str = None,
                 resource_name: str = None, github_repo: str = None):
        self.web_handler.organization_name = organization_name
        self.web_handler.x_api_key = x_api_key

        self.resource_group = resource_group
        self.resource_name = resource_name
        self.github_repo = github_repo

        if environment == "local":
            self.web_handler.BASE_URL = "http://localhost:5000"
            self.web_handler.DEBUG = True
        elif environment == "dev":
            self.web_handler.BASE_URL = "https://dev.codelighthouse.io"
            self.web_handler.DEBUG = True
        else:
            self.web_handler.BASE_URL = "https://codelighthouse.io"

    def error_catcher(self, email: str):
        def CLH_wrapper_outer(f):
            @functools.wraps(f)
            def CLH_wrapper_inner(*args, **kw):
                try:
                    return f(*args, **kw)
                except BaseException as e:
                    arguments = CodeLighthouse.format_arguments(args, kw)
                    stack_trace = CodeLighthouse.format_stack_trace(e.__traceback__)
                    # for some reason, requires passing itself
                    self.web_handler.send_error(self.web_handler,
                                                error_type=type(e).__name__,
                                                function=f.__name__,
                                                resource_group=self.resource_group,
                                                resource_name=self.resource_name,
                                                description=str(e),
                                                email=email,
                                                arguments=arguments,
                                                stack_trace=stack_trace,
                                                github_repo=self.github_repo)

            return CLH_wrapper_inner

        return CLH_wrapper_outer

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

    @staticmethod
    def format_stack_trace(trace):
        # traceback allows for locals to be found up and down the stack.  Call trace.f_locals for them
        output = []
        for item in traceback.extract_stack(trace.tb_frame):
            if item.name == "CLH_wrapper_inner":
                continue
            data = {
                "file": item.filename,
                "line": item.line,
                "lineno": item.lineno,
                "function": item.name
            }
            output.append(data)
        return output