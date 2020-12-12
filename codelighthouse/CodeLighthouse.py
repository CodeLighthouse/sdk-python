import functools
from contextlib import ContextDecorator
from codelighthouse.CodeLighthouseWebHandler import CodeLighthouseWebHandler
import traceback
import sys
import threading


class CodeLighthouse(ContextDecorator):
    web_handler = CodeLighthouseWebHandler()
    resource_name = None
    resource_group = None
    github_repo = None
    default_email = None
    sys_excepthook = None
    threading_excepthook = None
    send_uncaught_exceptions = True

    def __init__(self, organization_name, x_api_key, default_email, send_uncaught_exceptions=True,
                 environment="prod", resource_group: str = None,
                 resource_name: str = None, github_repo: str = None):
        self.web_handler.organization_name = organization_name
        self.web_handler.x_api_key = x_api_key

        self.resource_group = resource_group
        self.resource_name = resource_name
        self.github_repo = github_repo
        self.default_email = default_email
        self.send_uncaught_exceptions = send_uncaught_exceptions

        if self.send_uncaught_exceptions:
            self.install_sys_hook()

        if environment == "local":
            self.web_handler.BASE_URL = "http://localhost:5000"
            self.web_handler.DEBUG = True
        elif environment == "dev":
            self.web_handler.BASE_URL = "https://dev.codelighthouse.io"
            self.web_handler.DEBUG = True
        else:
            self.web_handler.BASE_URL = "https://codelighthouse.io"

    def error_catcher(self, email: str):
        """
        Wraps the function allowing for any previously uncaught error to be caught by CodeLighthouse
        """
        def CLH_wrapper_outer(f):
            @functools.wraps(f)
            def CLH_wrapper_inner(*args, **kw):
                try:
                    return f(*args, **kw)
                except BaseException as e:
                    self.error(e, email, args, kw)

            return CLH_wrapper_inner

        return CLH_wrapper_outer

    def error(self, exception, email=None, args=None, kwargs=None):
        """
        This prepares the exception for our server.  You can optionally pass an email for a specific developer or use
        the global default.

        :param exception: the exception itself.  (e in `except ValueError as e:`)
        :param email: the email of the developer you want to notify.
        :param args: allows you to pass the arguments that went into the function
        :param kwargs: allows you to pass the keyword arguments that went into the function
        :return: The error guid if it was successful -- otherwise, returns None
        """
        arguments = CodeLighthouse.format_arguments(args, kwargs)
        stack_trace = CodeLighthouse.format_stack_trace(exception.__traceback__)

        if not email:
            email = self.default_email

        guid = self.web_handler.send_error(error_type=type(exception).__name__,
                                           function=stack_trace[0]["function"],
                                           resource_group=self.resource_group,
                                           resource_name=self.resource_name,
                                           description=str(exception),
                                           email=email,
                                           arguments=arguments,
                                           stack_trace=stack_trace,
                                           github_repo=self.github_repo)

        # IF WEB_HANDLER ERRORS OUT, IT RETURNS NONE
        return guid

    def excepthook(self, exc_type, exc_value, traceback):
        if self.send_uncaught_exceptions:
            self.error(exc_value)

    def install_sys_hook(self):
        self.send_uncaught_exceptions = True

        self.sys_excepthook = sys.excepthook

        def excepthook(*exc_info):
            print(*exc_info)
            self.excepthook(*exc_info)

            if self.sys_excepthook:
                self.sys_excepthook(*exc_info)

        sys.excepthook = excepthook
        sys.excepthook.codelighthouse_client = self

        if hasattr(threading, 'excepthook'):
            self.threading_excepthook = threading.excepthook

            def threadhook(args):
                self.excepthook(args[0], args[1], args[2])

                if self.threading_excepthook:
                    self.threading_excepthook(args)

            threading.excepthook = threadhook
            threading.excepthook.codelighthouse_client = self

    def uninstall_sys_hook(self):
        self.send_uncaught_exceptions = False

        client = getattr(sys.excepthook, 'codelighthouse_client', None)

        if client is self:
            sys.excepthook = self.sys_excepthook
            self.sys_excepthook = None

        if hasattr(threading, 'excepthook'):
            client = getattr(threading.excepthook, 'codelighthouse_client', None)
            if client is self:
                threading.excepthook = self.threading_excepthook
                self.threading_excepthook = None

    @staticmethod
    def format_arguments(args, kwargs):
        """
        Formats the arguments before sending them to the CodeLighthouse Backend

        :param args:
        :param kwargs:
        :return:
        """
        output = {"args": []}

        if args:
            for arg in args:
                output["args"].append(arg)
        if kwargs:
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