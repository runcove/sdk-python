import pathlib
import re

import cove_sdk

SPEC = pathlib.Path(__file__).parents[2] / "openapi.yaml"


def _info_version(text: str) -> int:
    block = re.search(r"^info:\n((?:[ ].*\n|\n)*)", text, re.M)
    assert block, "no top-level info: block"
    m = re.search(r"^  version: ['\"]?(\d+)['\"]?$", block.group(1), re.M)
    assert m, "info.version not found"
    return int(m.group(1))


def test_unit_api_version_matches_the_contract() -> None:
    assert cove_sdk.API_VERSION == _info_version(SPEC.read_text())
