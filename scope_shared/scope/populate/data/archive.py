# Allow typing to forward reference
# TODO: Not necessary with Python 3.11
from __future__ import annotations

import scope.database.document_utils as document_utils

import copy
import json
from pathlib import Path
import pyzipper
from typing import Dict, List, Optional, Tuple, Union


class Archive:
    # Entries contained in this archive
    _entries: Dict[Path, dict]

    def __init__(
        self,
        entries: Dict[Path, dict],
    ):
        self._entries = entries

    @classmethod
    def read_archive(
        cls,
        *,
        archive_path: Path,
        password: str,
    ) -> Archive:
        """
        Read an archive from an encrypted zipfile.
        """

        if not archive_path.is_file():
            raise ValueError("Archive does not exist")

        # Open the file
        with open(
            archive_path,
            mode="rb",
        ) as archive_file:
            # Process it as an encrypted zipfile
            with pyzipper.AESZipFile(
                archive_file,
                "r",
                compression=pyzipper.ZIP_LZMA,
                encryption=pyzipper.WZ_AES,
            ) as archive_zipfile:
                # Set the zipfile password
                archive_zipfile.setpassword(password.encode("utf-8"))

                # Confirm the zipfile is valid
                if archive_zipfile.testzip():
                    raise ValueError("Invalid archive or password")

                # Load the entries, each item in the zipfile is a document
                entries: Dict[Path, dict] = {}
                for info_current in archive_zipfile.infolist():
                    document_bytes = archive_zipfile.read(info_current)
                    document_string = document_bytes.decode("utf-8")
                    document_current = json.loads(document_string)
                    document_normalized = document_utils.normalize_document(
                        document=document_current
                    )

                    entries[Path(info_current.filename)] = document_normalized

                # Create and return the archive
                return Archive(entries=entries)

    @classmethod
    def write_archive(
        cls,
        *,
        archive: Archive,
        archive_path: Path,
        password: str,
    ) -> None:
        """
        Write an archive to an encrypted zipfile.
        """

        if archive_path.exists():
            raise ValueError("Archive already exists")

        # Ensure archive directory exists
        if archive_path.parent:
            archive_path.parent.mkdir(parents=True, exist_ok=True)

        # The export is stored in a single zip file
        with open(
            archive_path,
            mode="xb",
        ) as archive_file:
            with pyzipper.AESZipFile(
                archive_file,
                "w",
                compression=pyzipper.ZIP_LZMA,
                encryption=pyzipper.WZ_AES,
            ) as archive_zipfile:
                # Set the password
                archive_zipfile.setpassword(password.encode("utf-8"))

                # Write each entry
                for (path_current, document_current) in archive.entries.items():
                    document_normalized = document_utils.normalize_document(
                        document=document_current
                    )
                    document_string = json.dumps(
                        document_normalized,
                        indent=2,
                    )
                    document_bytes = document_string.encode("utf-8")

                    archive_zipfile.writestr(
                        str(path_current),
                        data=document_bytes,
                    )

    @staticmethod
    def collapse_document_revisions(
        *,
        documents: List[dict],
    ) -> List[dict]:
        """
        Remove all documents that have been replaced by a more recent revision.
        """
        grouped_documents = Archive.group_document_revisions(documents=documents)

        # Each group contains all revisions of a specific document, keep only the most recent version
        collapsed_documents: List[dict] = []
        for (group_key_current, group_current) in grouped_documents.items():
            document_most_recent = None
            for document_current in group_current:
                if (document_most_recent is None) or (
                    document_current["_rev"] > document_most_recent["_rev"]
                ):
                    document_most_recent = document_current

            collapsed_documents.append(document_most_recent)

        return collapsed_documents

    @staticmethod
    def collapse_entry_revisions(
        *,
        entries: Dict[Path, dict],
    ) -> Dict[Path, dict]:
        """
        Remove all entries that have been replaced by a more recent revision.
        """
        grouped_entries = Archive.group_entry_revisions(entries=entries)

        # Each group contains all revisions of a specific document, keep only the most recent version
        collapsed_entries: Dict[Path, dict] = {}
        for (group_key_current, group_current) in grouped_entries.items():
            key_most_recent = None
            document_most_recent = None
            for (key_current, document_current) in group_current.entries():
                if (document_most_recent is None) or (
                    document_current["_rev"] > document_most_recent["_rev"]
                ):
                    key_most_recent = key_current
                    document_most_recent = document_current

            collapsed_entries[key_most_recent] = document_most_recent

        return collapsed_entries

    def collection_documents(
        self,
        *,
        collection: str,
        ignore_sentinel: bool,
    ) -> List[dict]:
        """
        Obtain all documents in a specified collection.
        """

        return list(
            self.collection_entries(
                collection=collection,
                ignore_sentinel=ignore_sentinel,
            ).values()
        )

    def collection_entries(
        self,
        *,
        collection: str,
        ignore_sentinel: bool,
    ) -> Dict[Path, dict]:
        """
        Obtain all entries in a specified collection.
        """

        # Filter to entries in this collection
        collection_entries = {}
        for (key_current, document_current) in self.entries.items():
            parents_current = [
                str(parent_current)
                for parent_current in key_current.parents
                if str(parent_current) not in ["."]
            ]

            if collection in parents_current:
                collection_entries[key_current] = document_current

        # If there is a sentinel to ignore, do that
        if ignore_sentinel:
            collection_entries = {
                key_current: document_current
                for (key_current, document_current) in collection_entries.items()
                if document_current["_type"] != "sentinel"
            }

        return collection_entries

    @property
    def entries(self) -> Dict[Path, dict]:
        """
        All entries in the archive.

        Always returns a deepcopy, so all uses of this property are independent.
        """

        return copy.deepcopy(self._entries)

    @staticmethod
    def group_document_revisions(
        *,
        documents: List[dict],
    ) -> Dict[Union[Tuple[str], Tuple[str, str]], List[dict]]:
        """
        Group documents according to a tuple created from
        - document "_type"
        - any document "_set_id"
        """
        grouped_documents: Dict[Union[Tuple[str], Tuple[str, str]], List[dict]] = {}
        for document_current in documents:
            # Singletons have only a _type, while set elements also have a _set_id
            group_key_current = document_current["_type"]
            if "_set_id" in document_current:
                group_key_current = (
                    document_current["_type"],
                    document_current["_set_id"],
                )

            # Ensure we have a group for this key
            if group_key_current not in grouped_documents:
                grouped_documents[group_key_current] = []

            # Add entry to its group
            grouped_documents[group_key_current].append(document_current)

        return grouped_documents

    @staticmethod
    def group_entry_revisions(
        *,
        entries: Dict[Path, dict],
    ) -> Dict[Union[Tuple[str], Tuple[str, str]], Dict[Path, dict]]:
        """
        Group entries according to a tuple created from
        - document "_type"
        - any document "_set_id"
        """
        grouped_entries: Dict[Union[Tuple[str], Tuple[str, str]], Dict[Path, dict]] = {}
        for (key_current, document_current) in entries.items():
            # Singletons have only a _type, while set elements also have a _set_id
            group_key_current = document_current["_type"]
            if "_set_id" in document_current:
                group_key_current = (
                    document_current["_type"],
                    document_current["_set_id"],
                )

            # Ensure we have a group for this key
            if group_key_current not in grouped_entries:
                grouped_entries[group_key_current] = {}

            # Add entry to its group
            grouped_entries[group_key_current][key_current] = document_current

        return grouped_entries

    def patients_documents(
        self,
        *,
        ignore_sentinel: bool,
        collapsed: bool,
    ) -> List[dict]:
        documents = self.collection_documents(
            collection="patients",
            ignore_sentinel=ignore_sentinel,
        )

        if collapsed:
            documents = Archive.collapse_document_revisions(documents=documents)

        return documents

    def providers_documents(
        self,
        *,
        ignore_sentinel: bool,
        collapsed: bool,
    ) -> List[dict]:
        documents = self.collection_documents(
            collection="providers",
            ignore_sentinel=ignore_sentinel,
        )

        if collapsed:
            documents = Archive.collapse_document_revisions(documents=documents)

        return documents
