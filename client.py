class Client:

    def __init__(self, name, email, phone_number):
        self.name = name
        self.email = email
        self.phone_number = phone_number

    def edit(self, name, email, phone_number):
        self.name = name
        self.email = email
        self.phone_number = phone_number

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if not name:
            raise ValueError("Missing name")
        self._name = name

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        if not email:
            raise ValueError("Missing email")
        self._email = email

    @property
    def phone_number(self):
        return self._phone_number

    @phone_number.setter
    def phone_number(self, phone_number):
        if not phone_number:
            raise ValueError("Missing phone number")
        self._phone_number = phone_number