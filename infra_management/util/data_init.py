from sqlalchemy.orm import Session
from models import sql_models as models
from util.engine import get_engine

def data_init():
    engine = get_engine()
    with Session(engine) as session:
        project_type = models.ProjectType()
        project_type.name = "Encoder Only"
        project_type.active = 1
        project_type.supported = 1
        session.add(project_type)

        project_type2 = models.ProjectType()
        project_type2.name = "Network Simulation"
        project_type2.active = 1
        project_type2.supported = 1
        session.add(project_type2)

        encoder_type = models.EncoderType()
        encoder_type.name = "Standard Encoder"
        encoder_type.active = 1
        session.add(encoder_type)
        session.commit()

        codec = models.Codec()
        codec.name = "h261"
        codec.active = 1
        codec.encoder_type_id = 1
        codec.supported = 1
        session.add(codec)

        codec2 = models.Codec()
        codec2.name = "h263"
        codec2.active = 1
        codec2.encoder_type_id = 1
        codec2.supported = 1
        session.add(codec2)

        codec3 = models.Codec()
        codec3.name = "h264"
        codec3.active = 1
        codec3.encoder_type_id = 1
        codec3.supported = 1
        session.add(codec3)

        codec4 = models.Codec()
        codec4.name = "h265"
        codec4.active = 1
        codec4.encoder_type_id = 1
        codec4.supported = 1
        session.add(codec4)

        transmission_condition = models.TransmissionCondition()
        transmission_condition.name = "Delay"
        transmission_condition.lower_bound = 0
        transmission_condition.upper_bound = 999
        transmission_condition.unit = "ms"
        transmission_condition.active = 1
        transmission_condition.supported = 1
        session.add(transmission_condition)

        transmission_condition2 = models.TransmissionCondition()
        transmission_condition2.name = "Jitter"
        transmission_condition2.lower_bound = 0
        transmission_condition2.upper_bound = 200
        transmission_condition2.unit = "ms"
        transmission_condition2.active = 1
        transmission_condition.supported = 1
        session.add(transmission_condition2)

        transmission_condition3 = models.TransmissionCondition()
        transmission_condition3.name = "Packet Loss"
        transmission_condition3.lower_bound = 0
        transmission_condition3.upper_bound = 20
        transmission_condition3.unit = "%"
        transmission_condition3.active = 1
        transmission_condition.supported = 1
        session.add(transmission_condition3)

        sequence = models.Sequence()
        sequence.name = "blue_sky"
        sequence.description = "Video of a blue sky"
        sequence.active = 1
        sequence.supported = 1
        session.add(sequence)

        sequence2 = models.Sequence()
        sequence2.name = "city"
        sequence2.description = "Video of a city"
        sequence2.active = 1
        sequence2.supported = 1
        session.add(sequence2)

        sequence3 = models.Sequence()
        sequence3.name = "football"
        sequence3.description = "Video of football"
        sequence3.active = 1
        sequence3.supported = 1
        session.add(sequence3)

        sequence4 = models.Sequence()
        sequence4.name = "mobile"
        sequence4.description = "mobile"
        sequence4.active = 1
        sequence4.supported = 1
        session.add(sequence4)

        sequence5 = models.Sequence()
        sequence5.name = "bus"
        sequence5.description = "bus"
        sequence5.active = 1
        sequence5.supported = 1
        session.add(sequence5)

        sequence6 = models.Sequence()
        sequence6.name = "coastguard"
        sequence6.description = "video of the coastguard"
        sequence6.active = 1
        sequence6.supported = 1
        session.add(sequence6)

        sequence7 = models.Sequence()
        sequence7.name = "foreman"
        sequence7.description = "video of the foreman"
        sequence7.active = 1
        sequence7.supported = 1
        session.add(sequence7)

        sequence8 = models.Sequence()
        sequence8.name = "waterfall"
        sequence8.description = "video of a waterfall"
        sequence8.active = 1
        sequence8.supported = 1
        session.add(sequence8)

        videofile = models.VideoFile()
        videofile.name = "blue_sky_1080p"
        videofile.filepath = "blue_sky_1080p25.y4m"
        videofile.sequence_id = 1
        videofile.spacial_x = 1920
        videofile.spacial_y = 1080
        videofile.temporal = 25
        videofile.depth = 10
        videofile.quality = 20
        videofile.gamut = "Gamut 1"
        videofile.active = 1
        videofile.supported = 1
        session.add(videofile)

        videofile2 = models.VideoFile()
        videofile2.name = "city_cif"
        videofile2.filepath = "city_cif.y4m"
        videofile2.sequence_id = 2
        videofile2.spacial_x = 352
        videofile2.spacial_y = 288
        videofile2.temporal = 30
        videofile2.depth = 10
        videofile2.quality = 20
        videofile2.gamut = "Gamut 1"
        videofile2.active = 1
        videofile2.supported = 1
        session.add(videofile2)

        videofile3 = models.VideoFile()
        videofile3.name = "football_cif"
        videofile3.filepath = "football_422_qcif.y4m"
        videofile3.sequence_id = 3
        videofile3.spacial_x = 176
        videofile3.spacial_y = 144
        videofile3.temporal = 30
        videofile3.depth = 10
        videofile3.quality = 20
        videofile3.gamut = "Gamut 1"
        videofile3.active = 1
        videofile3.supported = 1
        session.add(videofile3)

        videofile4 = models.VideoFile()
        videofile4.name = "mobile_dif"
        videofile4.filepath = "mobile_sif.y4m"
        videofile4.sequence_id = 4
        videofile4.spacial_x = 352
        videofile4.spacial_y = 240
        videofile4.temporal = 29.97
        videofile4.depth = 10
        videofile4.quality = 20
        videofile4.gamut = "Gamut 1"
        videofile4.active = 1
        videofile4.supported = 1
        session.add(videofile4)

        videofile5 = models.VideoFile()
        videofile5.name = "bus_cif"
        videofile5.filepath = "bus_cif.y4m"
        videofile5.sequence_id = 5
        videofile5.spacial_x = 352
        videofile5.spacial_y = 288
        videofile5.temporal = 30
        videofile5.depth = 10
        videofile5.quality = 20
        videofile5.gamut = "Gamut 1"
        videofile5.active = 1
        videofile5.supported = 1
        session.add(videofile5)

        videofile6 = models.VideoFile()
        videofile6.name = "coastguard_qcif_mono"
        videofile6.filepath = "coastguard_qcif_mono.y4m"
        videofile6.sequence_id = 6
        videofile6.spacial_x = 176
        videofile6.spacial_y = 144
        videofile6.temporal = 29.97
        videofile6.depth = 10
        videofile6.quality = 20
        videofile6.gamut = "Gamut 1"
        videofile6.active = 1
        videofile6.supported = 1
        session.add(videofile6)

        videofile7 = models.VideoFile()
        videofile7.name = "forman_cif"
        videofile7.filepath = "foreman_cif.y4m"
        videofile7.sequence_id = 7
        videofile7.spacial_x = 352
        videofile7.spacial_y = 288
        videofile7.temporal = 29.97
        videofile7.depth = 10
        videofile7.quality = 20
        videofile7.gamut = "Gamut 1"
        videofile7.active = 1
        videofile7.supported = 1
        session.add(videofile7)

        videofile8 = models.VideoFile()
        videofile8.name = "waterfall_cif"
        videofile8.filepath = "waterfall_cif.y4m"
        videofile8.sequence_id = 8
        videofile8.spacial_x = 352
        videofile8.spacial_y = 288
        videofile8.temporal = 29.97
        videofile8.depth = 10
        videofile8.quality = 20
        videofile8.gamut = "Gamut 1"
        videofile8.active = 1
        videofile8.supported = 1
        session.add(videofile8)

        session.commit()