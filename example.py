from codelighthouse.CodeLighthouse import CodeLighthouse
import os

lighthouse = CodeLighthouse(organization_name=os.environ.get("ORG_NAME"),
                            x_api_key=os.environ.get("CODELIGHTHOUSE_SECRET"),
                            resource_group="AWS EC2s",
                            resource_name="application core"
                            )


@lighthouse.error_catcher(email="kyle@codelighthouse.io")
def broken_function():
    not_a_dictionary = 1
    not_a_dictionary.append("HELLO")


broken_function()
