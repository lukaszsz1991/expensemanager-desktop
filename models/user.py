class User:
    def __init__(self, id: str, email: str, role: str = "", created_at: str = ""):
        self.id = id
        self.email = email
        self.role = role
        self.created_at = created_at

    def __repr__(self):
        return f"User(id={self.id}, email={self.email}, role={self.role})"