# Permissions and Groups Setup

This Django application uses custom permissions and groups to control access to certain parts of the application.

## Custom Permissions

The `Book` model has the following custom permissions:

- `can_view`: Allows viewing of books.
- `can_create`: Allows creation of new books.
- `can_edit`: Allows editing of existing books.
- `can_delete`: Allows deletion of books.

## Groups

Three user groups have been set up:

- **Viewers**: Can only view books.
- **Editors**: Can view, create, and edit books.
- **Admins**: Can perform all actions, including deleting books.

## Permission Enforcement

The views in the application use the `@permission_required` decorator to enforce these permissions. Users must belong to the appropriate group to access certain views.

For example:

- The `book_edit` view is protected by the `can_edit` permission.
- The `book_delete` view is protected by the `can_delete` permission.

