from codelighthouse.CodeLighthouse import CodeLighthouse
import os

CodeLighthouse.init(organization_name=os.environ.get("ORG_NAME"),
                    x_api_key=os.environ.get("CODELIGHTHOUSE_SECRET"))


@CodeLighthouse.error_catcher(author="hello@codelighthouse.io")
def broken_function():
    not_a_dictionary = 1
    not_a_dictionary.append("HELLO")


broken_function()
