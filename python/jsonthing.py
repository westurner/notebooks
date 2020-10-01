import datetime
import json


class Thing(dict):
    def __json__(self, spec=None):
        return {k.title(): v for k, v in self.items()}


class DatedThing(Thing):
    def __json__(self, **kw):
        return {
            **super().__json__(**kw),
            **{"dateCreated": datetime.datetime.now().isoformat()},
        }


data = {"things": [DatedThing(one=1)]}
jsonstr = json.dumps(data)
_data = json.loads(jsonstr)
assert "dateCreated" not in _data["things"][0]


class JSONJSONEncoder(json.JSONEncoder):
    def _iterencode(obj, _current_indent_level):
        import pdb; pdb.set_trace()
        if hasattr(obj, "__json__"):
            _obj = obj.__json__()
        else:
            _obj = obj
        return super()._iterencode(_obj, _current_indent_level)


jsonstr = json.dumps(data, cls=JSONJSONEncoder)
assert "dateCreated" in jsonstr

_data = json.loads(jsonstr)
assert "dateCreated" in _data["things"][0]
assert isinstance(_data["things"][0]["dateCreated"], str)


class DateJSONDecoder(json.JSONDecoder):
    @staticmethod
    def _object_pairs_hook(items):
        for key, value in items:
            if key.startswith("date") or key.endswith("_date"):
                value = datetime.datetime.fromisoformat(value)
            yield key, value

    @classmethod
    def object_pairs_hook(cls, items):
        return dict(cls._object_pairs_hook(items))


_data = json.loads(jsonstr,
                   object_pairs_hook=DateJSONDecoder.object_pairs_hook)
assert "dateCreated" in _data["things"][0]
assert isinstance(_data["things"][0]["dateCreated"], datetime.datetime)

# TODO: JSONEncode...

"""But, this approach needs an actual schema to reference in order to properly
deserialize datetimes that have attribute names that don't contain "date": we
must have a schema that maps attribute names to datatypes (or reify and specify
every value as a [datatype, value] tuple, for example, for every value). With
JSON-LD, @context is that schema."""
