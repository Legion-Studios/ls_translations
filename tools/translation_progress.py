#!/usr/bin/env python3
"""
Author: KoffeinFlummi, DartRuffian
Modified from: https://github.com/acemod/ACE3/blob/master/tools/stringtablediag.py

Checks for missing translations and tracks translation progress in a GitHub issue.
Use --markdown to only return markdown formatted data
"""

import sys
import os
from xml.dom import minidom


def get_all_languages(project_path):
    """Checks what languages exist in the repo."""
    languages = []

    for addon in os.listdir(project_path):
        if addon[0] == ".":
            continue

        stringtable_path = os.path.join(project_path, addon, "stringtable.xml")
        try:
            xml_doc = minidom.parse(stringtable_path)
        except:
            continue

        keys = xml_doc.getElementsByTagName("Key")
        for key in keys:
            for child in key.childNodes:
                try:
                    if not child.tagName in languages:
                        languages.append(child.tagName)
                except:
                    continue

    return languages


def check_addon(project_path, addon, languages):
    """Checks the given addon for all the different languages."""
    localized = []

    stringtable_path = os.path.join(project_path, addon, "stringtable.xml")
    try:
        xml_doc = minidom.parse(stringtable_path)
    except:
        return 0, localized

    key_number = len(xml_doc.getElementsByTagName("Key"))

    for language in languages:
        localized.append(len(xml_doc.getElementsByTagName(language)))

    return key_number, localized


def main():
    scriptpath = os.path.realpath(__file__)
    project_path = os.path.dirname(os.path.dirname(scriptpath))

    languages = get_all_languages(project_path)

    if "--markdown" not in sys.argv:
        print("#########################")
        print("# Stringtable Diag Tool #")
        print("#########################")
        print("\nLanguages present in the repo:")
        print(", ".join(languages))

    key_sum = 0
    localized_sum = list(map(lambda x: 0, languages))
    missing = list(map(lambda x: [], languages))

    language_names = {"Chinesesimp": "Simplified Chinese"}

    for addon in os.listdir(project_path):
        key_number, localized = check_addon(project_path, addon, languages)

        if key_number == 0:
            continue

        if "--markdown" not in sys.argv:
            print("\n# " + addon)

        key_sum += key_number
        for i in range(len(localized)):
            if "--markdown" not in sys.argv:
                print("  %s %s / %i" %
                      ((languages[i]+":").ljust(10), str(localized[i]).ljust(3), key_number))
            localized_sum[i] += localized[i]
            if localized[i] < key_number:
                missing[i].append(addon)

    if "--markdown" not in sys.argv:
        print("\n###########")
        print("# RESULTS #")
        print("###########")
        print("\nTotal number of keys: %i\n" % (key_sum))

        for i in range(len(languages)):
            language = languages[i]
            language = language_names.get(
                language, language)  # Prettified names
            if localized_sum[i] == key_sum:
                print("%s No missing stringtable entries." %
                      ((language + ":").ljust(12)))
            else:
                print("%s %s missing stringtable entry/entries." %
                      ((language + ":").ljust(12), str(key_sum - localized_sum[i]).rjust(4)), end="")
                print(" ("+", ".join(missing[i])+")")

        print("\n\n### MARKDOWN ###\n")

    print("Total number of keys: %i\n" % (key_sum))

    print("| Language | Missing Entries | Addons | % Translated |")
    print("|----------|----------------:|--------|--------------|")

    for i, language in enumerate(languages):
        language = language_names.get(language, language)

        if localized_sum[i] == key_sum:
            print("| {} | 0 | - | 100% |".format(language))
        else:
            print("| {} | {} | {} | {}% |".format(
                language,
                key_sum - localized_sum[i],
                ", ".join(missing[i]),
                round(100 * localized_sum[i] / key_sum, 2)))

    print("\n\nThank you to the ACE team for the original script.")


if __name__ == "__main__":
    main()
