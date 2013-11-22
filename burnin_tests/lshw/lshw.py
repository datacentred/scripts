#!/usr/bin/env python3
"""
Harware validation module
"""

import re
import subprocess
import xml.etree.ElementTree as ET

class HardwareValidator:
    """
    Class to interrogate the host platform's hardware configuration via
    the lshw command.
    """

    def __init__(self):
        """
        Class initialisation
        """
        self.data = None
        self.tree = None
        self.stack = None

    def collect(self):
        """
        Collects the output from lshw

        @returns True on success or False on failure
        """
        try:
            self.data = subprocess.check_output(['lshw', '-xml'])
        except subprocess.CalledProcessError:
            return False

        return True

    def inject(self, filename):
        """
        For test purposes inject a test input into the class rather
        than invoke lshw directly

        @returns True on success or False on failure
        """
        try:
            filein = open(filename)
        except IOError:
            return False

        self.data = filein.read()
        filein.close()
        return True

    def parse(self):
        """
        Attempt to parse the output data collected during collect()
        
        @returns True on success or False on failure
        """
        try:
            xml = ET.fromstring(self.data)
        except ET.ParseError:
            print('Malformed XML inject')
            return False
        self.tree = ET.ElementTree(xml)
        return True

    def validate_recurse(self, element):
        """
        Performs a recursive validation of element and its sub
        elements.

        We maintain a stack to record where we are in the tree, this
        along with any id attributes are combined into an XPath lookup
        which identifies a unique element in the system tree.  If the
        element contains any text compare for equality

        @param element Valid element to validate against the system XML
            tree

        @returns True on success, False on failure
        """
        # Append the current element to the XPath stack.  We assume that
        # if an id attribute is present it will be a unique identifier,
        # otherwise we rely on the element only being allowed a single
        # instance by the schema
        selector = element.tag
        uuid = element.get('id')
        if uuid != None and len(uuid):
            selector += "[@id='" + element.get('id') + "']"

        # Build a search path relative to the root node
        self.stack.append(selector)
        path = '/'.join(self.stack)

        # Find any nodes that match in the system description, if they
        # dont exist flag a failure as the tree structures don't match
        print(path)
        match = self.tree.findall(path)
        if len(match) != 1:
            print('error: XPath not unique')
            return False

        # Things get messy here as XML shouldn't have any whitespace
        # between elements.  As a result the xml parser will quite
        # happily parse [\s\n]+ as valid text, so be sure to filter
        # those out before comparison
        if element.text and re.match(r'[^\s\n]', element.text):
            if not match[0].text or not re.match(r'[^\s\n]', match[0].text):
                print('error: element has no text')
                return False
            if element.text != match[0].text:
                print('error: element text mismatch')
                print('expected:', element.text)
                print('recieved:', match[0].text)
                return False

        # Recurse down the tree
        for subelement in element:
            if not self.validate_recurse(subelement):
                return False

        self.stack.pop()
        return True

    def validate(self, configuration):
        """
        Validates the configuration parsed in parse() is what we are
        expecting

        @param configuration Path to an XML configuration file to
            validate the system XML tree against

        @returns True on success or False on failure
        """
        try:
            tree = ET.parse(configuration)
        except ET.ParseError:
            print('Malformed XML configuration')
            return False

        # Do a depth first traversal of each sub element repeating the
        # the attribute checks at each node
        self.stack = list()
        for subelement in tree.getroot():
            if not self.validate_recurse(subelement):
                return False

        return True

# Test harness
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print('error: expected configuration file')
        sys.exit(1)
    validator = HardwareValidator()
    if not validator.collect():
        print('error: unable to collect data')
        sys.exit(1)
    if not validator.parse():
        print('error: unable to parse data')
        sys.exit(1)
    if validator.validate(sys.argv[1]):
        sys.exit(0)
    else:
        sys.exit(1)
