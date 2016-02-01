# Python 3 JSON Library
# JSON serialization Using Mappings
Python 3 library for serializing and deserializing complex class-based Python models using an arbitrary complex schema 
of mappings. 


## Features
* Ability to create serializers and deserializers for complex Python class-based models using a mapping schema.
* Python models need not be coupled to the serialization process - models do not have to inherit from a particular
superclass or implement an interface with a "to_json" (or similar) method.
* JSON representations produced are not coupled to the Python model - an arbitrary mapping between the JSON and the
model can be defined.
* Works seamlessly with Python's in-built `json.dumps` and `json.loads` serialization methods - does not require the use
of exotic "convert_to_json" methods.
* Simple to define serialization of subclasses based on how superclasses are serialized.
* Pure Python 3 - no XML or similar required to describe mappings, not using outdated Python 2.


## How to use
### Outline
1. Define schema for mapping an object to and/or from JSON representation using a list of `JsonPropertyMapping`
definitions.
2. Use `MappingJSONEncoderClassBuilder` with the mappings to build a subclass of `JSONEncode` for serializing instances 
of a specific type. Similar with decode.
3. Use created encoder class with Python's in-built `json.dumps` via the `cls` parameter. Similar with decoder.

Example:
```python
simple_mapping_schema = [JsonPropertyMapping("json_property", "object_property")]

MyObjectJSONEncoder = MappingJSONEncoderClassBuilder(MyObjectType, simple_mapping_schema).build()

my_object_as_json_string = json.dumps(my_object, cls=MyObjectJSONEncoder, **other_kwargs)
```


### Details
#### One-to-one JSON property to object property mapping
Model:
```python
class Person:
    def __init__(self):
        self.name = None
```

JSON:
```json
{
    "full_name": <person.name>
}
```

To define that:
* The JSON "full_name" property is set from the object's "name" property.
* The object's "name" property is set from the JSON's "full_name" property.
```python
mapping_schema = [JsonPropertyMapping("full_name", "name")]
```

Build class that will serialize `Person` models to JSON (subclass of `JSONEncoder`):
```python
PersonJSONEncoder = MappingJSONEncoderClassBuilder(Person, mapping_schema).build()
```

Serialize instance of `Person` using Python's inbuilt `json.dumps`:
```python
person_as_json = json.dumps(person, cls=PersonJSONEncoder, indent=1)
```

Build class that will deserialize `Person` models from JSON (subclass of `JSONDecoder`):
```python
PersonJSONDecoder = MappingJSONDecoderClassBuilder(Person, mapping_schema).build()
```

Deserialize JSON representation of `Person` model using Python's inbuilt `json.loads`:
```python
person = json.loads(person_as_json, cls=PersonJSONDecoder)
```


#### Arbitrary mapping to JSON property value
Model:
```
class Person(Model):
    def __init__(self):
        self.name = None

    def get_first_name(self) -> str:
        return self.name.split(" ")[0]
        
    def get_family_name(self) -> str:
        return self.name.split(" ")[1]
```

JSON:
```json
{
    "first_name": <person.get_first_name()>,
    "family_name": <person.get_family_name()>
}
```

To define that:
* Serialization to the JSON "first_name" property value uses the object's `get_first_name` method.
* Serialization to the JSON "family_name" property value uses the object's `get_family_name` method.
```python
mapping_schema = [
    JsonPropertyMapping("first_name", object_property_getter=lambda person: person.get_first_name()),
    JsonPropertyMapping("family_name", object_property_getter=lambda person: person.get_family_name())
]
```
* See <LINK> for how to do the reverse mapping. *


#### Arbitrary mapping to object property value
Model:
```
class Person(Model):
    def __init__(self):
        self.name = None
```

JSON:
```json
{
    "first_name": <person.get_first_name()>,
    "family_name": <person.get_family_name()>
}
```

To define that:
* The object's name property value is derived from the value of both the "first_name" and "family name" JSON property 
values:
```python
mapping_schema = [
    JsonPropertyMapping("name", json_property_getter=lambda obj_as_dict: "%s %s" % (obj_as_dict["first_name"],
                                                                                    obj_as_dict["family_name"]))
]
```


#### Deserializing objects with constructors parameters
Model:
```python
class Person:
    def __init__(self, constructor_name: str):
        self.name = name
```

JSON:
```json
{
    "full_name": <person.name>
}
```

To define that:
* Serialization to the JSON "full_name" property value uses the object's "name" property value.
* Deserialization requires the value of the JSON "full_name" property be binded to the "constructor_name" parameter
in the constructor:
```python
mapping_schema = [JsonPropertyMapping("full_name", "name", object_constructor_parameter_name="constructor_name")]
```


#### Deserializing objects with mutators
Model:
```python
class Person:
    def __init__(self):
        self._name = None
        
    def set_name(name: str):
        self._name = name
```

JSON:
```json
{
    "full_name": <person._name>
}
```

To define that:
* Deserialization requires the private "_name" property be set via the "set_name" mutator from the "full_name" JSON
property.
```python
mapping_schema = [JsonPropertyMapping("full_name", object_property_setter=lambda person, name: person.set_name(name))]
```


#### Conditionally optional JSON properties
Model:
```python
class Person:
    def __init__(self):
        self.name = name
```

JSON:
```json
<if person.name is not None:>
{
    "full_name": <person.name>
}
<else:>
{
    # No `full_name` property
}
```

To define that:
* JSON representation should only include the "full_name" if it is not `None` (e.g. to reduce the size of the JSON).
```python
def add_name_to_json_if_not_none(json_as_dict: dict, name: Optional[str]):
    if name is not None:
        json_as_dict["full_name"] = name

mapping_schema = [JsonPropertyMapping("full_name", json_property_setter=add_name_to_json_if_not_none)]
```


#### Inheritance
Models:
```python
class Person:
    def __init__(self):
        self.name = None
        
    
class Employee(Person):
    def __init__(self):
        super().__init__()
        self.title = None
```

JSON:
```json
{
    "full_name": <employee.name>,
    "job_title": <employee.title>
}
```

To define that:
* Serialization of `Employee` should "extend" the way `Person` is serialized.
```python
person_mapping_schema = [JsonPropertyMapping("full_name", "name")]
employee_mapping_schema = [JsonPropertyMapping("job_title", "title")]

PersonJSONEncoder = MappingJSONEncoderClassBuilder(Person, person_mapping_schema).build()
EmployeeJSONEncoder = MappingJSONEncoderClassBuilder(Employee, employee_mapping_schema, Person).build()

PersonJSONDecoder = MappingJSONDecoderClassBuilder(Person, person_mapping_schema).build()
EmployeeJSONDecoder = MappingJSONDecoderClassBuilder(Employee, employee_mapping_schema, Person).build()
```

Note: Mappings of properties for superclass are done first and can subsequently be "overriden" by mappings for the
subclass. For obvious reasons, mappings to constructor parameters of superclass are not used if serialization involves
the subclass.


#### Nested complex objects
Model:
```python
class Person:
    def __init__(self):
        self.name = None


class Team:
    def __init__(self):
        self.moto = None
        self.people = []    # type: List[Person]
```

JSON:
```json
{
    "team_moto": <team.moto>,
    "members": <[person in team.people]>
}
```

To define that:
* `Person` instances, nested inside `Employee` objects, should be serialized and deserialized by specific encoder and 
decoders.
```
employee_mapping_schema = [
    JsonPropertyMapping("team_moto", "moto"),
    JsonPropertyMapping("members", "people", encoder_cls=PersonJSONEncoder, decoder_cls=PersonJSONDecoder)
]
```


#### One-way mappings
* Contrived example warning... *

Model:
```python
class Person:
    def __init__(self):
        self.name = None
        self.age = None
```

JSON input:
```json
{
    "full_name": <person.name>
}
```

JSON output:
```json
{
    "age": <person.age>
}
```

To define that:
* Serialization should ignore the object's "name" property.
* Deserialization only with the JSON's "full_name" property.
```python
mapping_schema = [
    JsonPropertyMapping(
        json_property_getter=lambda json_as_dict: json_as_dict["full_name"],
        object_property_setter=lambda person, name: person.set_name(name)
    ),
    JsonPropertyMapping(
        json_property_setter=lambda json_as_dict, age: json_as_dict.__setitem__("age", age),
        object_property_getter=lambda person: person.age
    )
]
```


### Warning
Ensure your serializers are not vulnerable to attack if you are serializing JSON from an untrusted source.


### Notes
* Decoders and encoders work for iterable collections of instances in the same way as they do for single instances.



## Performance
If you are performing serialization, chances are that you are going to be doing/have done I/O. Given how relatively slow
the I/O will be, **the performance** of this library, compared with that of any other (including the endless JSON
libraries touted as "ultra fast"), **is not going to be of realistic concern** given reasonable amounts of data.

However, if you happen to be serializing huge numbers of objects and need it done extraordinarily fast (in Python?), use
of JSON encoders/decoders produced by this library will add a small amount of overhead on-top of the in-built JSON
serialization methods. In addition, the complexity of the mappings used will influence the performance (i.e. if the
value of a JSON property is calculated from an object method that finds the answer to life, the universe and everything,
serialization is going to be rather slow).


## Alternatives
* If you are not using class-based Python models and have no restrictions on the structure of the JSON representation:
    * [Python's in-built `json` library](https://docs.python.org/3/library/json.html) will work out the box with its 
    default encoder (`JSONEncode`) and decoder (`JSONDecode`).
    * [demjson](https://github.com/dmeranda/demjson) can encode and decode JSON with added syntax checking.
    * [ultrajson](https://github.com/esnme/ultrajson) claimed as "ultra fast" JSON encoder and decoder.
    * [py-yajl](https://github.com/rtyler/py-yajl) yet another "fast" JSON encoder/decoder.
* If you are using class-based Python models but your JSON need not be human readable and you are not concerned with
interoperability:
    * [jsonpickle](https://github.com/jsonpickle/jsonpickle) will automatically serialize objects.
    * [py-importjson](https://github.com/TonyFlury/py-importjson).
* If you want to deserialize flat data files into Python `dict` objects using mapping schema:
    * [jsonmapping](https://github.com/pudo/jsonmapping)
* If you do not mind coupling your Python models to the serialization library:
    * [jsonobject](https://github.com/dimagi/jsonobject).
* If you only wish to serialize models using a mapping schema and are not interested in deserialization or compatibility
with Python's in-built `json` library.
    * [serpy](https://github.com/clarkduvall/serpy) can serialize complex models with arbitrary mappings from fields and
    methods to JSON.


## License
[GNU GPL](LICENSE.txt).