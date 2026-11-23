<!-- pyreverse-primer-comment -->
🤖 **Effect of this PR on tracked pyreverse diagrams:** 🤖

**Effect on `ClassDef` in [astroid](https://github.com/pylint-dev/astroid):**

<details>
<summary>Diagram diff</summary>

```diff
--- main
+++ pr
@@ -29,12 +29,15 @@
   }
   class ClassDef {
   }
+  class Decorators {
+  }
   BaseInstance --|> Proxy
   Instance --|> BaseInstance
   ClassModel --|> ObjectModel
   InstanceModel --|> ObjectModel
   FilterStmtsBaseNode --|> NodeNG
   LookupMixIn --|> NodeNG
+  Decorators --|> NodeNG
   Statement --|> NodeNG
   LocalsDictNodeNG --|> LookupMixIn
   ClassDef --|> FilterStmtsBaseNode
@@ -46,6 +49,7 @@
   InferenceContext --* ClassModel : context
   ClassModel --* ClassDef : special_attributes
   InstanceModel --* Instance : special_attributes
+  Decorators --o ClassDef : decorators
   Union --o InferenceContext : boundnode
   Instance --o InferenceContext : boundnode
   InferenceContext --o InferenceContext : boundnode
```
</details>

<details>
<summary>Rendered diagram after this change</summary>

```mermaid
classDiagram
  class Union {
  }
  class BaseInstance {
  }
  class Instance {
  }
  class Proxy {
  }
  class CallContext {
  }
  class InferenceContext {
  }
  class ClassModel {
  }
  class InstanceModel {
  }
  class ObjectModel {
  }
  class FilterStmtsBaseNode {
  }
  class LookupMixIn {
  }
  class Statement {
  }
  class NodeNG {
  }
  class LocalsDictNodeNG {
  }
  class ClassDef {
  }
  class Decorators {
  }
  BaseInstance --|> Proxy
  Instance --|> BaseInstance
  ClassModel --|> ObjectModel
  InstanceModel --|> ObjectModel
  FilterStmtsBaseNode --|> NodeNG
  LookupMixIn --|> NodeNG
  Decorators --|> NodeNG
  Statement --|> NodeNG
  LocalsDictNodeNG --|> LookupMixIn
  ClassDef --|> FilterStmtsBaseNode
  ClassDef --|> Statement
  ClassDef --|> LocalsDictNodeNG
  BaseInstance --> ObjectModel : special_attributes
  ClassDef --> NodeNG : instance_attrs
  CallContext --* InferenceContext : callcontext
  InferenceContext --* ClassModel : context
  ClassModel --* ClassDef : special_attributes
  InstanceModel --* Instance : special_attributes
  Decorators --o ClassDef : decorators
  Union --o InferenceContext : boundnode
  Instance --o InferenceContext : boundnode
  InferenceContext --o InferenceContext : boundnode
```
</details>

**Effect on `FunctionDef` in [astroid](https://github.com/pylint-dev/astroid):**

<details>
<summary>Diagram diff</summary>

```diff
--- main
+++ pr
@@ -21,6 +21,12 @@
   }
   class FunctionDef {
   }
+  class CallContext {
+  }
+  class ClassDef {
+  }
+  class InferenceContext {
+  }
   FunctionModel --|> ObjectModel
   AssignTypeNode --|> NodeNG
   FilterStmtsBaseNode --|> NodeNG
@@ -33,6 +39,13 @@
   FunctionDef --|> MultiLineBlockNode
   FunctionDef --|> Statement
   FunctionDef --|> LocalsDictNodeNG
+  ClassDef --|> FilterStmtsBaseNode
+  ClassDef --|> Statement
+  ClassDef --|> LocalsDictNodeNG
   FunctionModel --* FunctionDef : special_attributes
+  CallContext --* InferenceContext : callcontext
+  ClassDef --> NodeNG : instance_attrs
   Arguments --o FunctionDef : args
   NodeNG --o FunctionDef : body
+  ClassDef --o InferenceContext : boundnode
+  ClassDef --o FunctionDef : parent
```
</details>

<details>
<summary>Rendered diagram after this change</summary>

```mermaid
classDiagram
  class FunctionModel {
  }
  class ObjectModel {
  }
  class AssignTypeNode {
  }
  class FilterStmtsBaseNode {
  }
  class LookupMixIn {
  }
  class MultiLineBlockNode {
  }
  class Statement {
  }
  class Arguments {
  }
  class NodeNG {
  }
  class LocalsDictNodeNG {
  }
  class FunctionDef {
  }
  class CallContext {
  }
  class ClassDef {
  }
  class InferenceContext {
  }
  FunctionModel --|> ObjectModel
  AssignTypeNode --|> NodeNG
  FilterStmtsBaseNode --|> NodeNG
  LookupMixIn --|> NodeNG
  MultiLineBlockNode --|> NodeNG
  Statement --|> NodeNG
  Arguments --|> AssignTypeNode
  LocalsDictNodeNG --|> LookupMixIn
  FunctionDef --|> FilterStmtsBaseNode
  FunctionDef --|> MultiLineBlockNode
  FunctionDef --|> Statement
  FunctionDef --|> LocalsDictNodeNG
  ClassDef --|> FilterStmtsBaseNode
  ClassDef --|> Statement
  ClassDef --|> LocalsDictNodeNG
  FunctionModel --* FunctionDef : special_attributes
  CallContext --* InferenceContext : callcontext
  ClassDef --> NodeNG : instance_attrs
  Arguments --o FunctionDef : args
  NodeNG --o FunctionDef : body
  ClassDef --o InferenceContext : boundnode
  ClassDef --o FunctionDef : parent
```
</details>

*This comment was generated for commit deadbeef*
