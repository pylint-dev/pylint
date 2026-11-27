"""Check that no-member is not emitted for the attributes of a ``type`` statement
alias, which is a ``typing.TypeAliasType`` at runtime (issue #10091)."""

type Alias = str
type GenericAlias[T] = list[T]

print(Alias.__value__)
print(GenericAlias.__value__)
print(Alias.nonexistent)  # [no-member]

NotAnAlias = str
print(NotAnAlias.__value__)  # [no-member]
