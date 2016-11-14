from django.shortcuts import render

from app.models import User
from app.utils.decorator import admin_required
from app.utils.pagination import Pagination


@admin_required
def index_cont(request, page=1):
    pagination = Pagination()
    pagination.url = "dashboard.users.page"
    pagination.page = int(page)
    pagination.perPage = 20
    pagination.count = User.objects.count()
    users = User.objects.order_by('created_date')[pagination.ifrom:pagination.ito]
    return render(request, 'dashboard/users/index.html', {
        "users": users,
        "pagination": pagination
    })