import csv
import openpyxl
import json
from enum import Enum
from landing.models import DataSet
from pprint import pprint

class FileType(Enum):
    CSV=0
    XLSX=1
    JSON=2

class JSONDataSet:
    def __init__(self, filepath, filetype):
        if filetype == FileType.CSV:
            with open(filepath, newline='') as csv_file:
                csv_data = csv.reader(csv_file)
                json_dict = dict()
                json_dict["tags"] = list()
                json_dict["data"] = list()

                json_dict["title"] = csv_data.__next__()
                json_dict["description"] = csv_data.__next__()

                for row in csv_data:
                    data_item = dict()
                    data_item["question"] = row[0]
                    data_item["tag"] = str()
                    json_dict["data"].append(data_item)
                
            self.json_dict = json_dict

        elif filetype == FileType.XLSX:
            xlxs_data = openpyxl.load_workbook(filepath).active
            json_dict = dict()
            json_dict["tags"] = list()
            json_dict["data"] = list()

            i = 0
            for elem in xlxs_data['A']:
                if i == 0:
                    json_dict["title"] = elem.value
                elif i == 1:
                    json_dict["description"] = elem.value
                else:
                    data_item = dict()
                    data_item["question"] = elem.value
                    data_item["tag"] = str()
                    json_dict["data"].append(data_item)
                i += 1

            self.json_dict = json_dict

        elif filetype == FileType.JSON:
            # lol
            self.json_dict = json.loads(json.loads(filepath['data']))

    # write this dataset to the database
    def SaveDataset(self, user):
        dataset = DataSet(data=json.dumps(self.json_dict), user=user)
        dataset.save()

    # get all datasets in the database associated with a specific user
    @staticmethod
    def GetDatasets(user):
        return list(map(lambda x: JSONDataSet(x, FileType.JSON), DataSet.objects.filter(user=user).values()))

    def AddTag(self, tag):
        self.json_dict['tags'].append(tag)

    #TODO
    def xml2csv(xml):
        pass

    #TODO
    def xml2xlsx(xml):
        pass
