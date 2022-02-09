"""Test the view.summary_report.generate_summary_report function"""

import logging
import pathlib

import pytest

import view.summary_report


@pytest.mark.parametrize("output_file_name_base", ["test_1", "test_2"])
def test_generate_summary_report(output_file_name_base: str, tmp_path: pathlib.Path) -> None:
    """Test the view.summary_report.generate_summary_report function

    Parameters:
    output_file_name_base (str): The file name base to use when creating the report
    tmp_path (pathlib.Path): The path used to stage files needed for testing (pytest fixture)

    Returns:
    None
    """
    output_path = tmp_path / f"{output_file_name_base}.html"

    # Generate the report
    view.summary_report.generate_summary_report(output_path=output_path)

    # Test the generated report
    with open(output_path, "r", encoding="utf_8") as report_file:
        doctype = report_file.readline()

        # Check for a DOCTYPE tag on the first line
        assert "DOCTYPE" in doctype
        minimum_line_count_sentry = False

        for line_counter, line in enumerate(report_file):
            # Log the XML line data every 10th line at the DEBUG level
            if line_counter % 10 == 0:
                logging.debug(line)

            # The report XML should have at least 20 lines of content
            if line_counter >= 20:
                minimum_line_count_sentry = True

    # Check whether the generated file exceeds a minimum line length threshold
    assert minimum_line_count_sentry is True
