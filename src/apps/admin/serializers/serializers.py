from rest_framework import serializers

from apps.accounts.validators import MinMaxLengthPasswordValidator


class GeneratePasswordSerializer(serializers.Serializer):
    length_password = serializers.IntegerField()

    def validate_length_password(self, value: int) -> int:
        """"""
        validator = MinMaxLengthPasswordValidator()
        min_length_password = validator.min_length
        max_length_password = validator.max_length

        if not (min_length_password <= value <= max_length_password):
            raise serializers.ValidationError(
                f"Длина пароля должна быть от {min_length_password} до {max_length_password} символов."
            )

        return value
