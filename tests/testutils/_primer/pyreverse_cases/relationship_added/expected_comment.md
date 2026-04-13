<!-- pyreverse-primer-comment -->
🤖 **Effect of this PR on tracked pyreverse diagrams:** 🤖

**Effect on `ClassDef` in [astroid](https://github.com/pylint-dev/astroid):**

<details>
<summary>Diagram diff</summary>

```diff
--- main
+++ pr
@@ -1,3 +1,6 @@
 classDiagram
   class ClassDef {
   }
+  class NodeNG {
+  }
+  ClassDef --|> NodeNG
```
</details>

<details>
<summary>Rendered diagram</summary>

```mermaid
classDiagram
  class ClassDef {
  }
  class NodeNG {
  }
  ClassDef --|> NodeNG
```
</details>

*This comment was generated for commit deadbeef*
