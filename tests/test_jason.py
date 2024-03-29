"core.jason"

import collections
import sys

from dkjason.jason import jsonname, response, NUMPY

try:
    import numpy as np
except ImportError:  # pragma: nocover
    pass

import pytest
import datetime
import decimal
import ttcal
from dkjason import jason


def roundtrip(v):
    "Convenience function to thest the roundtrip (dump/eval)."
    return jason.json_eval(jason.dumps(v)) == v


def test_jason_eval():
    "Test the jason_eval function using the roundtrip convenience function."
    assert roundtrip([])
    assert roundtrip(['hello world'])
    assert roundtrip(['hello world'.split()])
    assert roundtrip({})


if NUMPY:
    def test_numpy_vals():
        assert jason.loads(jason.dumps(np.int64(42))) == 42


def test_dumps():
    "Test the dumps function."
    assert jason.dumps(datetime.datetime(2012, 4, 2, 6, 12), indent=None) == '"@datetime:2012-04-02T06:12:00"'
    assert jason.dumps(decimal.Decimal('3.14159263')) == repr(float('3.14159263'))
    assert jason.dumps({}.keys()) == '[]'
    assert jason.dumps({}.values()) == '[]'
    assert jason.dumps(range(0)) == '[]'
    assert jason.dumps(u'hello'.encode('u8')) == '"hello"'


@pytest.mark.skipif(sys.version_info.major == 2,
                    reason="collections.abc requires python 3")
def test_generator():
    assert jason.dumps((i for i in range(0))) == '[]'


def test_jasonval():
    "Test the jasonval method."
    resp = jason.jsonval(['Hei', 'Verden', '2012'])
    print('response:', resp)
    r = str(resp.content)
    # print("CONTENT:", response.content)
    # print(dir(response))
    assert r.count('Hei') == 1
    assert r.count('Verden') == 1
    assert r.count('2012') == 1


def test_dictviews():
    a42 = dict(a=42)
    assert jason.json_eval(jason.dumps(a42.keys())) == ['a']
    assert jason.json_eval(jason.dumps(a42.values())) == [42]


def test_class_dumps():
    """Test the dump of the jason value of a class by using
       the __jason__ method.
    """
    class C:
        def __json__(self):
            return 42

    assert jason.dumps(C()) == '42'

    class D(object):
        def __init__(self):
            self.a = 42

    assert jason.json_eval(jason.dumps(D())) == {"a": 42}


def test_set_dumps():
    assert jason.json_eval(jason.dumps(1)) == 1
    assert jason.json_eval(jason.dumps(set())) == []
    assert jason.json_eval(jason.dumps({1, 2})) == [1, 2]
    assert jason.json_eval(jason.dumps(ttcal.Year(2017))) == {'year': 2017, 'kind': 'YEAR'}
    assert jason.dumps(ttcal.Duration.parse('1:10:01')) == '"@duration:4201"'
    assert jason.dumps(datetime.date(2019, 3, 15)) == '"@date:2019-03-15"'
    assert jason.json_eval(jason.dumps(datetime.time(hour=1, minute=10, second=1))) == {
        'hour': 1,
        'minute': 10,
        'second': 1,
        'microsecond': 0,
        'kind': 'TIME'
    }
    
    class Foo(object):
        __slots__ = ['a', 'b']
    
    with pytest.raises(TypeError):
        jason.dumps(Foo())  # not JSON serializable


@pytest.mark.skipif(sys.version_info.major == 2,
                    reason="collections.abc requires python 3")
def test_mapping():
    class Bar(collections.abc.Mapping):
        __slots__ = ['a']

        def __getitem__(self, item):  # pragma: nocover
            pass

        def __iter__(self):
            return iter([])

        def __len__(self):  # pragma: nocover
            return 0

    assert isinstance(Bar(), collections.abc.Mapping)
    assert jason.dumps(Bar()) == "{}"

    
def test_django_queryset_dumps():
    from django.contrib.auth.models import User
    assert jason.dumps(User.objects.none()) == '[]'


def test_loads():
    val = '{"k":"@datetime:1970-05-02T06:10:00"}'
    jval = jason.loads(val)
    assert jval['k'] == datetime.datetime(1970, 5, 2, 6, 10)

    val = '{"k":"@date:1970-05-02"}'
    jval = jason.loads(val)
    assert jval['k'] == datetime.date(1970, 5, 2)

    val = u'{"k":"@døte:1970-05-02"}'
    jval = jason.loads(val)
    assert not isinstance(jval['k'], datetime.date)

    val = u'{"k":"@date1970-05-02"}'
    jval = jason.loads(val)
    assert not isinstance(jval['k'], datetime.date)

    val = u'{"k":42}'
    jval = jason.loads(val)
    assert jval['k'] == 42

    val = b'{"k":42}'
    jval = jason.loads(val)
    assert jval['k'] == 42

    import json
    val = b'{"k":42}'
    jval = jason.loads(val, cls=json.JSONDecoder)
    assert jval['k'] == 42
    
    
def test_jsonname():
    assert jsonname("hello.world") == "hello_world"
    

def test_response(rf):
    request = rf.get('/')
    r = response(request, 42)
    assert r.status_code == 200
    assert r.content == b'42'
    
    request = rf.get('/?callback=cb')
    r = response(request, 42)
    assert r.status_code == 200
    assert r.content == b'cb(42)'
    

def test_jsonp():
    print("CONTENT:", jason.jsonp('cb', {'x':42}).content)
    # assert r'JSON.parse(val)}("{\"x\":42}")' in str(jason.jsonp('cb', {'x':42}).content)
    # assert 'cb(42)' in str(jason.jsonp('cb', 42).content)
    
    assert jason.jsonp('cb', {'x':42}).content.startswith(b'cb(function(val){return(dk&&dk.jason&&dk.jason.parse)?dk.jason.parse(val):JSON.parse(val)}')
    assert jason.jsonp('cb', 42).content == b'cb(42)'
    assert jason.jsonp('cb', 'hello').content == b'cb("hello")'
  
