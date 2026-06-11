def generate_sequence_code(sequence, encoder):
    def pad(x):
        """ Pad with zeros """
        x = str(x)
        while len(x) < 3:
            x = "0" + x
        return x

    code = ""
    code += pad(sequence["videoFileId"])
    code += pad(encoder["encoderTypeId"])
    code += pad(encoder["codecId"])
    code += pad(encoder["encoderModeId"])
    return code