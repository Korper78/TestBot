from sqlalchemy import Column, INTEGER, SmallInteger, VARCHAR, ForeignKey, Integer, Boolean
from sqlalchemy.orm import declarative_base

TGBase = declarative_base()


class Foundation(TGBase):
    __tablename__: str = 'foundations'
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(24), nullable=False, unique=True)
    address = Column(VARCHAR(100), nullable=False, unique=True)


    def __repr__(self):
        return f'Контора:{self.id}-{self.name}-{self.address}'


class ProductionArea(TGBase):
    __tablename__: str = 'production_areas'
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(24), nullable=False)
    foundation_id = Column(INTEGER, ForeignKey('foundations.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return f'Производство:{self.id}-{self.name}'


class Storage(TGBase):
    __tablename__: str = 'storages'
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(24), nullable=False)
    address = Column(VARCHAR(100), nullable=False, unique=True)
    foundation_id = Column(INTEGER, ForeignKey('foundations.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return f'Склад:{self.id}-{self.name}'


class Category(TGBase):
    __tablename__: str = 'categories'
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(32), nullable=False)
    parent_id = Column(INTEGER, ForeignKey('categories.id', ondelete='CASCADE'))

    def __repr__(self):
        return f'Категория:{self.id}-{self.name}'


class RawMaterial(TGBase):
    __tablename__: str = 'raw_materials'
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(32), nullable=False, unique=True)

    def __repr__(self):
        return f'Сырье/товар:{self.id}-{self.name}'


class Product(TGBase):
    __tablename__: str = 'products'
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    amount = Column(Integer, default=0)
    material_id = Column(INTEGER, ForeignKey('raw_materials.id', ondelete='CASCADE'), nullable=False)
    category_id = Column(INTEGER, ForeignKey('categories.id', ondelete='CASCADE'), nullable=False)
    storage_id = Column(INTEGER, ForeignKey('storages.id', ondelete='CASCADE'))
    production_area_id = Column(INTEGER, ForeignKey('production_areas.id', ondelete='CASCADE'))
    is_shipment = Column(Boolean, default=False)


class Role(TGBase):
    __tablename__: str = 'roles'
    id = Column(Integer, primary_key=True)
    role = Column(VARCHAR(24), nullable=False)


class User(TGBase):
    __tablename__: str = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(VARCHAR(32), nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id', ondelete='CASCADE'))

    def __repr__(self):
        return f'id:{self.id}\nname:{self.username}'
