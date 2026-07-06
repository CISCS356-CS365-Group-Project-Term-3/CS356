import pytest
from unittest.mock import MagicMock, patch

import infra_management as app

from models.api_models import (
    NameIdCreate,
    NameIdUpdate,
    CodecCreate,
    CodecUpdate,
    VideoFileCreate,
    VideoFileUpdate,
    SequenceCreate,
    SequenceUpdate,
    TransmissionConditionCreate,
    TransmissionConditionUpdate
)


class TestRequest:
    def __init__(self, method, json=None):
        self.method = method
        self.json = json or {}


class TestTable:
    id = MagicMock()


class TestRow:
    def __init__(self, id=1):
        self.id = id
        self.active = False


@pytest.fixture
def session_mock():
    with patch("infra_management.Session") as mock:
        session = MagicMock()
        mock.return_value.__enter__.return_value = session
        yield session


@pytest.fixture
def codec_create_payload():
    return {
        "name": "h264",
        "active": 1
    }


@pytest.fixture
def video_create_payload():
    return {
        "sequence_id": "1",
        "name": "video",
        "filepath": "/tmp/a.mp4",
        "spacial": [1, 2],
        "temporal": 10,
        "depth": 8,
        "quality": "high",
        "gamut": "srgb",
        "active": 1
    }


@pytest.fixture
def video_update_payload():
    return {
        "id": 1,
        "sequence_id": "1",
        "name": "video",
        "filepath": "/tmp/a.mp4",
        "spacial": [1, 2],
        "temporal": 10,
        "depth": 8,
        "quality": "high",
        "gamut": "srgb",
        "active": 1
    }


@pytest.fixture
def sequence_create_payload():
    return {
        "name": "seq",
        "description": "desc",
        "active": 1,
        "version": 1.0
    }


@pytest.fixture
def sequence_update_payload():
    return {
        "id": 1,
        "name": "seq",
        "description": "desc",
        "active": 1
    }


@pytest.fixture
def transmission_create_payload():
    return {
        "name": "tc",
        "lower_bound": 1,
        "upper_bound": 10,
        "active": 1,
        "unit": "ms"
    }


@pytest.fixture
def transmission_update_payload():
    return {
        "id": 1,
        "name": "tc",
        "lower_bound": 1,
        "upper_bound": 10,
        "active": 1
    }


# tests POST update + validate + commit for NameId model
def test_standard_crud_post_nameid_success(session_mock):

    row = TestRow()
    session_mock.query.return_value.filter.return_value.all.return_value = [row]

    request = TestRequest("POST", {"id": 1, "name": "x", "active": 1})

    result = app.standard_crud(
        request,
        TestTable,
        MagicMock(return_value=row),
        None,
        NameIdUpdate,
        NameIdCreate,
    )

    assert result["status"] is True


# tests PUT create for NameId model
def test_standard_crud_put_nameid_success(session_mock):

    row = TestRow()

    creator = MagicMock(return_value=row)

    request = TestRequest(
        "PUT",
        {"name": "x", "active": 1}
    )

    result = app.standard_crud(
        request,
        TestTable,
        None,
        creator,
        NameIdUpdate,
        NameIdCreate,
    )

    assert result["status"] is True


# tests Codec create (PUT path)
def test_codec_create_success(session_mock, codec_create_payload):

    row = TestRow()
    creator = MagicMock(return_value=row)

    request = TestRequest("PUT", codec_create_payload)

    result = app.standard_crud(
        request,
        TestTable,
        None,
        creator,
        CodecUpdate,
        CodecCreate,
    )

    assert result["status"] is True


# tests Codec update (POST path with validation + update)
def test_codec_update_success(session_mock):

    row = TestRow()
    row.id = 1

    session_mock.query.return_value.filter.return_value.all.return_value = [row]

    request = TestRequest(
        "POST",
        {
            "id": 1,
            "name": "h264",
            "active": 1,
            "version": "1.0"
        }
    )

    updater = MagicMock(return_value=row)

    result = app.standard_crud(
        request,
        TestTable,
        updater,
        None,
        CodecUpdate,
        CodecCreate,
    )

    updater.assert_called_once_with(row, request.json)

    session_mock.commit.assert_called_once()

    assert result["status"] is True


# tests VideoFile create (PUT path)
def test_video_create_success(session_mock, video_create_payload):

    row = TestRow()
    creator = MagicMock(return_value=row)

    request = TestRequest("PUT", video_create_payload)

    result = app.standard_crud(
        request,
        TestTable,
        None,
        creator,
        VideoFileUpdate,
        VideoFileCreate,
    )

    assert result["status"] is True


# tests VideoFile update (POST path)
def test_video_update_success(session_mock, video_update_payload):

    row = TestRow()

    session_mock.query.return_value.filter.return_value.all.return_value = [row]

    request = TestRequest("POST", video_update_payload)

    result = app.standard_crud(
        request,
        TestTable,
        MagicMock(return_value=row),
        None,
        VideoFileUpdate,
        VideoFileCreate,
    )

    assert result["status"] is True


# tests Sequence create (PUT path)
def test_sequence_create_success(session_mock, sequence_create_payload):

    row = TestRow()
    creator = MagicMock(return_value=row)

    request = TestRequest("PUT", sequence_create_payload)

    result = app.standard_crud(
        request,
        TestTable,
        None,
        creator,
        SequenceUpdate,
        SequenceCreate,
    )

    assert result["status"] is True


# tests Sequence update (POST path)
def test_sequence_update_success(session_mock, sequence_update_payload):

    row = TestRow()

    session_mock.query.return_value.filter.return_value.all.return_value = [row]

    request = TestRequest("POST", sequence_update_payload)

    result = app.standard_crud(
        request,
        TestTable,
        MagicMock(return_value=row),
        None,
        SequenceUpdate,
        SequenceCreate,
    )

    assert result["status"] is True


# tests TransmissionCondition create (PUT path)
def test_transmission_create_success(session_mock, transmission_create_payload):

    row = TestRow()
    creator = MagicMock(return_value=row)

    request = TestRequest("PUT", transmission_create_payload)

    result = app.standard_crud(
        request,
        TestTable,
        None,
        creator,
        TransmissionConditionUpdate,
        TransmissionConditionCreate,
    )

    assert result["status"] is True


# tests TransmissionCondition update (POST path)
def test_transmission_update_success(session_mock, transmission_update_payload):

    row = TestRow()

    session_mock.query.return_value.filter.return_value.all.return_value = [row]

    request = TestRequest("POST", transmission_update_payload)

    result = app.standard_crud(
        request,
        TestTable,
        MagicMock(return_value=row),
        None,
        TransmissionConditionUpdate,
        TransmissionConditionCreate,
    )

    assert result["status"] is True


# tests activate endpoint updates active flag
def test_standard_activate_success(session_mock):

    row = TestRow()

    session_mock.query.return_value.filter.return_value.all.return_value = [row]

    request = TestRequest("POST", {"id": 1, "active": 1})

    result = app.standard_activate(
        request,
        TestTable,
    )

    assert row.active == 1
    assert result["status"] is True


# tests UI options endpoint returns structured dictionary
@patch("infra_management.Session")
def test_get_ui_options_basic(mock_session):

    session = MagicMock()

    mock_session.return_value.__enter__.return_value = session

    session.query.return_value.filter.return_value.all.return_value = []

    result = app.get_ui_options(filter=False)

    assert isinstance(result, dict)
    assert "project_types" in result
    assert "encoder_modes" in result
    assert "codecs" in result
    assert "sequences" in result


# tests mappings endpoint returns codec and file mappings
@patch("infra_management.Session")
def test_get_mappings(mock_session):

    session = MagicMock()

    mock_session.return_value.__enter__.return_value = session

    session.query.return_value.all.return_value = [
        MagicMock(id=1, name="file")
    ]

    result = app.get_mappings()

    assert "raw_file" in result
    assert "codec" in result