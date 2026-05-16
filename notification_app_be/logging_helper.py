import importlib as _il

_auth_mod = _il.import_module("logging-middleware.auth")
_logger_mod = _il.import_module("logging-middleware.logger")

get_auth_token = _auth_mod.get_auth_token
log = _logger_mod.log
