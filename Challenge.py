class kvp:
    def __init__(self,str):
        self.str = str

    def parse(self):
        arr = self.str.split(': "')
        self.key = arr[0].strip()
        self.value = arr[1].strip()

    def to_json(self):
        return '"' + self.key + '" : "' + self.value.replace('@', '\\"') + '"'

class jobj:
    def __init__(self):
        self.elems = []
    def add(self,kvp):
        self.elems.append(kvp)
    def to_json(self):
        iterkv = iter(self.elems)
        kv = next(iterkv)
        tmp = '{' + kv.to_json()
        return tmp + ''.join([',' + kv.to_json() for kv in iterkv]) + '}'

def create_jobj(str):
    arr_kv = str.split('" ')
    res = jobj()
    for str in arr_kv:
        kv = kvp(str)
        kv.parse()
        res.add(kv)
    return res

with open('event_data.txt', 'r') as file:
    data = file.read()

no_escape = data.replace('\\"','@').strip()
arr_lines = no_escape.split('\n')
arr_jobj = []
for line in arr_lines:
    arr_jobj.append(create_jobj(line))

with open("part_a_challenge_output.txt", "w") as output:
    for jo in arr_jobj:
        output.write(jo.to_json())