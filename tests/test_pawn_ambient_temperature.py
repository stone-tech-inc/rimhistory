"""Test the extraction of pawn environment ambient temperature"""

import logging

from save import Save


def test_pawn_ambient_temperature(config_data: dict) -> None:
    """Test the extraction of pawn environment ambient temperature

    Parameters:
    config_data (dict): The project configuration data as a dictionary (fixture)

    Returns:
    None
    """
    path_to_save_file = config_data["rimworld_save_file_path"]
    pawn_data = Save(path_to_save_file=path_to_save_file).data.dataset.pawn.dictionary_list
    logging.debug(pawn_data[0].keys())

    assert "pawn_ambient_temperature" in pawn_data[0].keys()
