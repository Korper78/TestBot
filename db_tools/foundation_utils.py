from db_tools.db_utils import DbCRUD
from db_tools.models import Foundation


class FoundTools:

    @staticmethod
    async def get_foundations() -> list | None:
        foundations = await DbCRUD.get_all(db_object=Foundation)
        # return await DbCRUD.get_all(db_object=Foundation)
        return [foundation[0] for foundation in foundations]

    @staticmethod
    async def get_foundation(foundation_id: int) -> Foundation | None:
        return await DbCRUD.get_one(db_object=Foundation, obj_id=foundation_id)

    @staticmethod
    async def add_foundation(name: str,
                             address: str) -> bool:
        foundation = Foundation(name=name, address=address)
        print(foundation)
        return await DbCRUD.add(db_object=foundation)

    @staticmethod
    async def del_foundation(foundation: Foundation):
        await DbCRUD.delete(db_object=foundation)

    @staticmethod
    async def update_foundation(foundation_id: int,
                                name: str = None,
                                address: str = None):
        foundation = await FoundTools.get_foundation(foundation_id)
        await DbCRUD.update(db_object=Foundation,
                            obj_id=foundation_id,
                            name=name if name else foundation.name,
                            address=address if address else foundation.address)
