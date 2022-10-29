# will verifiy end points arguments for presence
# if necessary arguments not sent then remind the user to send
def verify_endpoints_info(sent_data,required_args):
    for data in required_args:
        if(sent_data.get(data) == None):
            return f'The {data} argument is required'

def constraint_password(password):
    if(len(password) < 8):
        return f'length of password: {password} should be 8 or more.'

    
# will use this function to check the data sent for patch
# if all arguments or data is not sent then it will append
# data from the got_data array and we can use that to send a request
def add_for_patch(sent_data,required_args,original_data):
    for data in required_args:
        if(sent_data.get(data) != None):
            original_data[data] = sent_data[data]
    return original_data

              