from sqlalchemy.orm import Session
import models.sql_models as models
from util.engine import get_engine

def data_init():
    engine = get_engine()
    with Session(engine) as session:
        project_type = models.ProjectType()
        project_type.name = "testProjectType"
        session.add(project_type)

        encoder_type = models.EncoderType()
        encoder_type.name = "testEncoderType"
        session.add(encoder_type)

        codec = models.Codec()
        codec.name = "testCodec"
        session.add(codec)

        encoder_mode = models.EncoderModes()
        encoder_mode.name = "testEncoderMode"
        session.add(encoder_mode)

        transmission_condition = models.TransmissionCondition()
        transmission_condition.name = "TestTransmission"
        transmission_condition.lower_bound = 0
        transmission_condition.upper_bound = 300
        session.add(transmission_condition)

        sequence = models.Sequence()
        sequence.name = "foreman"
        sequence.description = "Video of a foreman"
        session.add(sequence)


        videofile = models.VideoFile()
        videofile.name = "TestVideoFiles"
        videofile.filepath = "TestVideoFile_1920x1080_60hz_10bit"
        videofile.sequence_id = 1
        videofile.resolution_x = 1920
        videofile.resolution_y = 1080
        videofile.framerate = 60
        videofile.depth = 10
        videofile.quality = 20
        videofile.gamut = "Gamut 1"
        session.add(videofile)

        session.commit()

