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

        quality = models.Quality()
        quality.name = "testQuality"
        session.add(quality)

        gamut = models.Gamut()
        gamut.name = "testGamut"
        session.add(gamut)

        topology = models.Gamut()
        gamut.name = "testGamut"
        session.add(gamut)

        transmission_condition = models.TransmissionCondition()
        transmission_condition.name = "TestTransmission"
        transmission_condition.lower_bound = 0
        transmission_condition.upper_bound = 300
        session.add(transmission_condition)

        framerate = models.FrameRate()
        framerate.name = "TestFrameRate"
        framerate.frame_rate = 60
        session.add(framerate)

        depth = models.Depth()
        depth.name = "TestDepth"
        depth.depth = 8
        session.add(depth)

        resolution = models.Resolution()
        resolution.name = "TestResolution"
        resolution.x = 1920
        resolution.y = 1080
        session.add(resolution)

        videofile = models.VideoFile()
        videofile.name = "TestVideoFiles"
        videofile.resolutions = [resolution]
        videofile.framerates = [framerate]
        videofile.depths = [depth]
        session.add(videofile)

        session.commit()

