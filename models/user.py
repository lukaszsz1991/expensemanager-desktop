class User:
    def __init__(self, id: str, email: str, first_name: str, last_name: str):
        self.id = id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return f"User(id={self.id}, email={self.email}, name={self.first_name} {self.last_name})"
