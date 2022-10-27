# will verifiy end points arguments for presence
# if necessary arguments not sent then remind the user to send
def verify_endpoints_info(sent_data,required_args):
    for data in required_args:
        if(sent_data.get(data) == None):
            return f'The {data} argument is required'

def add_for_patch(sent_data,required_args,got_data):
    count = 0
    arguments = []
    for data in required_args:
        count += 1
        if(sent_data.get(data) != None):
            sent_data.get(data) == got_data[count]
            arguments.append(sent_data.get(data))
        elif(sent_data.get(data)== None):
            arguments.append(sent_data.get(data))

              