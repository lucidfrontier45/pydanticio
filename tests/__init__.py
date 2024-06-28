from pydantic import BaseModel, ConfigDict


class TestClass(BaseModel):
    model_config = ConfigDict(frozen=True)

    a: int
    b: int
    s: str
    x: float
    y: float

    def get_csv_header(self):
        return "a,b,s,x,y"

    def to_csv_row(self):
        return f"{self.a},{self.b},{self.s},{self.x},{self.y}"


test_records = [
    TestClass(a=1, b=2, s="hello", x=3.14, y=2.71),
    TestClass(a=2, b=3, s="world", x=2.71, y=3.14),
]
