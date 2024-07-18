# Code sample

# Given a 2-d shape and 3-d shape., output the total area and volume of all shapes as json or html.
# two examples with one using informal interface and formal interface.
# Import modules when needed
# Values:   Circle radius = 5, Square side  = 2, Rectangle length = 3, width = 4, Spehere radius = 5

import json
import abc
from tabulate import tabulate


# I - Interface Segregation - Shape and ShapeThreeD are interfaces.  ShapeThreeD includes volume.  Not all shapes have volume.
# O - Open/Closed Principle - open for extension but closed for modification. shape class makes sure objects of type shape implement defined.
class Shape(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass: type) -> bool:
        return (hasattr(subclass, 'area') and callable(subclass.area))

    @abc.abstractmethod
    def area(self):
        """returns the area of a shape: square, triangle, circle"""
        pass    

# L - Liskov Substitution - Sphere is a 3d shape with volume and area.  It can be used in place of a shape.  It has a volume and area
class ShapeThreeD(Shape):
    @classmethod
    def __subclasshook__(cls, subclass: type) -> bool:
        return (hasattr(subclass, 'volume') and callable(subclass.volume) and
                hasattr(subclass, 'area') and callable(subclass.area)
        )
    
    @abc.abstractmethod
    def volume(self):
        """returns the volume of a shape: cube, sphere, cone"""
        pass

#S - Single Responsibility  - Class does one thing holds value and calculates area.
class Square(Shape):
    def __init__(self, length):
        self.length = length

    def area(self):
        return self.length ** 2

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius ** 2
    
class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width
    
class Sphere(ShapeThreeD, Shape):
    def __init__(self, radius):
        self.radius = radius

    def volume(self):
        return 4/3 * 3.14 * self.radius ** 3

    #surface area of sphere
    def area(self):
        return 4 * 3.14 * self.radius ** 2
    
# O open closed -  open for extension but closed for modification. AreaCalculator accepts array of Shape. If additional shapes
# are added, the class does not need to be modified. 
# D Dependency Inversion - AreaCalculator depends on Shape interface. It does not depend on specific shapes.

class AreaCalculator:
    def __init__(self, shapes):
        self.shapes = shapes

    def calc(self, shape:Shape):
        return shape.area()

    def area_sum(self):
        # Return sum of all shapes areas
        areas = []        
        for shape in self.shapes:
            if isinstance(shape, Shape): #Remember Sphere is a 3dShape which is a shape #Liskov Substitution 
                areas.append(self.calc(shape))   #Dependency Inversion              
            else:
                raise TypeError(f'{shape} is not a shape')
        
        return sum(areas)

class VolumeCalculator:
    def __init__(self, shapes):
        self.shapes = shapes

    def calc(self, shape:ShapeThreeD):
        return shape.volume()

    def volume_sum(self):
        # Return sum of all shapes areas
        volumes = []
        for shape in self.shapes:
            if isinstance(shape, ShapeThreeD):
                volumes.append(self.calc(shape)) #Dependency Inversion - VolumeCalculator depends on ShapeThreeD interface. It does not depend on specific shapes.
            else:
                volumes.append(0)
        
        return sum(volumes)
    
class DisplayRules:
    def rounding_rules(value):
        return round(value, 2)
    
class CalcOutput:
    def __init__(self, volume, area):
        self.area = DisplayRules.rounding_rules(area) if isinstance(area, (float, float)) else 0
        self.volume = DisplayRules.rounding_rules(volume) if isinstance(volume, (float, float)) else 0        
    
    def to_json(self):        
        
        result = f'{{"total_area": {self.area}, "total_volume": {self.volume}}}'
        return result

    def to_html(self):
        #lol = list of lists for tabulate
        lol = []
        result = []
        
        result.append(f'[{self.area}, {self.volume}]')
        lol = [result]
        html = tabulate(lol, headers=['Total Area', 'Total Volume'], tablefmt='html')
        
        return html

class bo(ShapeThreeD):
    def volume(self):
        pass

def main(shapes):

    area_calc = AreaCalculator(shapes).area_sum()    
    volume_calc = VolumeCalculator(shapes).volume_sum()
    resp = CalcOutput(area_calc, volume_calc)

    htm = resp.to_html()
    jsn = resp.to_json()
    print(f"htm: {htm}")
    print(f"jsn: {jsn}")

    print(issubclass(bo, ShapeThreeD))
    print(issubclass(Sphere, ShapeThreeD))
    print(issubclass(Square, Shape))

    return resp    

if __name__ == '__main__':

    shapes = [   
        Square(2),
        Circle(5),
        Rectangle(3,4),
        Sphere(5)
    ]

    main(shapes)

