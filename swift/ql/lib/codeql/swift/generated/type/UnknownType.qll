// generated by codegen/codegen.py
import codeql.swift.elements.type.Type

class UnknownTypeBase extends @unknown_type, Type {
  override string getAPrimaryQlClass() { result = "UnknownType" }

  string getName() { unknown_types(this, result) }
}
