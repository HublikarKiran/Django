# API Serializer Notes

## What A Serializer Is

In Django REST Framework, a serializer converts complex Django objects into simple data types such as dictionaries and lists. These simple data types can then be rendered as JSON.

Serializers also validate incoming API data before saving it to the database.

In short:

- model to JSON: serializer output
- JSON to model: serializer validation and save

## Where Serializers Are Configured In This Project

Main file:

```text
studentsystem/api/serializers.py
```

The API views import serializers from this file:

```text
studentsystem/api/views.py
```

Example:

```python
from .serializers import UserSerializer, SubjectSerializer
```

## Serializer Base Class Used

This project uses:

```python
serializers.ModelSerializer
```

`ModelSerializer` automatically creates serializer fields from Django model fields.

Example:

```python
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'
        read_only_fields = ['created_by']
```

Meaning:

- use the `Subject` model
- include all model fields
- do not allow API clients to manually set `created_by`

## Serializers In This Project

Configured in:

```text
studentsystem/api/serializers.py
```

Current serializers:

```text
UserSerializer
StudentProfileSerializer
SubjectSerializer
StudyMaterialsSerializer
AssignmentSerializer
AssignmentSubmissionSerializer
ChatMessageSerializer
AttendanceRecordSerializer
ResultSerializer
NotificationSerializer
PlacementOpportunitySerializer
PlacementApplicationSerializer
AdmissionApplicationSerializer
FacultyProfileSerializer
ParentProfileSerializer
```

## UserSerializer

Code location:

```text
studentsystem/api/serializers.py
```

Important fields:

```python
fields = [
    'id',
    'username',
    'password',
    'email',
    'first_name',
    'last_name',
    'phone_number',
    'role',
    'is_verified',
    'is_active',
]
```

Special behavior:

```python
password = serializers.CharField(write_only=True, required=False)
```

Meaning:

- password can be sent to the API
- password is not returned in API responses

The `create()` method uses:

```python
user.set_password(password)
```

This is important because passwords must be hashed. Never save a plain password directly.

The `update()` method also uses `set_password()` if a new password is provided.

## Read-Only Serializer Fields

Some fields are controlled by server-side code, not by the API client.

Examples:

```python
read_only_fields = ['created_by']
read_only_fields = ['uploaded_by']
read_only_fields = ['student']
read_only_fields = ['user', 'answer']
```

Project examples:

- `SubjectSerializer`: `created_by` is set in `SubjectViewSet.perform_create()`.
- `StudyMaterialsSerializer`: `uploaded_by` is set in `StudyMaterialsViewSet.perform_create()`.
- `AssignmentSerializer`: `created_by` is set in `AssignmentViewSet.perform_create()`.
- `AssignmentSubmissionSerializer`: `student` is set from `request.user`.
- `ChatMessageSerializer`: `user` and `answer` are set by server code.

## How Serializers Connect To ViewSets

Configured in:

```text
studentsystem/api/views.py
```

Example:

```python
class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all().order_by('name')
    serializer_class = SubjectSerializer
    permission_classes = [AdminWritePermission]
```

DRF uses `serializer_class` to:

- format API response data
- validate request body data
- create model objects
- update model objects

## Example API Input And Serializer Work

Request:

```json
{
  "name": "Django",
  "description": "Web framework"
}
```

Flow:

1. API request reaches `SubjectViewSet`.
2. DRF passes JSON data to `SubjectSerializer`.
3. Serializer validates fields against the `Subject` model.
4. `perform_create()` saves `created_by=request.user`.
5. Response returns serialized subject data.

## Serializer Validation

This project mainly relies on model-level validation from `ModelSerializer`.

You can add custom validation like this:

```python
def validate_name(self, value):
    if len(value) < 3:
        raise serializers.ValidationError("Name must have at least 3 characters.")
    return value
```

Or object-level validation:

```python
def validate(self, attrs):
    if attrs["start_date"] > attrs["end_date"]:
        raise serializers.ValidationError("Start date must be before end date.")
    return attrs
```

## Best Practices

- Keep passwords `write_only=True`.
- Use `read_only_fields` for fields that must come from the server.
- Use `perform_create()` in viewsets for user-owned fields.
- Do not expose sensitive fields unless required.
- Add custom validation when business rules are not fully represented by the model.

