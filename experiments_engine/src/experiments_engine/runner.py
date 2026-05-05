
def decode(message_body):
    # method will construct an experiment object from the message
    return message_body.decode()

def conduct(experiment):
    # method will run the actual experiment
    return f"the {experiment} experiment is now completed"

def experiment(message_body):
    experiment = decode(message_body)
    print(f"experiment decoded: {experiment}")
    result = conduct(experiment)
    print(f"experiment completed: {result}")