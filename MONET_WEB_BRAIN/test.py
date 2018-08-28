class Parent:
    def __init__(self, name):
        self.name = name


class Child(Parent):
    def __init__(self, is_done):
        self.done = is_done

a = Parent('a')
b = Child(True)

print(b.name)
print(b.done)

