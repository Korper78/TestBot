from db_tools.db_utils import DbCRUD
from db_tools.models import User


class UserTools:

    @staticmethod
    async def get_user(user_id: int) -> User | None:
        return await DbCRUD.get_one(db_object=User, obj_id=user_id)

    @staticmethod
    async def add_user(user_id: int,
                       username: str,
                       role: int = 2) -> bool:
        user = User(id=user_id, username=username, role_id=role)
        return await DbCRUD.add(db_object=user)

    @staticmethod
    async def del_user(user: User):
        await DbCRUD.delete(db_object=user)

    @staticmethod
    async def update_user(user_id: int,
                          username: str = None,
                          role_id: int = None):
        user = await UserTools.get_user(user_id)
        await DbCRUD.update(db_object=User,
                            obj_id=user_id,
                            username=username if username else user.username,
                            role_id=role_id if role_id else user.role_id)
