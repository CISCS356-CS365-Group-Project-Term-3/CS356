from sqlalchemy.orm import Session
import models.sql_models as models
from util.engine import get_engine

def data_init():
    engine = get_engine()
    with Session(engine) as session:
        project_type = models.ProjectType()
        project_type.name = "EncoderOnly"
        project_type.active = 1
        session.add(project_type)

        project_type2 = models.ProjectType()
        project_type2.name = "Streaming"
        project_type2.active = 1
        session.add(project_type2)

        encoder_type = models.EncoderType()
        encoder_type.name = "Standard Encoder"
        encoder_type.active = 1
        session.add(encoder_type)
        session.commit()

        codec = models.Codec()
        codec.name = "AVC (H.264)"
        codec.active = 1
        codec.encoder_type_id = 1
        session.add(codec)

        codec2 = models.Codec()
        codec2.name = "SVC (H.264)"
        codec2.active = 1
        codec2.encoder_type_id = 1
        session.add(codec2)

        encoder_mode = models.EncoderMode()
        encoder_mode.name = "Random Access"
        encoder_mode.active = 1
        session.add(encoder_mode)

        encoder_mode2 = models.EncoderMode()
        encoder_mode2.name = "Low Delay"
        encoder_mode2.active = 1
        session.add(encoder_mode2)

        transmission_condition = models.TransmissionCondition()
        transmission_condition.name = "Delay"
        transmission_condition.lower_bound = 0
        transmission_condition.upper_bound = 999
        transmission_condition.unit = "ms"
        transmission_condition.active = 1
        session.add(transmission_condition)

        transmission_condition2 = models.TransmissionCondition()
        transmission_condition2.name = "Jitter"
        transmission_condition2.lower_bound = 0
        transmission_condition2.upper_bound = 200
        transmission_condition2.unit = "ms"
        transmission_condition2.active = 1
        session.add(transmission_condition2)

        transmission_condition3 = models.TransmissionCondition()
        transmission_condition3.name = "Packet Loss"
        transmission_condition3.lower_bound = 0
        transmission_condition3.upper_bound = 20
        transmission_condition3.unit = "%"
        transmission_condition3.active = 1
        session.add(transmission_condition3)

        sequence = models.Sequence()
        sequence.name = "foreman"
        sequence.description = "Video of a foreman"
        sequence.active = 1
        session.add(sequence)


        videofile = models.VideoFile()
        videofile.name = "TestVideoFiles"
        videofile.filepath = "TestVideoFile_1920x1080_60hz_10bit"
        videofile.sequence_id = 1
        videofile.spacial_x = 1920
        videofile.spacial_y = 1080
        videofile.temporal = 60
        videofile.depth = 10
        videofile.quality = 20
        videofile.gamut = "Gamut 1"
        videofile.active = 1
        session.add(videofile)

        session.commit()

