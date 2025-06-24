"""import pytest

# from unittest import mock
from unittest.mock import MagicMock, patch
from pathlib import Path
from docx import Document
from core.document_processor import DocumentProcessor, MARKERS


@pytest.fixture
def processor():
    return DocumentProcessor()


def test_replace_in_paragraph(processor):
    paragraph = MagicMock()
    paragraph.text = "Hello [NAME]!"
    paragraph.runs = [MagicMock()]

    processor._replace_in_paragraph(paragraph, "[NAME]", "John")

    assert paragraph.runs[0].text == "Hello John!"


def test_check_assets(processor):
    asset_list = {"assets": [{"category": "Laptops"}, {"category": "Smartphones"}]}
    accessories = [
        {"category": {"name": "Charger"}},
        {"category": {"name": "Mouses"}},
        {"category": {"name": "Keyboards"}},
        {"category": {"name": "Monitors"}},
        {"category": {"name": "Headsets"}},
        {"category": {"name": "SIM Card"}},
    ]

    result = processor._check_assets(asset_list, accessories)

    assert result == {
        "has_laptop": True,
        "has_smartphone": True,
        "has_monitor": True,
        "has_mouse": True,
        "has_keyboard": True,
        "has_charger": True,
        "has_headset": True,
        "has_simcard": True,
    }


def test_process_assets_type(processor):
    paragraph = MagicMock()
    paragraph.text = MARKERS["HAS_SIMCARD"] + " " + MARKERS["SIMCARD_MODEL"]
    paragraph.runs = [MagicMock()]

    item = {"model": "Chip VIVO"}

    processor._process_assets_type(
        paragraph,
        has_asset=True,
        presence_marker=MARKERS["HAS_SIMCARD"],
        description_marker=MARKERS["SIMCARD_MODEL"],
        item=item,
    )
    print(MARKERS["HAS_SIMCARD"])
    assert paragraph.runs[0].text == "X Chip VIVO"


@patch(
    "core.document_processor.LAPTOP_TEMPLATE_PATH", Path("fake_laptop_template.docx")
)
@patch(
    "core.document_processor.SMARTPHONE_TEMPLATE_PATH",
    Path("fake_smartphone_template.docx"),
)
def test_load_template_laptop(monkeypatch, processor):
    monkeypatch.setattr(Document, "save", MagicMock())

    with patch.object(Path, "exists", return_value=True):
        with patch("docx.Document", return_value=MagicMock()):
            processor.load_template("Laptops")
            assert processor.document is not None


@patch("core.document_processor.LAPTOP_TEMPLATE_PATH", Path("missing_template.docx"))
def test_load_template_missing(monkeypatch, processor):
    with patch.object(Path, "exists", return_value=False):
        with pytest.raises(FileNotFoundError):
            processor.load_template("Laptops")


@patch("core.document_processor.snipeit_client.accessories_api_call")
@patch("core.document_processor.snipeit_client.specific_accessory_api_call")
def test_process_assets(
    mock_specific_accessory_api_call, mock_accessories_api_call, processor
):
    processor.document = MagicMock()
    processor.document.paragraphs = [MagicMock(text="[NAME]", runs=[MagicMock()])]

    asset_list = {
        "user_id": "1",
        "user_name": "John Doe",
        "employee_number": "1234",
        "assets": [{"category": "Laptops"}],
    }

    selected_asset = {
        "model": "Dell",
        "asset_tag": "ABC-1234",
        "serial": "XYZ",
        "category": "Laptops",
        "asset_id": "1",
    }

    mock_accessories_api_call.return_value = [
        {
            "category": {"name": "Mouses"},
            "model": "Logitech",
            "asset_tag": "5678",
            "serial": "DEF",
        }
    ]
    mock_specific_accessory_api_call.return_value = []

    processor.process_assets(asset_list, selected_asset)

    assert processor.document is not None
    assert mock_accessories_api_call.called


@patch("core.document_processor.OUTPUT_DIR", "./output")
def test_save(monkeypatch, processor):
    processor.document = MagicMock()
    monkeypatch.setattr(Document, "save", MagicMock())

    output_path = processor.save(
        username="John Doe", asset_tag="ABC-1234", type_of_term="Laptops"
    )

    assert output_path.name == "1234 - Termo Laptops - John Doe.docx"


def test_save_no_document(processor):
    processor.document = None

    with pytest.raises(ValueError):
        processor.save("John", "ABC-1234", "Laptops")
"""
