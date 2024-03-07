from django.core.validators import RegexValidator

regex_validator_email = RegexValidator(
    "^(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])$",
    message="Incorrect expression of e-mail.",
)
regex_validator_login = RegexValidator(
    "^(?=.*?[a-zA-Z\d])[a-zA-Z][a-zA-Z\d_-]{2,28}[a-zA-Z\d]$",
    message="Login must be between 4 and 30 characters long and must start with a letter and end with a letter or number. It can contain a floor and dash between the start and end.",
)
regex_validator_password = RegexValidator(
    "^(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[0-9])(?=.*?[.~!@#$%^&*()+=[\]\\;:'\"/,|{}<>?])[a-zA-Z0-9.~!@#$%^&*()+=[\]\\;:'\"/,|{}<>?]{8,40}$",
    message="Password must be between 8 and 40 characters long, contain one lowercase and one uppercase letter, one number and one special character.",
)
regex_validator_nickname = RegexValidator(
    "^[a-zA-Z]\w{2,}$", message="Incorrect expression of nickname."
)
