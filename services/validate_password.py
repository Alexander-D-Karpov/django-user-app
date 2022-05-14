from common.error import ValidatorException
from user.services.validators import RegexValidator, ValidatorChain


def validate_password(password: str) -> None:
    num_validator = RegexValidator(
        "\d",
        ValidatorException("The password must contain at least 1 number", "NumPas"),
    )
    uppercase_validator = RegexValidator(
        "[A-Z]",
        ValidatorException(
            "The password must contain at least 1 UPPERCASE symbol", "UpPas"
        ),
    )
    special_character_validator = RegexValidator(
        "[()[\]{}|\\`~!@#$%^&*_\-+=;:'\",<>./?]",
        ValidatorException(
            "The password must contain at least 1 special character: "
            + """()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?""",
            "SpecPas",
        ),
    )

    chain = ValidatorChain(
        [num_validator, uppercase_validator, special_character_validator]
    )

    chain.check(password)
