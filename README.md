# Pelops

## Docker Configuration

### Environment Variables

- `NGINX_LOG_ACCESS`
  - `true` = Nginx Logging Enabled (Default)
  - `false` = Nginx Logging Disabled
- `NGINX_LOG_ERROR`
  - `true` = Nginx Error Logging Enabled (Default)
  - `false` = Nginx Error Logging Disabled
- `UWSGI_LOG_ENABLED`
  - `true` = Uwsgi Logging Enabled (Default)
  - `false` = Uwsgi Logging Disabled
- `PELOPS_DEBUG`
  - `True` = Set Pelops Application to debug mode
  - `False` = Set Pelops Application to normal mode (Default)
- `LINKERD_AWAIT_DISABLED`
  - `1` = Set the Pelops container to not wait for the linkerd proxy to be ready
