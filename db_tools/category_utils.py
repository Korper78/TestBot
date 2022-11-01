from db_tools.db_utils import DbCRUD
from db_tools.models import Category


class CategoryTools:

    @staticmethod
    async def get_categories(supercategory_id: int = None) -> list | None:
        categories = await DbCRUD.get_all(db_object=Category)
        categories = [category[0] for category in categories if category[0].parent_id == supercategory_id]
        return categories

    # @staticmethod
    # async def get_products_by_prodarea(prodarea_id: int) -> list | None:
    #     products = await DbCRUD.get_all(db_object=Product)
    #     products = [product[0] for product in products if product[0].production_area_id == prodarea_id]
    #     return products

    @staticmethod
    async def get_category(category_id: int) -> Category | None:
        return await DbCRUD.get_one(db_object=Category,
                                    obj_id=category_id)

    @staticmethod
    async def add_category(name: str,
                           parent_id: int = None) -> bool:
        category = Category(name=name,
                            parent_id=parent_id)
        return await DbCRUD.add(db_object=category)

    @staticmethod
    async def del_product(category: Category):
        await DbCRUD.delete(db_object=category)

    @staticmethod
    async def update_category(category_id: int,
                              name: str = None,
                              parent_id: int = None):
        category = await CategoryTools.get_category(category_id)
        await DbCRUD.update(db_object=Category,
                            obj_id=category_id,
                            name=name if name else category.name,
                            parent_id=parent_id if parent_id else category.parent_id)
