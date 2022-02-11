"""Extract data from a RimWorld save file"""

import json
import logging
import os
import xml.etree.ElementTree


def get_element_by_search_pattern(tree: xml.etree.ElementTree, element_search_pattern: str) ->\
    xml.etree.ElementTree.Element:
    """Search for an XML element in a RimWorld save file using a search pattern

    Parameters:
    tree (xml.etree.ElementTree): The XML tree to search
    element_search_pattern (str): Target element search pattern

    Returns:
    xml.etree.ElementTree.Element: The first instance of the element matching the search pattern
    """
    logging.debug("Searching for element using pattern: %s", element_search_pattern)
    root = tree.getroot()
    element = root.find(element_search_pattern)
    logging.debug("Element information:\nTag: %s\nAttributes: %s\nText: %s\nKeys: %s",
        element.tag, element.attrib, element.text, element.keys())

    return element


def get_elements_by_search_pattern(tree: xml.etree.ElementTree, element_search_pattern: str,
    limit: int=None) -> list:
    """Search for an XML element in a RimWorld save file using a search pattern

    Parameters:
    tree (xml.etree.ElementTree): The XML tree to search
    element_search_pattern (str): Target element search pattern
    limit (int): The maximum number of matching elements to return (default None)

    Returns:
    list: A list of XML elements matching the search pattern
    """
    logging.debug("Searching for all elements using pattern: %s", element_search_pattern)
    root = tree.getroot()
    elements = root.findall(element_search_pattern)
    element_list = []

    for element in elements:
        logging.debug("Element information:\nTag: %s\nAttributes: %s\nText: %s\nKeys: %s",
            element.tag, element.attrib, element.text, element.keys())
        element_list.append(element)

        # Enforce limit
        if limit is not None:
            if len(element_list) >= limit:
                logging.debug("Stopping returning additional elements due to having reached the \
                    limit of elements to return (%d)", limit)
                break

    return element_list


def get_element_lineage(element: xml.etree.ElementTree.Element,
    root: xml.etree.ElementTree.Element, lineage: str=None) -> str:
    """Return the lineage of an element as a string showing the hierarchy of tags going back to the
    root element of the XML document

    Parameters:
    element (xml.etree.ElementTree.Element): The element being analyzed
    root (xml.etree.ElementTree.Element): The root element of the XML document
    lineage (str): The string representation of the element hierarchy

    Returns:
    str: String representation of the lineage of the XML element
    """

    # Add the starting element to the lineage string
    if lineage is None:
        logging.debug("Initializing the lineage string with the starting element")
        lineage = element.tag

    # Check to see if the element has a parent element
    parent = root.find(f".//{element.tag}/..")

    # The top level has been reached. End recursion by returning the lineage data
    if parent is None:
        logging.debug("Tag lineage analysis is complete. Returning lineage:\n%s", lineage)
        return lineage

    # This block only executes when there is a valid parent
    logging.debug("The current element, %s, has a parent element, %s.\nRecursing XML tree",
        element.tag, parent.tag)

    # Prepend the detected parent to the lineage string
    lineage = f"{parent.tag} > {lineage}"

    # Recurse upward in the hierarchy, eventually returning the complete hierarchy
    return get_element_lineage(element=parent, root=root, lineage=lineage)


def get_save_file_path() -> str:
    """Return the path to the RimWorld save file to analyze as a string

    Parameters:
    None

    Returns:
    str: The path to the save game file as configured in config.json
    """
    with open("config.json", "r", encoding="utf_8") as config_file:
        config_data = json.load(config_file)

    rimworld_save_file_path = config_data["rimworld_save_file_path"]
    logging.debug("Retrieved location of save game from config file: %s", rimworld_save_file_path)

    return rimworld_save_file_path


def get_save_file_size() -> int:
    """Return the file size of the RimWorld save

    Parameters:
    None

    Returns:
    int: The file size as reported by os.stat()
    """
    rimworld_save_file_path = get_save_file_path()
    file_size = os.path.getsize(rimworld_save_file_path)

    return file_size
