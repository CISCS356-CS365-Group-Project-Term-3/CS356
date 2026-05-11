# This class decodes sequence codes into encoding parameters.


class SequenceDecoder:

    # Stores field mapping information
    FIELD_POSITIONS = {}

    # Stores field names
    FIELD_NAMES = {}

    # Stores default values
    DEFAULTS = {}

    def decode(self, code, config):

        # Main decoding function

        # Validate sequence code
        if not self.validate_code(code):
            return None

        # Split sequence into layers
        layers = self.split_layers(code)

        decoded_values = {}

        # Decode each layer
        for layer in layers:

            layer_values = self.decode_layer(
                layer,
                config
            )

            decoded_values.update(layer_values)

        # Apply default values
        decoded_values = self.resolve_defaults(
            decoded_values
        )

        return decoded_values

    def split_layers(self, code):

        # Splits layered sequence code

        return code.split("_")

    def decode_layer(self, layer_code, config):

        # Decodes one layer of sequence code

        decoded_layer = {}

        # Example decoding process
        for field, positions in self.FIELD_POSITIONS.items():

            start = positions[0]
            end = positions[1]

            segment = self.extract_field(
                layer_code,
                start,
                end
            )

            value = self.resolve_value(
                field,
                segment,
                config
            )

            decoded_layer[field] = value

        return decoded_layer

    def extract_field(self, code, start, end):

        # Extracts section from sequence code

        return code[start:end]

    def resolve_value(self, field, segment, config):

        # Resolves encoded value
        # using config mappings

        return config.get(field, {}).get(segment)

    def resolve_defaults(self, values):

        # Applies defaults for missing values

        for field, default in self.DEFAULTS.items():

            if field not in values:
                values[field] = default

        return values

    def validate_code(self, code):

        # Validates sequence code format

        return len(code) > 0