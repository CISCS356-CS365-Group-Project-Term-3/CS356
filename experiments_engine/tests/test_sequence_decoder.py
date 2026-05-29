import pytest
from experiments_engine.sequence_decoder import SequenceDecoder, SequenceDecoderError
  
@pytest.fixture
def decoder():
    # Creates a fresh SequenceDecoder instance for each test
    return SequenceDecoder()
 
 
@pytest.fixture
def config():
    # A sample config lookup table 
    return {
        'encoder_type': {'000': 'standard', '001': 'scalable'},
        'codec': {'000': 'AVC', '001': 'SVC', '002': 'HEVC', '003': 'SHVC'},
        'encoder_mode': {'000': 'random_access', '001': 'low_delay', '002': 'intra_only'},
        'spatial': {'011': 'HD720', '012': 'HD1080', '014': 'UHD'},
        'temporal': {'005': '30fps', '006': '60fps', '007': '120fps'},
        'qp': {'005': 'Q25', '007': 'Q27', '012': 'Q32'},
        'scalability_type': {'000': 'spatial', '001': 'temporal', '002': 'quality'},
        'bit_depth': {'000': '8bit', '001': '10bit'},
        'reserved': {'000': 'none'},
        'raw_file': {'000': 'Beauty', '001': 'Bosphorus', '003': 'HoneyBee', '005': 'Jockey'},
    }
 
 
def test_segment_code_splits_into_10_segments(decoder):
    # A valid 30-char code should produce exactly 10 segments
    segments = decoder.segment_code('001003000012005007000000000003')
    assert len(segments) == 10
 
 
def test_segment_code_each_segment_is_3_chars(decoder):
    # Every segment must be exactly 3 characters long
    segments = decoder.segment_code('001003000012005007000000000003')
    assert all(len(s) == 3 for s in segments)
 
 
def test_segment_code_correct_values(decoder):
    # Check that specific positions contain the expected 3-char values
    segments = decoder.segment_code('001003000012005007000000000003')
    assert segments[0] == '001'
    assert segments[3] == '012'
    assert segments[9] == '003'
 
 
def test_map_segments_to_fields(decoder):
    # Segments should be mapped to the right field name
    segments = ['001', '003', '000', '012', '005', '007', '000', '000', '000', '003']
    result = decoder.map_segments_to_fields(segments)
 
    assert result['encoder_type'] == '001'
    assert result['codec'] == '003'
    assert result['encoder_mode'] == '000'
    assert result['spatial'] == '012'
    assert result['raw_file'] == '003'
 

def test_lookup_value_returns_correct_value(decoder, config):
    # "003" under "codec" should return "SHVC" from the config
    value = decoder.lookup_value('codec', '003', config)
    assert value == 'SHVC'
 
 
def test_lookup_value_unknown_segment_raises_error(decoder, config):
    # "999" is not in the config for codec, so it should raise an error
    with pytest.raises(SequenceDecoderError):
        decoder.lookup_value('codec', '999', config)
 
 
def test_decode_valid_code(decoder, config):
    # Full decode of a valid 30-char code
    result = decoder.decode('001003000012005007000000000003', config)
 
    assert result['encoder_type'] == 'scalable'
    assert result['codec'] == 'SHVC'
    assert result['encoder_mode'] == 'random_access'
    assert result['spatial'] == 'HD1080'
    assert result['temporal'] == '30fps'
    assert result['qp'] == 'Q27'
    assert result['scalability_type'] == 'spatial'
    assert result['bit_depth'] == '8bit'
    assert result['reserved'] == 'none'
    assert result['raw_file'] == 'HoneyBee'
 
 
def test_decode_second_sequence(decoder, config):
    # Decode a standard AVC encoder, different settings
    result = decoder.decode('000000000012005007000000000001', config)
 
    assert result['encoder_type'] == 'standard'
    assert result['codec'] == 'AVC'
    assert result['encoder_mode'] == 'random_access'
    assert result['spatial'] == 'HD1080'
    assert result['temporal'] == '30fps'
    assert result['qp'] == 'Q27'
    assert result['raw_file'] == 'Bosphorus'
 

def test_invalid_length_raises_error(decoder, config):
    # Code is too short (not 30 chars), should raise an error
    with pytest.raises(SequenceDecoderError):
        decoder.decode('tooshort', config)
 
 
def test_too_long_raises_error(decoder, config):
    # Code is too long (33 chars), should raise an error
    with pytest.raises(SequenceDecoderError):
        decoder.decode('001003000012005007000000000003XXX', config)
 
 
def test_empty_code_raises_error(decoder, config):
    # Empty string is not valid, should raise an error
    with pytest.raises(SequenceDecoderError):
        decoder.decode('', config)
 
 
def test_none_code_raises_error(decoder, config):
    # None is not a string, should raise an error
    with pytest.raises(SequenceDecoderError):
        decoder.decode(None, config)
 