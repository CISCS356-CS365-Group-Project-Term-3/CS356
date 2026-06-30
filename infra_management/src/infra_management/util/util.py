from sqlalchemy.orm import Session
from ..models import sql_models as models
from ..util.engine import get_engine

def sequence_create(table, body):
    name = body.get("name")
    description = body.get("description")
    active = 0
    return table(name = name, description = description, active = active)

def sequence_update(row, body):
    name = body.get("name")
    description = body.get("description")
    row.name = name if name else row.name
    row.description = description if description else row.description
    if body.get("active") == 1 and row.supported == 1:
        row.active = 1
    elif body.get("active") == 0:
        row.active = 0
    return row

def encoder_type_create(table, body):
    name = body.get("name")
    description = body.get("description")
    active = 0
    return table(name = name, description = description, active = active)

def encoder_type_update(row, body):
    name = body.get("name")
    description = body.get("description")
    row.name = name if name else row.name
    row.description = description if description else row.description
    if body.get("active") == 1 and row.supported == 1:
        row.active = 1
    elif body.get("active") == 0:
        row.active = 0
    return row


def video_file_create(table, body):
    return table(
        sequence_id = body.get("sequence_id"),
        name = body.get("name"),
        filepath = body.get("filepath"),
        spacial_x = body.get("spacial")[0],
        spacial_y = body.get("spacial")[1],
        temporal = body.get("temporal"),
        depth = body.get("depth"),
        quality = body.get("quality"),
        gamut = body.get("gamut"),
        active = 0
    )

def video_file_update(row, body):
    row.sequence_id = body.get("sequence_id") if body.get("sequence_id") else row.sequence_id
    row.name = body.get("name") if body.get("name") else row.name
    row.filepath = body.get("filepath") if body.get("filepath") else row.filepath
    row.depth = body.get("depth") if body.get("depth") else row.depth
    row.quality = body.get("quality") if body.get("quality") else row.quality
    row.gamut = body.get("gamut") if body.get("gamut") else row.gamut
    if body.get("spacial"):
        row.spacial_x = body.get("spacial")[0]
        row.spacial_y = body.get("spacial")[1]
    row.spacial_x = body.get("spacial") if body.get("spacial") else row.spacial
    if body.get("active") == 1 and row.supported == 1:
        row.active = 1
    elif body.get("active") == 0:
        row.active = 0
    return row

def transmission_create(table, body): #These could be further colapsed into a single function that creates a new instance using **kwargs
    name = body.get("name")
    lower_bound = body.get("lower_bound")
    upper_bound = body.get("upper_bound")
    unit = body.get("unit")
    return table(
        name = name,
        lower_bound = lower_bound,
        upper_bound = upper_bound,
        unit = unit,
        active = 0
    )

def transmission_update(row, body):
    name = body.get("name")
    lower_bound = body.get("lower_bound")
    upper_bound = body.get("upper_bound")
    unit = body.get("unit")
    row.name = name if name else row.name
    row.lower_bound = lower_bound if lower_bound else row.lower_bound
    row.upper_bound = upper_bound if upper_bound else row.upper_bound
    row.unit = unit if unit else row.unit
    if body.get("active") == 1 and row.supported == 1:
        row.active = 1
    elif body.get("active") == 0:
        row.active = 0
    return row

def codec_update(row, body):
    row.version = body.get("version") if body.get("version") else row.version
    row.encoder_type_id = body.get("encoder_type_id") if body.get("encoder_type_id") else row.encoder_type_id
    if body.get("active") == 1 and row.supported == 1:
        row.active = 1
    elif body.get("active") == 0:
        row.active = 0
    row.name = body.get("name") if body.get("name") else row.name

# def codec_create(table, body):
#     return table(
#         name = body.get("name"),
#         active = body.get("active"),
#         version = body.get("version")
#     )
def codec_create(table, body):
    engine = get_engine()
    with Session(engine) as session:
        codec_type_query = session.query(models.EncoderType).filter(models.EncoderType.id == body.get("encoder_type_id")).all()
        if len(codec_type_query) != 1:
            raise Exception("Codec type not found")
    return table(
        name = body.get("name"),
        active = 0,
        version = body.get("version"),
        encoder_type_id = body.get("encoder_type_id")
    )

# def name_id_create(table, body):
#     name = body.get("name") #Name should already be validated at this point.
#     return table(name=name)

def name_id_create(table, body):

    return table(
        name=body.get("name"),
        description=body.get("description"),
        active=body.get("active", 0)
    )

# def name_id_update(row, body):
#
#     if body.get("name") is not None:
#         row.name = body.get("name")
#
#     if body.get("active") is not None:
#         row.active = body.get("active")
#
#     return row

def name_id_update(row, body):
    name = body.get("name")
    active = body.get("active")
    row.name = name if name else row.name
    if body.get("active") == 1 and row.supported == 1:
        row.active = 1
    elif body.get("active") == 0:
        row.active = 0
    return row