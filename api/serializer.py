from rest_framework import serializers
from .models import PDFData
from bson import ObjectId


class ObjectIdField(serializers.Field):
    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        try:
            return ObjectId(data)
        except Exception:
            raise serializers.ValidationError("Invalid ObjectId")


class PDFDataSerializer(serializers.ModelSerializer):
    id = ObjectIdField(source='_id', read_only=True)

    class Meta:
        model = PDFData
        fields = '__all__'