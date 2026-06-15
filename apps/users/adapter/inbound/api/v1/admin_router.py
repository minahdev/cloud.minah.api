from fastapi import APIRouter, Depends

from users.app.ports.input.admin_use_case import AdminUseCase
from users.dependencies.admin_provider import get_admin_use_case

admin_router = APIRouter(prefix="/admin", tags=["admin"])
