#!/usr/bin/env python3
"""
Author: DartRuffian

Various stringtable related functions
"""

# import sys
import os
import xml.dom
import xml.dom.minidom


class Stringtables:
    """Performs various operations relating to stringtables."""
    @staticmethod
    def supported_languages() -> list[str]:
        # https://community.bistudio.com/wiki/Stringtable.xml#Supported_Languages
        return [
            "English",
            "Czech",
            "French",
            "Spanish",
            "Italian",
            "Polish",
            "Portuguese",
            "Russian",
            "German",
            "Korean",
            "Japanese",
            "Chinese",
            "Chinesesimp",
            "Turkish",
            "Slovak",
            "Ukrainian",
            "Latin",
            "Bulgarian",
            "Hungarian"
        ]

    @staticmethod
    def prettified_language_name(language: str) -> str:
        """Returns a prettified version of a language name"""
        prettified_names: dict[str, str] = {
            "Chinesesimp": "Simplified Chinese"
        }
        return prettified_names.get(language, language)

    @staticmethod
    def is_language_supported(language: str) -> bool:
        """Determines if a given language is supported by Arma 3"""
        return language in Stringtables.supported_languages()

    @staticmethod
    def get_all_languages(project_path: str) -> list[str]:
        """Checks what languages exist in the project."""
        languages: list[str] = []

        for addon in os.listdir(project_path):
            if addon[0] == ".":
                continue

            stringtable_path = os.path.join(
                project_path, addon, "stringtable.xml")
            try:
                xml_doc: xml.dom.minidom.Document = xml.dom.minidom.parse(
                    stringtable_path)
            except:
                continue

            keys = xml_doc.getElementsByTagName("Key")
            for key in keys:
                for child in key.childNodes:
                    try:
                        if not child.tagName in languages:  # type: ignore
                            languages.append(child.tagName)  # type: ignore
                    except:
                        continue

        return languages

    @staticmethod
    def check_missing_translations(project_path: str, addon: str, languages: list[str]) -> tuple[dict[str, int], set[str]]:
        """Checks a given addon and returns a dictionary of languages and the number of missing keys for that language, and a set of all translaton keys missing translations for any of the given language."""

        try:
            xml_doc = xml.dom.minidom.parse(os.path.join(
                project_path, addon, "stringtable.xml"))
        except:
            return {}, set()

        keys_missing_translations: set[str] = set()
        missing_key_counts: dict[str, int] = {}
        keys = xml_doc.getElementsByTagName("Key")

        for key in keys:
            translation_key = key.getAttribute("ID")
            # Filter out things like text codes for new lines
            current_translations = [
                node.tagName for node in key.childNodes if node.nodeType == xml.dom.Node.ELEMENT_NODE]

            for language in languages:
                if not language in current_translations:
                    keys_missing_translations.add(translation_key)
                    missing_key_count = missing_key_counts.get(language, 0)
                    missing_key_counts[language] = missing_key_count + 1

        return missing_key_counts, keys_missing_translations


def main() -> None:
    print(
        f"All supported languages:\n{", ".join(Stringtables.supported_languages())}")
    print(
        f"All languages present in project:\n{", ".join(Stringtables.get_all_languages("."))}")


if __name__ == "__main__":
    main()
