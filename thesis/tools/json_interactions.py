import json
import os
from os import path

class JsonEditor:

    @staticmethod
    def check_if_json_exists(file_path):
        return path.exists(file_path)

    @staticmethod
    def write_to_json(file_path, dictionary):
        json_string = json.dumps(dictionary)
        json_file = open(file_path, "w")
        json_file.write(json_string)
        json_file.close()
        print(f"JSON write successful to: {file_path[43:]}")

    @staticmethod
    def read_from_json(file_path):
        with open(file_path) as f:
            dictionary = json.load(f)
            f.close()
        return dictionary

    @staticmethod
    def find_new_values(new_dict, existing_json, method=1):
        """
        :param new_dict:
        :param existing_json:
        :param method: [method 1] (less strict) is used when adding new competition links.
        [method 2] (more strict) is used when updating the matches database.
        :return:
        """
        new_values_dict = {}
        for value in new_dict:
            if method == 2:
                if value not in existing_json and new_dict[value] not in existing_json.values():
                    new_values_dict.update({value: new_dict[value]})

            elif method == 1:
                if value not in existing_json or new_dict[value] not in existing_json.values():
                    new_values_dict.update({value: new_dict[value]})

        if len(new_values_dict) > 0:
            return new_values_dict
        else:
            return None

    @staticmethod
    def update_json(new_dict, file_name, json_folder=1, method=1):
        """
        :param new_dict: New dictionary which the older dictionary should be update with.
        :param file_name: filename in folder
        :param json_folder:
        [1] is competitions/competition folder
        [2] is the matches folder
        :param method:
        [1] is standard method for update competitions and sports
        [2] is method used for updating matches
        :return:
        """
        json_location = JsonEditor.json_path_finder(file_name, json_folder)
        json_exists = JsonEditor.check_if_json_exists(json_location)

        if json_exists is False:
            json_location = json_location
            JsonEditor.write_to_json(json_location, new_dict)
            print(f"[update_json SUCCESS] New JSON file created at: {json_location}")
            return len(new_dict)

        existing_json = JsonEditor.read_from_json(json_location)
        new_values_dict = JsonEditor.find_new_values(new_dict, existing_json, method)

        if new_values_dict is not None:
            existing_json.update(new_values_dict)
            JsonEditor.write_to_json(json_location, existing_json)
            print(f"JSON {json_location.split('arbitrageproject')[1]} updated with following values:\n{new_values_dict}")
            return len(new_values_dict)
        else:
            print(f"No new values, JSON not updated")
            return 0


    @staticmethod
    def get_total_match_amount():
        file_path = JsonEditor.json_path_finder('matches', 3)

        match_amount = JsonEditor.read_from_json(file_path)['match_count']
        print(f"Current matches in database: {match_amount}")
        return match_amount

    @staticmethod
    def update_total_match_amount(new_amount):
        new_amount_dict = {"match_count": new_amount}
        file_path = JsonEditor.json_path_finder('matches', 3)

        JsonEditor.write_to_json(file_path, new_amount_dict)
        return print(f"Updated amount of matches in database: {new_amount}")

# dict = Json_editor.read_from_json(r"C:\Users\Ck0rt\PycharmProjects\arbitrageproject\json_files\test.json")


