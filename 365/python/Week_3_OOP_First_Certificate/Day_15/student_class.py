class Student:
    def __init__(self,name,age,grade,roll):
        self.name=name
        self.age=age
        self.grade=grade
        self.roll=roll
    
    def display_info(self):
        print(f"Name:{self.name}, Age:{self.age}, Grade:{self.grade}, Roll:{self.roll}\n")
    
    def update_grade(self,new_grade):
        self.grade=new_grade
        print(f"Grade Improved to {self.grade}")

    def is_adult(self):
        return self.age>=18
    
    def study_hours(self, hours):
        print(f"{self.name} studied for {hours} hours")


# Create students
student1 = Student("Alice", 20, "A", 101)
student2 = Student("Bob", 17, "B", 102)
student3 = Student("Charlie", 19, "C", 103)

# Test display
student1.display_info()

# Test update grade
student1.update_grade("A+")

# Test is adult
print(student2.is_adult())  # Should be False
print(student1.is_adult())  # Should be True

# Test study hours
student3.study_hours(5)
