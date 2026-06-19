"""Download functionality for SNOMED-CT."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pystow
from pystow.utils import name_from_url

from umls_downloader import download_tgt

__all__ = [
    "download_snomed_international",
    "download_snomed_us",
]

# TODO add versioning

MODULE = pystow.module("bio", "snomed")
SNOMED_CT_US = (
    "https://download.nlm.nih.gov/mlb/utsauth/USExt/"
    "SnomedCT_USEditionRF2_PRODUCTION_20220301T120000Z.zip"
)
SNOMED_CT_INT = (
    "https://download.nlm.nih.gov/umls/kss/"
    "IHTSDO2022/IHTSDO20220630/SnomedCT_InternationalRF2_PRODUCTION_20220630T120000Z.zip"
)


def download_snomed_us(**kwargs: Any) -> Path:
    """Download the SNOMED-CT United States version."""
    return _download_snomed_helper(url=SNOMED_CT_US, **kwargs)


def download_snomed_international(**kwargs: Any) -> Path:
    """Download the SNOMED-CT international version."""
    return _download_snomed_helper(url=SNOMED_CT_INT, **kwargs)


def _download_snomed_helper(url: str, *, api_key: str | None = None, force: bool = False) -> Path:
    path = MODULE.join(name=name_from_url(url))
    if path.is_file() and not force:
        return path
    download_tgt(url, path, api_key=api_key)
    return path
