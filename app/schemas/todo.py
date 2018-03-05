from marshmallow import fields
from .. import ma

from ..models.todo import todo

class TodoSchema(ma.ModelSchema):

    class Meta:
        model = Todo


todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)
