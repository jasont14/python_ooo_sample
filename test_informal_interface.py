import pytest
from informal_interface import Circle, Square, Rectangle, Sphere, AreaCalculator, VolumeCalculator, CalcOutput

def test_circle_area():
    c = Circle(5)
    assert c.area() == 78.5

def test_square_area():
    s = Square(2)
    assert s.area() == 4

def test_rectangle_area():
    r = Rectangle(3,4)
    assert r.area() == 12

def test_sphere_area():
    s = Sphere(5)
    assert s.area() == 314.0

def test_area_calculator():
    shapes = [
        Square(2),
        Circle(5),
        Rectangle(3,4),
        Sphere(5)
    ]
    ac = AreaCalculator(shapes)
    assert ac.area_sum() == 408.5

def test_volume_calculator():
    shapes = [
        Square(2),
        Circle(5),
        Rectangle(3,4),
        Sphere(5)
    ]
    vc = VolumeCalculator(shapes)
    assert round(vc.volume_sum(),2) == 523.33

def test_calc_output():
    shapes = [
        Square(2),
        Circle(5),
        Rectangle(3,4),
        Sphere(5)
    ]
    ac = AreaCalculator(shapes)
    vc = VolumeCalculator(shapes)
    area_calc = ac.area_sum()    
    volume_calc = vc.volume_sum()
    resp = CalcOutput(volume_calc, area_calc)
    assert resp.area == 408.5 and resp.volume == 523.33
    