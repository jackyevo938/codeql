import sys

from swift.codegen.test.utils import *

root_name = schema.root_class_name


@pytest.fixture
def load(tmp_path):
    file = tmp_path / "schema.yml"

    def ret(yml):
        write(file, yml)
        return schema.load(file)

    return ret


def test_empty_schema(load):
    ret = load("{}")
    assert ret.classes == [schema.Class(root_name)]
    assert ret.includes == set()


def test_one_empty_class(load):
    ret = load("""
MyClass: {}
""")
    assert ret.classes == [
        schema.Class(root_name, derived={'MyClass'}),
        schema.Class('MyClass', bases={root_name}),
    ]


def test_two_empty_classes(load):
    ret = load("""
MyClass1: {}
MyClass2: {}
""")
    assert ret.classes == [
        schema.Class(root_name, derived={'MyClass1', 'MyClass2'}),
        schema.Class('MyClass1', bases={root_name}),
        schema.Class('MyClass2', bases={root_name}),
    ]


def test_two_empty_chained_classes(load):
    ret = load("""
MyClass1: {}
MyClass2:
    _extends: MyClass1
""")
    assert ret.classes == [
        schema.Class(root_name, derived={'MyClass1'}),
        schema.Class('MyClass1', bases={root_name}, derived={'MyClass2'}),
        schema.Class('MyClass2', bases={'MyClass1'}),
    ]


def test_empty_classes_diamond(load):
    ret = load("""
A: {}
B: {}
C:
    _extends: 
        - A
        - B
""")
    assert ret.classes == [
        schema.Class(root_name, derived={'A', 'B'}),
        schema.Class('A', bases={root_name}, derived={'C'}),
        schema.Class('B', bases={root_name}, derived={'C'}),
        schema.Class('C', bases={'A', 'B'}),
    ]


def test_dir(load):
    ret = load("""
A:
    _dir: other/dir
""")
    assert ret.classes == [
        schema.Class(root_name, derived={'A'}),
        schema.Class('A', bases={root_name}, dir=pathlib.Path("other/dir")),
    ]


def test_directory_filter(load):
    ret = load("""
_directories:
    first/dir: '[xy]'
    second/dir: foo$
    third/dir: bar$
Afoo: {}
Bbar: {}
Abar: {}
Bfoo: {}
Ax: {}
Ay: {}
A: {}
""")
    assert ret.classes == [
        schema.Class(root_name, derived={'Afoo', 'Bbar', 'Abar', 'Bfoo', 'Ax', 'Ay', 'A'}),
        schema.Class('Afoo', bases={root_name}, dir=pathlib.Path("second/dir")),
        schema.Class('Bbar', bases={root_name}, dir=pathlib.Path("third/dir")),
        schema.Class('Abar', bases={root_name}, dir=pathlib.Path("third/dir")),
        schema.Class('Bfoo', bases={root_name}, dir=pathlib.Path("second/dir")),
        schema.Class('Ax', bases={root_name}, dir=pathlib.Path("first/dir")),
        schema.Class('Ay', bases={root_name}, dir=pathlib.Path("first/dir")),
        schema.Class('A', bases={root_name}, dir=pathlib.Path()),
    ]


def test_directory_filter_override(load):
    ret = load("""
_directories:
    one/dir: ^A$
A:
    _dir: other/dir
""")
    assert ret.classes == [
        schema.Class(root_name, derived={'A'}),
        schema.Class('A', bases={root_name}, dir=pathlib.Path("other/dir")),
    ]


def test_lowercase_rejected(load):
    with pytest.raises(AssertionError):
        load("aLowercase: {}")


def test_digit_rejected(load):
    with pytest.raises(AssertionError):
        load("1digit: {}")


def test_properties(load):
    ret = load("""
A:
     one: string
     two: int?
     three: bool*
     four: x?*
     five: predicate
""")
    assert ret.classes == [
        schema.Class(root_name, derived={'A'}),
        schema.Class('A', bases={root_name}, properties=[
            schema.SingleProperty('one', 'string'),
            schema.OptionalProperty('two', 'int'),
            schema.RepeatedProperty('three', 'bool'),
            schema.RepeatedOptionalProperty('four', 'x'),
            schema.PredicateProperty('five'),
        ]),
    ]


def test_element_properties(load):
    ret = load("""
Element:
    x: string
""")
    assert ret.classes == [
        schema.Class(root_name, properties=[
            schema.SingleProperty('x', 'string'),
         ]),
    ]


if __name__ == '__main__':
    sys.exit(pytest.main([__file__] + sys.argv[1:]))
