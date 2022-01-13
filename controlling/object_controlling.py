from os.path import join
import pandas as pd

from settings import local_data_path, data_file

from disk.backuping import disk



def object_to_csv(data) -> pd.DataFrame():
    row = pd.DataFrame(columns=['id', 'name', 'text', 'tags', 'photo']).append(pd.Series({
        'id': data["id"],
        'name': data["name"],
        'text': None if "text" not in data else data["text"],
        'tags': None if "tags" not in data else data["tags"],
        'photo': None if "photo" not in data else data["photo"]
    }), ignore_index=True)

    return row


class Server:

    def __init__(self):

        self.abs_min = 0
        self.busy_id, self.freed_id = self.get_busy_and_free_id()

    def get_busy_and_free_id(self):
        busy_id = set(pd.read_csv(join(local_data_path, data_file))['id'])

        max_busy = self.abs_min

        if busy_id:
            max_busy = max(busy_id)

        freed_id = set([i for i in range(self.abs_min, max_busy + 1)]) - set(busy_id)

        return busy_id, freed_id

    def get_id(self):

        id = None
        if self.freed_id:
            id = min(self.freed_id)
            self.freed_id.remove(id)
            self.busy_id.add(id)

        else:

            if self.busy_id:
                id = max(self.busy_id) + 1
            else:
                id = self.abs_min

            self.busy_id.add(id)

        return id

    def del_id(self, id: int):

        self.freed_id += {id}

    def save_object(self, data):

        unique_id = self.get_id()
        data['id'] = unique_id
        if "photo" in data:
            data["photo"] = data["name"] + ".jpg"

        object_to_csv(data).to_csv(join(local_data_path, data_file), mode='a', index=False, header=False)
        disk.save_object(data)

    def get_data(self):
        return pd.read_csv(join(local_data_path, data_file))

    def get_by_query(self, query):

        data = self.get_data()

        result_id = set(data["id"])
        if "id" in query and query["id"] != "*":
            result_id = set(data[data["id"] == int(query["id"])]["id"])

        result_name = set(data["id"])
        if "name" in query and query["name"] != "*":
            result_name = set(data[data["name"] == int(query["name"])]["id"])

        result_tags = set(data["id"])
        if "tags" in query and query["tags"] != "*":

            orig_tags = set(query["tags"].split(" "))
            result_tags = set()
            for index, row in data.iterrows():
                if str(row["tags"]) != "nan" and set(row["tags"].split(" ")).intersection(orig_tags):
                    result_tags.add(row["id"])

        res_indexes = result_id.intersection(result_name).intersection(result_tags)
        return data[data["id"].isin(res_indexes)]


server = Server()
