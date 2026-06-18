def generate_sequence_code(sequence, encoder, network):
    def pad(x):
        """ Pad with zeros """
        x = str(x)
        while len(x) < 3:
            x = "0" + x
        return x

    code = ""
    code += pad(sequence.get("videoFileId", 0))
    code += pad(encoder.get("encoderTypeId", 0))
    code += pad(encoder.get("codecId", 0))
    code += pad(encoder.get("encoderModeId", 0))
    code += network.get("packetLoss")
    code += network.get("delay")
    code += network.get("jitter")
    return code