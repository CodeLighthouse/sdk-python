from sdk.CodeLighthouse import CodeLighthouse

CodeLighthouse.init(workspace_name="mailreaper",
                       x_api_key="NrJ2SrDZWqu4vPIgpbU46AzoR8kpYod02IAenGRo2RfJU_gAgTc9uYiqQFIGABRBYGoFXCXUKqAMwq7qEsnDGg")


@CodeLighthouse.error_catcher(author="hello@codelighthouse.io")
def broken_function():
    not_a_dictionary = 1
    not_a_dictionary.append("HELLO")


broken_function()
