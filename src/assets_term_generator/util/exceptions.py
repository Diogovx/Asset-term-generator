class ApplicationError(Exception):
    pass


class UserNotFoundError(ApplicationError):
    pass


class AssetNotFoundError(ApplicationError):
    pass


class InvalidInputError(ValueError):
    pass


class NoCompatibleAssetsError(ApplicationError):
    pass


class TemplateConfigError(ApplicationError):
    pass
