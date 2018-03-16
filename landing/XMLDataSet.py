import csv
import openpyxl
import xmltodict
from dicttoxml import dicttoxml
from enum import Enum
from landing.models import DataSet

class FileType(Enum):
    CSV=0
    XLSX=1
    XML=2

class XMLDataSet:
    def __init__(self, filepath, filetype):
        if filetype == FileType.CSV:
            with open(filepath, newline='') as csv_file:
                csv_data = csv.reader(csv_file)
                xml_dict = dict()
                xml_dict["tags"] = list()
                xml_dict["data"] = list()

                xml_dict["title"] = csv_data.__next__()
                xml_dict["description"] = csv_data.__next__()

                for row in csv_data:
                    data_item = dict()
                    data_item["question"] = row[0]
                    data_item["tag"] = str()
                    xml_dict["data"].append(data_item)
                
            self.xml = dicttoxml(xml_dict)

        elif filetype == FileType.XLSX:
            xlxs_data = openpyxl.load_workbook(filepath).active
            xml_dict = dict()
            xml_dict["tags"] = list()
            xml_dict["data"] = list()

            i = 0
            for elem in xlxs_data['A']:
                if i == 0:
                    xml_dict["title"] = elem.value
                elif i == 1:
                    xml_dict["description"] = elem.value
                else:
                    data_item = dict()
                    data_item["question"] = elem.value
                    data_item["tag"] = str()
                    xml_dict["data"].append(data_item)
                i += 1

            self.xml =  dicttoxml(xml_dict)

        elif filetype == FileType.XML:
            self.xml = filepath

    # write this dataset to the databse
    def SaveDataset(self, user):
        print(user.id)
        dataset = DataSet(data=self.xml, user=user)
        dataset.save()

    # get all datasets in the database associated with a specific user
    @staticmethod
    def GetDatasets(user):
        return list(map(lambda x: XMLDataSet(x, FileType.XML), DataSet.objects.filter(user=user).values()))


    def xml2csv(xml):
        pass

    def xml2xlsx(xml):
        pass
