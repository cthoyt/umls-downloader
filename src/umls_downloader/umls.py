"""Download content."""

from __future__ import annotations

import csv
import sys
import zipfile
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path
from typing import BinaryIO, TextIO

from pystow.utils import Reader, Representation, open_zip_dict_reader, open_zip_reader, open_zipfile

from .api import download_tgt_versioned

__all__ = [
    "download_umls",
    "download_umls_full",
    "download_umls_metathesaurus",
    "open_mrconso_dict_reader",
    "open_mrconso_reader",
    "open_umls",
    "open_umls_full",
    "open_umls_hierarchy",
    "open_umls_semantic_types",
]

UMLS_URL_FMT = "https://download.nlm.nih.gov/umls/kss/{version}/umls-{version}-mrconso.zip"
UMLS_METATHESAURUS_URL_FMT = (
    "https://download.nlm.nih.gov/umls/kss/{version}/umls-{version}-metathesaurus.zip"
)
UMLS_METATHESAURUS_FULL_FMT = (
    "https://download.nlm.nih.gov/umls/kss/{version}/umls-{version}-metathesaurus-full.zip"
)


def _download_umls(
    url_fmt: str,
    version: str | None = None,
    *,
    api_key: str | None = None,
    force: bool = False,
) -> Path:
    return download_tgt_versioned(
        url_fmt=url_fmt,
        version=version,
        version_key="umls",
        module_key="umls",
        api_key=api_key,
        force=force,
    )


def download_umls(
    version: str | None = None, *, api_key: str | None = None, force: bool = False
) -> Path:
    """Ensure the given version of the UMLS MRCONSO.RRF file.

    :param version: The version of UMLS to ensure. If not given, is looked up with
        :mod:`bioversions`.
    :param api_key: An API key. If not given, is looked up using
        :func:`pystow.get_config` with the ``umls`` module and ``api_key`` key.
    :param force: Should the file be re-downloaded, even if it already exists?

    :returns: The path of the file for the given version of UMLS.
    """
    return _download_umls(url_fmt=UMLS_URL_FMT, version=version, api_key=api_key, force=force)


def download_umls_full(
    version: str | None = None, *, api_key: str | None = None, force: bool = False
) -> Path:
    """Ensure the given version of the UMLS MRSTY.RRF file.

    :param version: The version of UMLS to ensure. If not given, is looked up with
        :mod:`bioversions`.
    :param api_key: An API key. If not given, is looked up using
        :func:`pystow.get_config` with the ``umls`` module and ``api_key`` key.
    :param force: Should the file be re-downloaded, even if it already exists?

    :returns: The path of the file for the given version of UMLS.
    """
    return _download_umls(
        url_fmt=UMLS_METATHESAURUS_FULL_FMT,
        version=version,
        api_key=api_key,
        force=force,
    )


def download_umls_metathesaurus(
    version: str | None = None, *, api_key: str | None = None, force: bool = False
) -> Path:
    """Ensure the given version of the UMLS metathesaurus zip archive.

    :param version: The version of UMLS to ensure. If not given, is looked up with
        :mod:`bioversions`.
    :param api_key: An API key. If not given, is looked up using
        :func:`pystow.get_config` with the ``umls`` module and ``api_key`` key.
    :param force: Should the file be re-downloaded, even if it already exists?

    :returns: The path of the file for the given version of UMLS.
    """
    return _download_umls(
        url_fmt=UMLS_METATHESAURUS_URL_FMT,
        version=version,
        api_key=api_key,
        force=force,
    )


@contextmanager
def open_mrconso_dict_reader(
    version: str | None = None, *, api_key: str | None = None, force: bool = False
) -> Generator[csv.DictReader[str], None, None]:
    """Ensure and open the UMLS MRCONSO.RRF file from the given version as a dictionary reader.

    :param version: The version of UMLS to ensure. If not given, is looked up with
        :mod:`bioversions`.
    :param api_key: An API key. If not given, is looked up using
        :func:`pystow.get_config` with the ``umls`` module and ``api_key`` key.
    :param force: Should the file be re-downloaded, even if it already exists?

    :yields: A dictionary reader
    """
    path = download_umls(version=version, api_key=api_key, force=force)
    inner_path = _find_inner_path(path, "MRCONSO.RRF")
    old_limit = csv.field_size_limit(sys.maxsize)
    with open_zip_dict_reader(
        path, inner_path=inner_path, fieldnames=RRF_COLUMNS, delimiter="|"
    ) as reader:
        yield reader
    csv.field_size_limit(old_limit)


@contextmanager
def open_mrconso_reader(
    version: str | None = None, *, api_key: str | None = None, force: bool = False
) -> Generator[Reader, None, None]:
    """Ensure and open the UMLS MRCONSO.RRF file from the given version.

    :param version: The version of UMLS to ensure. If not given, is looked up with
        :mod:`bioversions`.
    :param api_key: An API key. If not given, is looked up using
        :func:`pystow.get_config` with the ``umls`` module and ``api_key`` key.
    :param force: Should the file be re-downloaded, even if it already exists?

    :yields: The file, which is used in the context manager.
    """
    path = download_umls(version=version, api_key=api_key, force=force)
    inner_path = _find_inner_path(path, "MRCONSO.RRF")
    old_limit = csv.field_size_limit(sys.maxsize)
    with open_zip_reader(path, inner_path=inner_path, operation="read") as reader:
        yield reader
    csv.field_size_limit(old_limit)


RRF_COLUMNS = [
    "CUI",
    "LAT - Language",
    "TS - Term Status",
    "LUI - Local Unique Identifier",
    "STT - String Type",
    "SUI - Unique Identifier for String",
    "ISPREF - is preferred",
    "AUI - Unique atom identifier",
    "SAUI - Source atom identifier",
    "SCUI - Source concept identifier",
    "SDUI - Source descriptor identifier",
    "SAB - source name",
    "TTY - Term Type in Source",
    "CODE",
    "STR",
    "SRL",
    "SUPPRESS",
    "CVF",
    "?",
]


@contextmanager
def open_umls(
    version: str | None = None,
    *,
    api_key: str | None = None,
    force: bool = False,
    representation: Representation = "binary",
) -> Generator[TextIO, None, None] | Generator[BinaryIO, None, None]:
    """Ensure and open the UMLS MRCONSO.RRF file from the given version.

    :param version: The version of UMLS to ensure. If not given, is looked up with
        :mod:`bioversions`.
    :param api_key: An API key. If not given, is looked up using
        :func:`pystow.get_config` with the ``umls`` module and ``api_key`` key.
    :param force: Should the file be re-downloaded, even if it already exists?
    :param representation: The representation to use, either "binary" or "text".
        Defaults to "binary" for backwards compatibility, but is much more
        convenient when using "text".

    :yields: The file, which is used in the context manager.
    """
    path = download_umls(version=version, api_key=api_key, force=force)
    inner_path = _find_inner_path(path, "MRCONSO.RRF")
    with open_zipfile(path, inner_path, operation="read", representation=representation) as file:
        yield file


@contextmanager
def open_umls_full(
    name: str,
    version: str | None = None,
    *,
    api_key: str | None = None,
    force: bool = False,
) -> Generator[BinaryIO, None, None]:
    """Ensure and open a UMLS file from the given version.

    :param name: The name of the file, like ``MRSTY.RRF``
    :param version: The version of UMLS to ensure. If not given, is looked up with
        :mod:`bioversions`.
    :param api_key: An API key. If not given, is looked up using
        :func:`pystow.get_config` with the ``umls`` module and ``api_key`` key.
    :param force: Should the file be re-downloaded, even if it already exists?

    :yields: The file, which is used in the context manager.
    """
    path = download_umls_full(version=version, api_key=api_key, force=force)
    # In the 2023AB release, they added an intermediate META directory,
    # which means we have to go searching for the file by name
    inner_path = _find_inner_path(path, name)
    with open_zipfile(path, inner_path=inner_path, representation="binary") as file:
        yield file


def _find_inner_path(path: Path, name: str) -> str:
    with zipfile.ZipFile(path) as zip_file:
        return next(
            zip_info.filename for zip_info in zip_file.infolist() if name in zip_info.filename
        )


@contextmanager
def open_umls_semantic_types(
    version: str | None = None, *, api_key: str | None = None, force: bool = False
) -> Generator[BinaryIO, None, None]:
    """Ensure and open a UMLS file from the given version.

    :param version: The version of UMLS to ensure. If not given, is looked up with
        :mod:`bioversions`.
    :param api_key: An API key. If not given, is looked up using
        :func:`pystow.get_config` with the ``umls`` module and ``api_key`` key.
    :param force: Should the file be re-downloaded, even if it already exists?

    :yields: The file, which is used in the context manager.

    This file contains the following columns:

    ==== ========================================================================
    CUI  Unique identifier of concept
    TUI  Unique identifier of Semantic Type
    STN  Semantic Type tree number
    STY  Semantic Type. The valid values are defined in the Semantic Network.
    ATUI Unique identifier for attribute
    CVF  Content View Flag. Bit field used to flag rows included in Content View.
    ==== ========================================================================

    .. seealso::

        https://www.ncbi.nlm.nih.gov/books/NBK9685/table/ch03.Tf/
    """
    with open_umls_full(name="MRSTY.RRF", version=version, api_key=api_key, force=force) as file:
        yield file


@contextmanager
def open_umls_hierarchy(
    version: str | None = None, *, api_key: str | None = None, force: bool = False
) -> Generator[BinaryIO, None, None]:
    """Ensure and open a UMLS file from the given version.

    :param version: The version of UMLS to ensure. If not given, is looked up with
        :mod:`bioversions`.
    :param api_key: An API key. If not given, is looked up using
        :func:`pystow.get_config` with the ``umls`` module and ``api_key`` key.
    :param force: Should the file be re-downloaded, even if it already exists?

    :yields: The file, which is used in the context manager.

    This file contains the following columns:

    ==== ==========================================================================
    CUI  Unique identifier of concept
    AUI  Unique identifier of atom - variable length field, 8 or 9 characters
    CXN  Context number (e.g., 1, 2, 3)
    PAUI Unique identifier of atom's immediate parent within this context
    SAB  Abbreviated source name (SAB) of the source of atom
    RELA Relationship of atom to its immediate parent
    PTR  Path to the top or root of the hierarchical context from this atom.
    HCD  Source asserted hierarchical number or code for this atom in this context.
    CVF  Content View Flag. Bit field used to flag rows included in Content View.
    ==== ==========================================================================

    .. seealso::

        https://www.ncbi.nlm.nih.gov/books/NBK9685/table/ch03.T.computable_hierarchies_file_mrhie
    """
    with open_umls_full(name="MRHIER.RRF", version=version, api_key=api_key, force=force) as file:
        yield file
