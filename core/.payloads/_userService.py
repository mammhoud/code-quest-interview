from base.common.base.services.core import model_update  # type: ignore
from django.contrib.auth.models import Group
from django.db import transaction

# from base.contrib.profiles.models.profile import Profile
from django.utils.translation import gettext_lazy as _  # noqa: F401

import logging

# from core import loggerRequest as logger  # type: ignore

# from ninja_jwt.token_blacklist import OutstandingToken
logger = logging.getLogger(__name__)

# from tenant_users.tenants.tasks import provision_tenant
from ..models.user import User as Account

# from base.contrib.contact.models.email import Email


# def create_tenantWithOwner(*, name, tenant_slug, user):
#     """
#     args: user
#     tenant_schema_name: name
#     current_site: site for to be added on domain_site

#     """
#     tenant, domain = provision_tenant(
#         tenant_name=name, tenant_slug=tenant_slug, user_email=user.email
#     )
#     return {"tenans": tenant, "domain": domain}


def create_userInfo(*, created_user):
    user_group, created = Group.objects.get_or_create(name="client")
    if created:
        logger.debug("created new group")  # TODO: log this as user message
    created_user.groups.add(user_group)

    # todo add a new function to create a email address if not exist, profile and contact information with user prompot data
    # todo check if the user is already created all profile data and approved to authintecately use the website selected features
    # user_profile, created = Profile.objects.get_or_create(user=created_user)

    # Generate a token and send a verification email here
    # Set the token in the user's profile
    # token = Token.objects.get_or_create(token_type="EA", user=created_user)
    # token.users.add(user_profile)
    # token.save()

    # user_profile.email = ss.email

    # user_profile.email_token = token
    # user_profile.save()


@transaction.atomic
def user_create(
    *,
    email: str,
    is_active: bool = True,
    is_admin: bool = False,
    password: str | None = None,
) -> Account:
    user = Account.objects.create_user(
        email=email, is_active=is_active, is_admin=is_admin, password=password
    )  # type: ignore

    return user

from core.base.models0 import Profile
@transaction.atomic
def create_profile(*, user: Account, email) -> Account:
    profile, created = Profile.objects.get_or_create(
        user=user,
        # todo: add more data defiend as bussines needed
    )
    if not created:
        logger.danger(
            "created new profile with the same profile"
        )  # TODO: log this as user message

    if user.is_superuser:
        profile.role = "Admin"
        profile.save()
    from allauth.account.models import EmailAddress as EmailAddress
    from common.contact.models.contact import Contact  # noqa: F401
    from common.contact.models.contact import ContactEmail as email

    # email_address = EmailAddress.objects.get_primary(user)
    # if not email_address:  # noqa: E722
    if EmailAddress.objects.filter(email=user.email, primary=True).exists():
        raise Exception("Email address already exists")
    else:
        email_address, _ = EmailAddress.objects.get_or_create(
            user=user, email=user.email, primary=True, verified=False
        )

    contact, created = Contact.objects.get_or_create(profile=profile)
    if created:
        email_address = email.objects.get_or_create(
            email=email_address, contact=contact, is_user_email=True
        )
    # profile.contact = contact
    return user


@transaction.atomic
def user_update(*, user: Account, data) -> Account:
    non_side_effect_fields = ["first_name", "last_name"]

    user, has_updated = model_update(
        instance=user, fields=non_side_effect_fields, data=data
    )

    # Side-effect fields update here (e.g. username is generated based on first & last name)

    # ... some additional tasks with the user ...

    return user


@transaction.atomic
def create_user(
    *, email, username=None, is_active=True, is_admin=False, password=None
):
    if not email:
        raise ValueError("Users must have an email address")
    if not Account.objects.filter(email=email, is_active=True).exists():
        user = Account(
            email=email,
            username=username,
            is_active=is_active,
            is_admin=is_admin,
            is_staff=is_admin or is_active,  # Setting staff as active/admin
        )
        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.full_clean()  # Validate the model before saving
        email = Account.normalize_email(email.lower())  # type: ignore
        user.save()
        create_profile(user=user, email=email)
    else:
        raise ValueError("A user with that email already exists")

    return user
