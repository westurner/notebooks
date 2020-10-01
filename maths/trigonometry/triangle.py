#!/usr/bin/env python3
"""
trigonometry --  a module for trigonometry
"""

import math


class Triangle:
    def __init__(self, sides=None, angles=None):
        """
        Kwargs:
            sides (dict or None):
        """
        self._side_names = ["a", "b", "c"]

        self.__sides = sides
        self._sides = self.to_params_dict(sides, self._side_names)
        self.sides = None

        self.__angles = angles
        self._angles = self.to_params_dict(sides, self._side_names)
        self.angles = None

        self.solve()

    @staticmethod
    def to_params_dict(arg, keys):
        if arg is None:
            return arg
        if hasattr(arg, "keys"):  # isinstance(arg, dict)
            if not any(ekey in arg for ekey in keys):
                raise ValueError(
                    ("No known side names were specified:", (arg, keys))
                )
            return arg
        if isinstance(arg, (tuple, list)):
            return dict(zip(keys, arg))
        else:
            raise ValueError(("Argument format is not supported", arg))

    @property
    def all_sides_specified(self):
        return (
            self._sides
            and len(self._sides) == 3
            and all(v is not None for v in self._sides.values())
        )

    @property
    def all_angles_specified(self):
        return (
            self._angles
            and len(self._angles) == 3
            and all(v is not None for v in self._angles.values())
        )

    def solve(self):
        raise NotImplementedError("RightTriangle subclasses only for now")


class RightTriangle(Triangle):
    def __init__(self, sides=None, angles=None):
        self.__sides = sides
        self._sides = self.to_params_dict(sides, keys=["h", "a", "b"])
        if "h" not in self._sides:
            raise ValueError("Must specify a side named h")
        self.sides = None

        self.__angles = angles
        self._angles = self.to_params_dict(angles, keys=["oh", "a", "b"])
        self.angles = None

        self.solve()

    def solve(self):
        # a2 + b2 = c2
        if self.all_sides_specified:
            self.sides = self._sides
        else:
            unknown_sides = set(self._side_keys).difference(self._sides.keys())
            # unknown_sides = [x for x in self._side_keys
            #    if x not in self._sides]
            # a**2 + b**2 = c**2
            # a = sqrt(c) -
            if len(unknown_sides) == 1:
                if "h" in self._sides:
                    unknown_sides[:]
                    unknownsidekey = (unknown_sides - set(("h",)))[0]
                    unknownsidelength = math.sqrt(self._sides["h"]) - self._sides[othersidekey]

        if self.all_angles_specified:
            self.angles = self._angles


from itertools import zip_longest
import pytest


@pytest.mark.parametrize(
    "sides,angles,output",
    [[[3, 4, 5], None, dict(sides=[3, 4, 5], angles=[None, 90, None])]],
)
def test_right_triangle1(sides, angles, output):
    t = RightTriangle(sides, angles)
    o_sides = output.get("sides")
    if o_sides:
        assert t.sides is not None
        assert list(t.sides.values()) == o_sides
    o_angles = output.get("angles")
    if o_angles:
        assert t.angles is not None
        assert list(t.angles.values()) == o_angles
