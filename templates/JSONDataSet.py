import csv
import openpyxl
import json
from enum import Enum
from .models import DataSet
from pprint import pprint

class FileType(Enum):
    CSV=0
    XLSX=1
    JSON=2

class InputException(Exception):
    def __init__(self, message):
        self.message = message

class JSONDataSet:
    """ Class respresented a dataset

    Args:
        filepath (str): Path to a csv/xlsx file on disk (In case of JSON, this is actually the (poorly named) data itself)
        filetype (FileType): Enum value representing the type of the file (CSV/XLSX/JSON)
        name (str): Name for the dataset (can be left empty for FileType.JSON)
        description (str): Description for the dataset (can be left empty for FileType.JSON)
        id (int): The id for this dataset in the database; to be left None if creating a new dataset
    """
    def __init__(self, filepath, filetype, name, description, id=None):
        self.name = name # need to save name as an identifier
        self.id = id

        if filetype == FileType.CSV:
            self.json_dict = self._init_csv(filepath, name, description)

        elif filetype == FileType.XLSX:
            self.json_dict = self._init_xlsx(filepath, name, description)

        elif filetype == FileType.JSON:
            # lol why u do this?
            self.json_dict = json.loads(filepath)

    def _init_csv(self, filepath, name, description):
        """Initialize the object with a csv file

        Args:
            filepath (str): Path to the csv file on disk
            name (str): Name of the dataset
            description (str): Description for the dataset
        """
        with open(filepath, newline='') as csv_file:
            csv_data = csv.reader(csv_file) # parse the file

            # initialize the data structure
            json_dict = dict()
            json_dict['tags'] = list()
            json_dict['data'] = dict()
            json_dict['data']['questions'] = list()
            json_dict['data']['responses'] = list()
            json_dict['data']['tags'] = list()
            json_dict['title'] = name
            json_dict['description'] = description

            rid = 0
            for i, row in enumerate(csv_data):
                # first pass of for loop: first row of the csv
                if i == 0:
                    for qid, question in enumerate(row):
                        temp = dict()
                        temp['qid'] = qid
                        temp['question'] = question
                        json_dict['data']['questions'].append(temp)
                else:
                    for qid, response in enumerate(row):
                        temp = dict()
                        temp['rid'] = rid
                        temp['qid'] = qid
                        temp['response'] = response
                        json_dict['data']['responses'].append(temp)
                        if len(list(filter(lambda x: x['rid'] == rid, json_dict['data']['tags']))) == 0:
                            json_dict['data']['tags'].append({'rid': rid, 'tags': list()})
                    rid += 1

            return json_dict

    def _init_xlsx(self, filepath, name, description):
        """Initialize the object with a xlsx file

        Args:
            filepath (str): Path to the xlsx file on disk
            name (str): Name of the dataset
            description (str): Description for the dataset
        """
        xlsx_data = openpyxl.load_workbook(filepath).active

        # initialize the data structure
        json_dict = dict()
        json_dict['tags'] = list()
        json_dict['data'] = dict()
        json_dict['data']['questions'] = list()
        json_dict['data']['responses'] = list()
        json_dict['data']['tags'] = list()
        json_dict['title'] = name
        json_dict['description'] = description

        rid = 0
        for row in range(1, xlsx_data.max_row + 1):
            if row == 1: # first pass
                for qid, question in enumerate(xlsx_data[str(row)]):
                    temp = dict()
                    temp['qid'] = qid
                    temp['question'] = question.value
                    json_dict['data']['questions'].append(temp)
            else:
                for qid, response in enumerate(xlsx_data[str(row)]):
                    temp = dict()
                    temp['rid'] = rid
                    temp['qid'] = qid
                    temp['response'] = response.value
                    json_dict['data']['responses'].append(temp)
                    if len(list(filter(lambda x: x['rid'] == rid, json_dict['data']['tags']))) == 0:
                        json_dict['data']['tags'].append({'rid': rid, 'tags': list()})
                rid += 1
        pprint(json_dict)
        return json_dict

    # write this dataset to the database
    def SaveDataset(self, user):
        """ Write this dataset to the database; Create a new entry if it isn't already there, and update the old entry if it is

        Args:
            user (User): The user that is saving the dataset
        """
        if (self.id == None): # no id => this isn't in the database
            dataset = DataSet(data=json.dumps(self.json_dict), user=user)
        else: # this dataset is already in the database, we're just updating it
            dataset = DataSet.objects.get(id=self.id)
            dataset.data = json.dumps(self.json_dict)

        dataset.save()
        self.id = dataset.id

    # get all datasets in the database associated with a specific user
    @staticmethod
    def GetDatasets(user):
        """ Pull all of the datasets from the database corresponding to a specific user

        Args:
            user (User): The user to get datasets for

        Returns:
            List<JSONDataSet>: A list of JSONDataSets
        """
        datasets = DataSet.objects.filter(user=user)
        return list(map(lambda x: JSONDataSet(x.data, FileType.JSON, "", "", x.id), datasets))

    @staticmethod
    def GetDataset(id):
        """ Get the dataset with a specific id

        Args:
            id (int): Id of the dataset to get from the database

        Returns:
            JSONDataSet: The dataset with that id from the database
        """
        return JSONDataSet(DataSet.objects.get(id=id).data, FileType.JSON, "", "", id)

    def AddTag(self, tag):
        self.json_dict["tags"].append(tag)

    def RemoveTag(self, tag):
        while self.HasTag(tag):
            self.json_dict["tags"].remove(tag)
        #TODO: Remove instances of the tag in items

    def TagItem(self, rid, tags):
        item = next(filter(lambda x: str(x['rid']) == rid, self.json_dict['data']['tags']), dict())
        item['tags'] = tags

    def ItemHasTag(self, rid, tag):
        return tag in next(filter(lambda x: str(x['rid']) == rid, self.json_dict['data']['tags']), dict()).get('tags', list())

    def HasTag(self, tag):
        return tag in self.json_dict["tags"]

    def GetTags(id):
        return JSONDataSet(DataSet.objects.get(id=id).tags, FileType.JSON, "", "", id)

    def SetTags(self,tags):
        """ Set the list of tags on this dataset

        Args:
            tags (list<str>): List of tags to be set to this dataset
        """
        self.json_dict['tags'] = tags

    def _CheckPermission(self, user):
        return DataSet.objects.get(id=self.id).user.id == user.id


    def ExportCSV(self, user):
        if not self._CheckPermission(user):
            return

        with open("media/tmp/" + self.json_dict['title'] + ".csv", "w+") as fpntr:
            writer = csv.writer(fpntr)
            row = [x['question'] for x in self.json_dict['data']['questions']]
            row += self.json_dict['tags'] # concatenate the lists
            writer.writerow(row)

            matrix = [[None for i in range(len(self.json_dict['data']['questions']))] for j in range(int(len(self.json_dict['data']['responses'])/len(self.json_dict['data']['questions'])))]

            for response in self.json_dict['data']['responses']:
                matrix[response['rid']][response['qid']] = response

            for row in matrix:
                tags = next(filter(lambda x: x['rid'] == row[0]['rid'], self.json_dict['data']['tags']))['tags']
                tags_to_append = list()
                for tag in self.json_dict['tags']:
                    print("tags:")
                    tags_to_append.append(1 if tag in tags else 0)
                row = [x['response'] for x in row] + tags_to_append
                writer.writerow(row)

        return "media/tmp/" + self.json_dict['title'] + ".csv"

    def ExportXLSX(self, user):
        if not self._CheckPermission(user):
            return

        wb = openpyxl.Workbook()
        ws = wb.active

        row = [x['question'] for x in self.json_dict['data']['questions']]
        row += self.json_dict['tags'] # concatenate the lists
        ws.append(row)

        matrix = [[None for i in range(len(self.json_dict['data']['questions']))] for j in range(int(len(self.json_dict['data']['responses'])/len(self.json_dict['data']['questions'])))]

        for response in self.json_dict['data']['responses']:
            matrix[response['rid']][response['qid']] = response

        for row in matrix:
            tags = next(filter(lambda x: x['rid'] == row[0]['rid'], self.json_dict['data']['tags']))['tags']
            tags_to_append = list()
            for tag in self.json_dict['tags']:
                print("tags:")
                tags_to_append.append(1 if tag in tags else 0)
            row = [x['response'] for x in row] + tags_to_append
            ws.append(row)

        wb.save("media/tmp/" + self.json_dict['title'] + ".xlsx")
        return "media/tmp/self.json_dict['title']" + ".xlsx"
