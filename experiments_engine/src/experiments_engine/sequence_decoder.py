import logging
 
# used to log errors and warnings during decoding
logger = logging.getLogger(__name__)
 
 
# Custom exception class for sequence decoding errors
class SequenceDecoderError(Exception):
    pass
 
 
# SequenceDecoder takes a 30-character sequence code and decodes it
# into a dictionary of encoding parameters.
 
class SequenceDecoder:
 
    # This dictionary maps each segment position (0-9) to the field it represents
    FIELD_NAMES = {
        0: "raw_file",
        1: "encoder_type",
        2: "codec",
        3: "encoder_mode",
        4: "loss",
        5: "delay",
        6: "jitter",
    }

    SEGMENT_LENGTH = 3
    SEGMENTS_PER_LAYER = len(FIELD_NAMES)
    CODE_LENGTH = SEGMENT_LENGTH * SEGMENTS_PER_LAYER  # 30

    @classmethod
    def decode(cls, code, config):
        # Takes the raw 30-char code and a config lookup table.
        # Returns a dictionary of decoded field names to their human-readable values
 
        # Check the code is valid, not empty
        cls.validate_code(code)
 
        # Separate the layer, single will return the code as is
        layer_code = cls.separate_layer(code)
 
        # Split the 30-char code into 10 segments of 3 chars each
        segments = cls.segment_code(layer_code)
 
        # Map each segment to its field name based on position
        field_map = cls.map_segments_to_fields(segments)
 
        # Look up each segment in the config to get the decoded values
        decoded = cls.build_decoded_dict(field_map, config)
 
        return decoded
 
    @classmethod
    def validate_code(cls, code):
        # Checks that the code is a non-empty string and correct length
 
        if not code or not isinstance(code, str):
            logger.error("Invalid code: empty or not a string.")
            raise SequenceDecoderError(
                "Code must be a non-empty string."
            )
 
        if len(code) != cls.CODE_LENGTH:
            logger.error(
                f"Invalid code length {len(code)}, expected {cls.CODE_LENGTH}."
            )
            raise SequenceDecoderError(
                f"Code must be exactly {cls.CODE_LENGTH} characters, "
                f"got {len(code)}."
            )
 
    @classmethod
    def separate_layer(cls, code):
        # In future, multi-layer codes would be split here
        return code
 
    @classmethod
    def segment_code(cls, layer_code):
        # Takes the full 30-char layer code and splits it into 10 segments of 3 characters each
 
        segments = [
            layer_code[i:i + cls.SEGMENT_LENGTH]
            for i in range(0, cls.CODE_LENGTH, cls.SEGMENT_LENGTH)
        ]
 
        return segments
 
    @classmethod
    def map_segments_to_fields(cls, segments):
        # Takes the list of 10 segments and maps each one to its field name using the FIELD_NAMES dictionary
 
        field_map = {}
 
        for index, segment in enumerate(segments):
 
            field_name = cls.FIELD_NAMES.get(index)
 
            if field_name is None:
                logger.error(f"Unknown segment index: {index}")
                raise SequenceDecoderError(
                    f"Unknown segment at index {index}."
                )
 
            field_map[field_name] = segment
 
        return field_map
 
    @classmethod
    def lookup_value(cls, field, segment, config):
        # Look up segment value from config table
 
        field_config = config.get(field, {})

        match field_config:
            case 'DECIMAL':
                return float(segment) / 1000.0
            case 'PERCENT_TENTHS':
                return float(segment) / 10.0
            case 'INTEGER':
                return int(segment)
            case _:

                value = field_config.get(segment)
        
                if value is None:
                    logger.error(f"Unknown segment '{segment}' for field '{field}'.")
                    raise SequenceDecoderError(
                        f"Unknown segment '{segment}' for field '{field}'."
                    )
        
                return value
 
    @classmethod
    def build_decoded_dict(cls, field_map, config):
        # Decoded dict per layer method
 
        decoded = {}
 
        for field, segment in field_map.items():
            decoded[field] = cls.lookup_value(field, segment, config)
 
        return decoded
