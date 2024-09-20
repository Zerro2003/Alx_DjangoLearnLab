
### Retrieve Operation

1. **Command**: Retrieve and display the book's attributes.
2. **Document in**: `retrieve.md`

**Example for `retrieve.md`:**

```markdown
# Retrieve Operation

```python
book = Book.objects.get(title="1984")
print(book.title, book.author, book.publication_year)
