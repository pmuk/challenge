def is_prime(n): 
    if n <= 1: 
        return False

    for i in range(2, n): 
        if n % i == 0: 
            return False; 
  
    return True

def calculate_next(last_prime):
    prime = False
    current = last_prime
    while not prime:
        current = current + 1
        prime = is_prime(current)
    return current

class kvp:
    def __init__(self,str):
        self.str = str

    def parse(self):
        arr = self.str.split(': "')
        self.key = arr[0].strip()
        self.value = arr[1].replace('"','').strip()

    def to_json(self):
        return '"' + self.key + '" : "' + self.value.replace('@', '\\"') + '"'

    def to_origin(self):
        return self.key + ': ' + '"' + self.value.replace('@','\\"') + '"'

class jobj:
    def __init__(self):
        self.elems = []
    
    def add(self,kvp):
        self.elems.append(kvp)
    
    def replace_value(self, key, new_val):
        for kv in self.elems:
            if kv.key == key:
                kv.value = new_val

    def to_json(self):
        iterkv = iter(self.elems)
        kv = next(iterkv)
        tmp = '{' + kv.to_json()
        return tmp + ''.join([',' + kv.to_json() for kv in iterkv]) + '}'

    def to_origin(self):
        iterkv = iter(self.elems)
        kv = next(iterkv)
        tmp = kv.to_origin()
        return tmp + ''.join([' '+kv.to_origin() for kv in iterkv])

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

from copy import deepcopy

#we deep copy the previous event store in the event_data.txt, deepcopy as we need to modify the list in jobj object
cpy = deepcopy(arr_jobj[0])
#we parse the fourth (and last) value of the last event from hexa
last_prime = int(cpy.elems[len(cpy.elems)-1].value,16)
key = 0x17F
#we un-obfuscate the value
unobfuscated = last_prime^key
#we calculate the next prime (not sure if it was needed or if I could just use a hardcoded value)
next_prime = calculate_next(unobfuscated)
#we reobfuscate
next_obf = next_prime^key
#we create a keyValuePair element in order to store our newly found value
new_kv = kvp('five: "'+str(hex(next_obf)))
new_kv.parse()
#we add the kvp to the structure containing the event
cpy.add(new_kv)
#we update the challenge as we need now to find the sixth value
cpy.replace_value('challenge', 'Find the sixth value in the @sequence@')

#we write the solution
with open("part_b_challenge_output.txt", "w") as output:
    for jo in arr_jobj:
        output.write(cpy.to_origin())