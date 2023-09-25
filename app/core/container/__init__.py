from pathlib import Path

from dependency_injector import containers, providers

from app.controller.repository.health_check import HealthCheckRepository
from app.controller.repository.user import UserRepository
from app.controller.service.auth import AuthService
from app.controller.service.health_check import HealthCheckService
from app.controller.service.user import UserService
from app.core.database import Database
from app.core.settings import Settings


class Container(containers.DeclarativeContainer):
    path = Path().absolute().joinpath("app/api/route")
    modules = ["app.api.route." + x.stem for x in path.iterdir()]
    wiring_config = containers.WiringConfiguration(modules=modules)

    settings = Settings()

    # Add Singletons (Database, Authentication, etc)
    # Example
    db = providers.Singleton(Database, settings.db)

    # Add provider.Factory for Repositories|Services
    # Example
    health_check_repository = providers.Factory(
        HealthCheckRepository, session_factory=db.provided.session
    )
    health_check_service = providers.Factory(
        HealthCheckService, health_check_repository=health_check_repository
    )
    user_repository = providers.Factory(
        UserRepository, session_factory=db.provided.session
    )
    user_service = providers.Factory(
        UserService, user_repository=user_repository
    )
    auth_service = providers.Factory(
        AuthService, user_service=user_service
    )
