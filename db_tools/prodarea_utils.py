from db_tools.db_utils import DbCRUD
from db_tools.models import ProductionArea


class ProdAreaTools:

    @staticmethod
    async def get_prodareas(foundation_id: int) -> list | None:
        prodareas = await DbCRUD.get_all(db_object=ProductionArea)
        prodareas = [prodarea[0] for prodarea in prodareas if prodarea[0].foundation_id == foundation_id]
        return prodareas

    @staticmethod
    async def get_prodarea(prodarea_id: int) -> ProductionArea | None:
        return await DbCRUD.get_one(db_object=ProductionArea,
                                    obj_id=prodarea_id)

    @staticmethod
    async def add_prodarea(name: str,
                           foundation_id: int) -> bool:
        prodarea = ProductionArea(name=name, foundation_id=foundation_id)
        return await DbCRUD.add(db_object=prodarea)

    @staticmethod
    async def del_prodarea(prodarea: ProductionArea):
        await DbCRUD.delete(db_object=prodarea)

    @staticmethod
    async def update_prodarea(prodarea_id: int,
                              name: str = None,
                              foundation_id: int = None):
        prodarea = await ProdAreaTools.get_prodarea(prodarea_id)
        await DbCRUD.update(db_object=ProductionArea,
                            obj_id=prodarea_id,
                            name=name if name else prodarea.name,
                            foundation_id=foundation_id if foundation_id else prodarea.foundation_id)
