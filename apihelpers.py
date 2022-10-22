# will verifiy end points arguments for presence
# if necessary arguments not sent then remind the user to send
def verify_endpoints_info(sent_data,required_args):
    for data in required_args:
        if(sent_data.get(data) == None):
            return f'The {data} argument is required'
