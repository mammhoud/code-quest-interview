from django.db.models.query import QuerySet

from ..models.user import User as Account
from core.base.payload.user import AccountFilter
# from base.contrib.contact.models.core import Contact
# from base.contrib.contact.models.email import Email


def user_get_login_data(*, user: Account):
    return {
        "id": user.id,  # type: ignore
        "email": user.email,
        "is_active": user.is_active,
        "is_admin": user.is_admin,
        "is_superuser": user.is_superuser,
    }


def user_get_online_users(*, user: Account):
    """
    Returns a list of online users.
    TODO: Create a mant to many model for get the users online at the same time userloged in then return a trigger to channel usersOnline
    based on the user contact model"""

    return None


def user_list(*, filters=None) -> QuerySet[Account]:
    """
    Returns a queryset of users based on the provided filters.

    Args:
        filters: A dictionary of filter conditions.
    """
    filters = filters or {}

    qs = Account.objects.all()

    return AccountFilter(filters, qs).qs
