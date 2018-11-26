#!/usr/bin/env python3
# Copyright (c) 2008-10 Qtrac Ltd. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.

"""Provides the Item example classes.
"""


class Item(object):  # 项

    def __init__(self, artist, title, year=None):
        self.__artist = artist  # artist::艺术家
        self.__title = title    # title::标题
        self.__year = year      # year::年代

    def artist(self):
        return self.__artist

    def setArtist(self, artist):
        self.__artist = artist

    def title(self):
        return self.__title

    def setTitle(self, title):
        self.__title = title

    def year(self):
        return self.__year

    def setYear(self, year):
        self.__year = year

    def __str__(self):
        year = ""
        if self.__year is not None:
            year = " in {}".format(self.__year)
        return "{} by {}{}".format(self.__title, self.__artist, year)


class Painting(Item):  # 油画

    def __init__(self, artist, title, year=None):
        super(Painting, self).__init__(artist, title, year)


class Sculpture(Item):  # 雕塑

    def __init__(self, artist, title, year=None, material=None):
        super(Sculpture, self).__init__(artist, title, year)
        self.__material = material  # material::材料

    def material(self):
        return self.__material

    def setMaterial(self, material):
        self.__material = material

    def __str__(self):
        materialString = ""
        if self.__material is not None:
            materialString = " ({})".format(self.__material)
        return "{}{}".format(super(Sculpture, self).__str__(),  # 调用父类__str__()方法.注意:不能调用str(self)会导至无限递归
                               materialString)


class Dimension(object):    # Dimension::尺寸|规格

    def __init__(self, width, height, depth=None):      # depth::深度
        self.__width = width
        self.__height = height
        self.__depth = depth

    def width(self):
        return self.__width

    def setWidth(self, width):
        self.__width = width

    def height(self):
        return self.__height

    def setHeight(self, height):
        self.__height = height

    def depth(self):
        return self.__depth

    def setDepth(self, depth):
        self.__depth = depth

    def area(self):  # area::面积
        raise NotImplemented        # NotImplemented::未执行 ???

    def volume(self):   # volume::体积
        raise NotImplemented



if __name__ == "__main__":
    items = []
    items.append(Painting("Cecil Collins", "The Poet", 1941))
    items.append(Painting("Cecil Collins", "The Sleeping Fool", 1943))
    items.append(Painting("Edvard Munch", "The Scream", 1893))
    items.append(Painting("Edvard Munch", "The Sick Child", 1896))
    items.append(Painting("Edvard Munch", "The Dance of Life", 1900))
    items.append(Sculpture("Auguste Rodin", "Eternal Springtime", 1917,
                           "plaster"))
    items.append(Sculpture("Auguste Rodin", "Naked Balzac", 1917,
                           "plaster"))
    items.append(Sculpture("Auguste Rodin", "The Secret", 1925,
                           "bronze"))
    uniquematerials = set()
    for item in items:
        print(item)
        if hasattr(item, "material"):
            uniquematerials.add(item.material())
    print("Sculptures use {} unique materials".format(
          len(uniquematerials)))

