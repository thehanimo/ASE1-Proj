from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse


def agent_required(function=None, redirect_field_name=None, login_url='forbidden'):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.user_type == 2,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def customer_required(function=None, redirect_field_name=None, login_url='forbidden'):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.user_type == 1,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def executive_required(function=None, redirect_field_name=None, login_url='forbidden'):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.user_type== 3 and hasattr(u, 'executive'),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def agent_or_executive_required(function=None, redirect_field_name=None, login_url='forbidden'):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and (u.user_type == 2 or (u.user_type == 3 and hasattr(u, 'executive'))),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def customer_or_executive_required(function=None, redirect_field_name=None, login_url='forbidden'):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and (u.user_type == 1 or (u.user_type == 3 and hasattr(u, 'executive'))),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def customer_details_required(function=None, redirect_field_name=None, login_url='customer:newprofile'):
    actual_decorator = user_passes_test(
        lambda u: hasattr(u, 'customer'),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def customer_details_empty(function=None, redirect_field_name=None, login_url='customer:editprofile'):
    actual_decorator = user_passes_test(
        lambda u: hasattr(u, 'customer') == False,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator