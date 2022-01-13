

def parse_dict(text):

    data = dict()
    for line in text.split("\n"):

        spl = list(line.split(":"))
        if len(spl) < 2:
            raise KeyError("Все строки должны иметь формат 'ключ : значение'")

        data[spl[0].strip(" ")] = ":".join(spl[1:]).strip(" ")

    return data
