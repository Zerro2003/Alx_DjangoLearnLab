
### Delete Operation

1. **Command**: Delete the book and confirm deletion.
2. **Document in**: `delete.md`

**Example for `delete.md`:**

```markdown
# Delete Operation

```python
from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
