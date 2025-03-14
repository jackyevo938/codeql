import pathlib
from dataclasses import dataclass, field
from typing import List, ClassVar

import inflection


@dataclass
class Param:
    param: str
    first: bool = False


@dataclass
class Property:
    singular: str
    type: str = None
    tablename: str = None
    tableparams: List[Param] = field(default_factory=list)
    plural: str = None
    first: bool = False
    local_var: str = "x"
    is_optional: bool = False
    is_predicate: bool = False

    def __post_init__(self):
        if self.tableparams:
            if self.type_is_class:
                self.tableparams = [x if x != "result" else self.local_var for x in self.tableparams]
            self.tableparams = [Param(x) for x in self.tableparams]
            self.tableparams[0].first = True

    @property
    def getter(self):
        return f"get{self.singular}" if not self.is_predicate else self.singular

    @property
    def indefinite_getter(self):
        if self.plural:
            article = "An" if self.singular[0] in "AEIO" else "A"
            return f"get{article}{self.singular}"

    @property
    def type_is_class(self):
        return bool(self.type) and self.type[0].isupper()

    @property
    def is_repeated(self):
        return bool(self.plural)


@dataclass
class Class:
    template: ClassVar = 'ql_class'

    name: str
    bases: List[str] = field(default_factory=list)
    final: bool = False
    properties: List[Property] = field(default_factory=list)
    dir: pathlib.Path = pathlib.Path()
    imports: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.bases = sorted(self.bases)
        if self.properties:
            self.properties[0].first = True

    @property
    def db_id(self):
        return "@" + inflection.underscore(self.name)

    @property
    def root(self):
        return not self.bases

    @property
    def path(self):
        return self.dir / self.name


@dataclass
class Stub:
    template: ClassVar = 'ql_stub'

    name: str
    base_import: str


@dataclass
class ImportList:
    template: ClassVar = 'ql_imports'

    imports: List[str] = field(default_factory=list)
