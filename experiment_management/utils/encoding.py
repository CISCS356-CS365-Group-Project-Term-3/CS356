def generate_sequence_code(sequence, encoder):
    def pad(x):
        """ Pad with zeros """
        x = str(x)
        while len(x) < 3:
            x = "0" + x
        return x

    code = ""
    code += pad(sequence["video_file_id"])
    code += pad(sequence["resolution_id"])
    code += pad(sequence["frame_rate_id"])
    code += pad(sequence["quality_id"])
    code += pad(sequence["depth_id"])
    code += pad(sequence["gamut_id"])
    code += pad(encoder["encoderTypeId"])
    code += pad(encoder["codecId"])
    code += pad(encoder["encoderModeId"])
    return code