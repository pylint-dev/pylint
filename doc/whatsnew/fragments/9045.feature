Enhanced pyreverse to properly distinguish between UML relationship types (association, aggregation, composition) based on object ownership semantics. Type annotations without assignment are now treated as associations, parameter assignments as aggregations, and object instantiation as compositions.

Closes #9045
Closes #9267
