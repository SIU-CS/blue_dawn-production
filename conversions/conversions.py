import csv
import openpyxl
from dicttoxml import dicttoxml
import xmltodict

def csv2xml(csv_file):
    """ Generates an xml string from an (untagged) csv data file
        
    Args:
        csv_file (string): path to the csv file

    Returns:
        bytes: XML bytes representing the untagged dataset
    """

    with open(csv_file, newline='') as csv_file:
        csv_data = csv.reader(csv_file)
        xml_dict = dict()
        xml_dict["tags"] = list()
        xml_dict["data"] = list()

        for row in csv_data:
            data_item = dict()
            data_item["question"] = row[0]
            data_item["tag"] = str()
            xml_dict["data"].append(data_item)
        
        return dicttoxml(xml_dict)

def xlsx2xml(xlsx_file):
    """ Generates an xml string from an (untagged) xlsx data file
    
    Args:
        xlsx_file (string): path to the xlsx file

    Returns:
        bytes: XML bytes representing the untagged dataset
    """ 

    xlxs_data = openpyxl.load_workbook(xlsx_file).active
    xml_dict = dict()
    xml_dict["tags"] = list()
    xml_dict["data"] = list()

    for elem in xlxs_data['A']:
        data_item = dict()
        data_item["question"] = elem.value
        data_item["tag"] = str()
        xml_dict["data"].append(data_item)

    return dicttoxml(xml_dict)


def xml2csv(xml):
    pass
        

def xml2xlsx(xml):
    pass

