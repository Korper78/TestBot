from db_tools.db_utils import DbCRUD
from db_tools.models import Storage


class StorageTools:

    @staticmethod
    async def get_storages(foundation_id: int) -> list | None:
        storages = await DbCRUD.get_all(db_object=Storage)
        storages = [storage[0] for storage in storages if storage[0].foundation_id == foundation_id]
        return storages

    @staticmethod
    async def get_storage(storage_id: int) -> Storage | None:
        return await DbCRUD.get_one(db_object=Storage,
                                    obj_id=storage_id)

    @staticmethod
    async def add_storage(name: str,
                          address: str,
                          foundation_id: int) -> bool:
        storage = Storage(name=name,
                          address=address,
                          foundation_id=foundation_id)
        return await DbCRUD.add(db_object=storage)

    @staticmethod
    async def del_storage(storage: Storage):
        await DbCRUD.delete(db_object=storage)

    @staticmethod
    async def update_storage(storage_id: int,
                             name: str = None,
                             address: str = None,
                             foundation_id: int = None):
        storage = await StorageTools.get_storage(storage_id)
        await DbCRUD.update(db_object=Storage,
                            obj_id=storage_id,
                            name=name if name else storage.name,
                            address=address if address else storage.address,
                            foundation_id=foundation_id if foundation_id else storage.foundation_id)
