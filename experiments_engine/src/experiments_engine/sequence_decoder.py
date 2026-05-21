import logging
 
# used to log errors and warnings during decoding
logger = logging.getLogger(__name__)
 
 
# Custom exception class for sequence decoding errors
class SequenceDecoderError(Exception):
    pass
 
 
# SequenceDecoder takes a 30-character sequence code and decodes it
# into a dictionary of encoding parameters.
 
class SequenceDecoder:
 
    SEGMENT_LENGTH = 3
    SEGMENTS_PER_LAYER = 10
    CODE_LENGTH = SEGMENT_LENGTH * SEGMENTS_PER_LAYER  # 30
 
    # This dictionary maps each segment position (0-9) to the field it represents
    FIELD_NAMES = {
        0: "encoder_type",
        1: "codec",
        2: "encoder_mode",
        3: "spatial",
        4: "temporal",
        5: "qp",
        6: "scalability_type",
        7: "bit_depth",
        8: "reserved",
        9: "raw_file",
    }
 
    def decode(self, code, config):
        # Takes the raw 30-char code and a config lookup table.
        # Returns a dictionary of decoded field names to their human-readable values
 
        # Check the code is valid, not empty
        self.validate_code(code)
 
        # Separate the layer, single will return the code as is
        layer_code = self.separate_layer(code)
 
        # Split the 30-char code into 10 segments of 3 chars each
        segments = self.segment_code(layer_code)
 
        # Map each segment to its field name based on position
        field_map = self.map_segments_to_fields(segments)
 
        # Look up each segment in the config to get the decoded values
        decoded = self.build_decoded_dict(field_map, config)
 
        return decoded
 
    def validate_code(self, code):
        # Checks that the code is a non-empty string and is exactly 30 characters.
 
        if not code or not isinstance(code, str):
            logger.error("Invalid code: empty or not a string.")
            raise SequenceDecoderError(
                "Code must be a non-empty string."
            )
 
        if len(code) != self.CODE_LENGTH:
            logger.error(
                f"Invalid code length {len(code)}, expected {self.CODE_LENGTH}."
            )
            raise SequenceDecoderError(
                f"Code must be exactly {self.CODE_LENGTH} characters, "
                f"got {len(code)}."
            )
 
    def separate_layer(self, code):
        # In future, multi-layer codes would be split here
        return code
 
    def segment_code(self, layer_code):
        # Takes the full 30-char layer code and splits it into 10 segments of 3 characters each
 
        segments = [
            layer_code[i:i + self.SEGMENT_LENGTH]
            for i in range(0, self.CODE_LENGTH, self.SEGMENT_LENGTH)
        ]
 
        return segments
 
    def map_segments_to_fields(self, segments):
        # Takes the list of 10 segments and maps each one to its field name using the FIELD_NAMES dictionary
 
        field_map = {}
 
        for index, segment in enumerate(segments):
 
            field_name = self.FIELD_NAMES.get(index)
 
            if field_name is None:
                logger.error(f"Unknown segment index: {index}")
                raise SequenceDecoderError(
                    f"Unknown segment at index {index}."
                )
 
            field_map[field_name] = segment
 
        return field_map
 
    def lookup_value(self, field, segment, config):
        # Look up segment value from config table
 
        field_config = config.get(field, {})
        value = field_config.get(segment)
 
        if value is None:
            logger.error(f"Unknown segment '{segment}' for field '{field}'.")
            raise SequenceDecoderError(
                f"Unknown segment '{segment}' for field '{field}'."
            )
 
        return value
 
    def build_decoded_dict(self, field_map, config):
        # Decoded dict per layer method
 
        decoded = {}
 
        for field, segment in field_map.items():
            decoded[field] = self.lookup_value(field, segment, config)
 
        return decoded