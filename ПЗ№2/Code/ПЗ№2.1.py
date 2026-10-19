class MyTest:
    def get_average(self, *args):
        return sum(args) / len(args)
numbers = []
while True:
    a = input("Введите число: ")
    if a == "":
        break
    numbers.append(float(a))
test = MyTest()
print(test.get_average(*numbers))
