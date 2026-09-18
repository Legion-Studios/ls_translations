#!/usr/bin/env python3
"""
Author: DartRuffian

Comments on a GitHub PR for missing translations
"""

import os
import sys
import traceback
import github
from stringtables import Stringtables
import io
from contextlib import redirect_stdout


def output_message(project_path: str, languages: list[str]):
    """Prints a table of the results to stdout"""
    row = "| {} | {} | {} |"
    all_missing_keys: set[str] = set()
    total_missing_translations: dict[str, tuple[int, set[str]]] = {}

    for addon in os.listdir(project_path):
        # Skip files or addons without a stringtable
        if not os.path.isfile(os.path.join(
                project_path, addon, "stringtable.xml")):
            continue

        missing_translation_counts, keys = Stringtables.check_missing_translations(
            project_path, addon, languages)
        all_missing_keys = all_missing_keys.union(keys)

        for language, count in missing_translation_counts.items():
            total_count, addons = total_missing_translations.get(
                language, (0, set()))  # type: ignore
            addons.add(addon)
            total_missing_translations[language] = (
                total_count + count, addons)

    if not total_missing_translations:
        print("No missing translations found!")
        return

    print("| Language | Missing Entries | Addons |")
    print("|----------|----------------:|--------|")

    for language, value in total_missing_translations.items():
        total_keys, addons = value
        print(row.format(language, total_keys, ", ".join(addons)))

    count_missing_keys = len(all_missing_keys)
    print()
    print(
        f"There are {count_missing_keys} keys missing translations for: {', '.join(languages)}")
    if (count_missing_keys <= 10):
        sorted_keys = list(all_missing_keys)
        sorted_keys.sort()
        for key in sorted_keys:
            print(f"  - {key}")


def extract_added_languages(git_diff: str) -> list[str]:
    """Takes a git diff and then extracts out newly added languages in the stringtables"""
    diff_lines = git_diff.split("\n")
    added_languages: list[str] = []

    languages = Stringtables.supported_languages()

    for line in diff_lines:
        # Filter out any changes that aren't lines being added (+++ = file additions)
        if not (line.startswith("+ ") and not line.startswith("+++")):
            continue
        line = line[1:].strip()  # Remove "+" and whitespace

        # Extract language name from line, e.g. <Language>Text</Language>
        language = line.split(">")[0][1:]
        if not language in languages:
            continue

        added_languages.append(language)

    return added_languages


def create_github_comment(message: str) -> int:
    try:
        token = os.environ["GITHUB_TOKEN"]
        pr_number = int(os.environ["PR_NUMBER"])
        auth = github.Auth.Token(token)
        repository = github.Github(auth=auth).get_repo(
            os.environ["REPOSITORY"])
    except:
        print("Could not obtain vars.")
        print(traceback.format_exc())
        return 1
    else:
        print("Sucessfully obtained environment variables.")

    print("\nCreating comment...")
    try:
        pr = repository.get_pull(pr_number)
        pr.create_issue_comment(body=message)
    except:
        print("Failed to update translation issue.")
        print(traceback.format_exc())
        return 1
    else:
        print("Successfully commented on pull request.")
    return 0


def main() -> int:
    script_path = os.path.realpath(__file__)
    project_path = os.path.dirname(os.path.dirname(script_path))

    git_diff = sys.stdin.read()
    languages = extract_added_languages(git_diff)

    # Capture all output to stdout and save it
    if "--print-local" in sys.argv:
        output_message(project_path, languages)
    else:
        output_capture = io.StringIO()
        with redirect_stdout(output_capture):
            output_message(project_path, languages)

        create_github_comment(output_capture.getvalue())

    return 0


if __name__ == "__main__":
    sys.exit(main())
