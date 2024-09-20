
### Update Operation

1. **Command**: Update the book's title.
2. **Document in**: `update.md`

**Example for `update.md`:**

```markdown
# Update Operation

```python
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
print(book.title)
