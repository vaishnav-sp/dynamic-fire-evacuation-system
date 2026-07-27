from dataclasses import dataclass


@dataclass
class Exit:
    id: str
    name: str

    # Exit Status
    is_open: bool = True
    is_accessible: bool = True

    # Information
    connected_to: str = ""

    def __str__(self):
        status = "OPEN" if self.is_open else "CLOSED"

        return (
            f"{self.id} | "
            f"{self.name} | "
            f"{status}"
        )