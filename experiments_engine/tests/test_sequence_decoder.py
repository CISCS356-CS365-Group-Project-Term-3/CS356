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
        'raw_file': {'000': 'Beauty', '001': 'Bosphorus', '003': 'HoneyBee', '005': 'Jockey'},
        'encoder_type': {'000': 'standard', '001': 'scalable'},
        'codec': {'000': 'AVC', '001': 'SVC', '002': 'HEVC', '003': 'SHVC'},
        'encoder_mode': {'000': 'random_access', '001': 'low_delay', '002': 'intra_only'},
        'loss': 'DECIMAL',  # 001 = 0.1%, 010 = 1%, 100 = 10%
        'delay': 'INTEGER',  # 080 = 80ms, 100 = 100ms
    }
 
 
def test_segment_code_splits_into_segments(decoder):
    # A valid code should produce the correct number of segments
    segments = decoder.segment_code('005001003000001000')
    assert len(segments) == 6
 
 
def test_segment_code_each_segment_is_3_chars(decoder):
    # Every segment must be exactly 3 characters long
    segments = decoder.segment_code('005001003000001000')
    assert all(len(s) == 3 for s in segments)
 
 
def test_segment_code_correct_values(decoder):
    # Check that specific positions contain the expected 3-char values
    segments = decoder.segment_code('005001003000001000')
    assert segments[0] == '005'
    assert segments[1] == '001'
    assert segments[5] == '000'
 
 
def test_map_segments_to_fields(decoder):
    # Segments should be mapped to the right field name
    segments = ['005', '001', '003', '000', '001', '080']
    result = decoder.map_segments_to_fields(segments)
 
    assert result['raw_file'] == '005'
    assert result['encoder_type'] == '001'
    assert result['codec'] == '003'
    assert result['encoder_mode'] == '000'
    assert result['loss'] == '001'
    assert result['delay'] == '080'
 

def test_lookup_value_returns_correct_value(decoder, config):
    # "003" under "codec" should return "SHVC" from the config
    value = decoder.lookup_value('codec', '003', config)
    assert value == 'SHVC'
 
 
def test_lookup_value_unknown_segment_raises_error(decoder, config):
    # "999" is not in the config for codec, so it should raise an error
    with pytest.raises(SequenceDecoderError):
        decoder.lookup_value('codec', '999', config)
 
 
def test_decode_valid_code(decoder, config):
    # Full decode of a valid 18-char code
    result = decoder.decode('005001003000001080', config)
 
    assert result['raw_file'] == 'Jockey'
    assert result['encoder_type'] == 'scalable'
    assert result['codec'] == 'SHVC'
    assert result['encoder_mode'] == 'random_access'
    assert result['loss'] == 0.001  # 001 = 0.1% loss
    assert result['delay'] == 80  # 080 = 80ms
 
 
def test_decode_second_sequence(decoder, config):
    # Decode a standard AVC encoder, different settings
    result = decoder.decode('001000000000010100', config)
 
    assert result['raw_file'] == 'Bosphorus'
    assert result['encoder_type'] == 'standard'
    assert result['codec'] == 'AVC'
    assert result['encoder_mode'] == 'random_access'
    assert result['loss'] == 0.01  # 010 = 1% loss
    assert result['delay'] == 100  # 100 = 100ms
 

def test_invalid_length_raises_error(decoder, config):
    # Code is too short (not 18 chars), should raise an error
    with pytest.raises(SequenceDecoderError):
        decoder.decode('tooshort', config)
 
 
def test_too_long_raises_error(decoder, config):
    # Code is too long (not 18 chars), should raise an error
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
 