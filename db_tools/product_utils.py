from db_tools.db_utils import DbCRUD
from db_tools.models import Product, RawMaterial


class ProductTools:

    @staticmethod
    async def get_products(storage_id: int | None, prodarea_id: int | None) -> list | None:
        products = await DbCRUD.get_all(db_object=Product)
        products = [product[0] for product in products if product[0].storage_id == storage_id and
                    product[0].production_area_id == prodarea_id and
                    not product[0].is_shipment]
        return products

    async def get_products_by_storage(storage_id: int) -> list | None:
        products = await DbCRUD.get_all(db_object=Product)
        products = [product[0] for product in products if product[0].storage_id == storage_id and
                    not product[0].is_shipment]
        return products

    @staticmethod
    async def get_products_by_prodarea(prodarea_id: int) -> list | None:
        products = await DbCRUD.get_all(db_object=Product)
        products = [product[0] for product in products if product[0].production_area_id == prodarea_id and
                    not product[0].is_shipment]
        return products

    @staticmethod
    async def get_products_by_category(category_id: int) -> list | None:
        products = await DbCRUD.get_all(db_object=Product)
        products = [product[0] for product in products if product[0].category_id == category_id]
        return products

    @staticmethod
    async def get_product_by_shipment(storage_id: int | None, prodarea_id: int | None, name: str) -> Product | None:
        products = await DbCRUD.get_all(db_object=Product)
        products = [product[0] for product in products if product[0].is_shipment and
                    product[0].storage_id == storage_id and
                    product[0].production_area_id == prodarea_id and
                    await ProductTools.get_product_name(product[0]) == name]
        return products[0] if products else None

    @staticmethod
    async def get_product(product_id: int) -> Product | None:
        return await DbCRUD.get_one(db_object=Product,
                                    obj_id=product_id)

    @staticmethod
    async def get_product_name(product: Product) -> str | None:
        raw_material = await DbCRUD.get_one(db_object=RawMaterial,
                                            obj_id=product.material_id)
        return raw_material.name

    @staticmethod
    async def get_product_names() -> list | None:
        raw_materials = await DbCRUD.get_all(db_object=RawMaterial)
        raw_materials = [raw_material[0] for raw_material in raw_materials]
        return raw_materials

    @staticmethod
    async def add_product_name(name: str) -> bool:
        raw_material = RawMaterial(name=name)
        return await DbCRUD.add(db_object=raw_material)

    @staticmethod
    async def add_product(amount: int,
                          material_id: int,
                          category_id: int,
                          storage_id: int,
                          production_area_id: int,
                          is_shipment: bool = False) -> bool:
        product = Product(amount=amount,
                          material_id=material_id,
                          category_id=category_id,
                          storage_id=storage_id,
                          production_area_id=production_area_id,
                          is_shipment=is_shipment)
        return await DbCRUD.add(db_object=product)

    @staticmethod
    async def del_product(product: Product):
        await DbCRUD.delete(db_object=product)

    @staticmethod
    async def update_product(product_id: int,
                             amount: int = None,
                             material_id: int = None,
                             category_id: int = None,
                             storage_id: int = None,
                             production_area_id: int = None,
                             is_shipment: bool = False):
        product = await ProductTools.get_product(product_id)
        await DbCRUD.update(db_object=Product,
                            obj_id=product_id,
                            amount=amount if amount else product.amount,
                            material_id=material_id if material_id else product.material_id,
                            category_id=category_id if category_id else product.category_id,
                            storage_id=storage_id if storage_id else product.storage_id,
                            production_area_id=production_area_id if production_area_id else product.production_area_id,
                            is_shipment=is_shipment)
