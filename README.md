# grafana

[![Build Status](https://travis-ci.org/infOpen/ansible-role-grafana.svg?branch=master)](https://travis-ci.org/infOpen/ansible-role-grafana)

Install grafana package.

## Requirements

This role requires Ansible 2.0 or higher,
and platform requirements are listed in the metadata file.

## Testing

This role use [Molecule](https://github.com/metacloud/molecule/) to run tests.

Locally, you can run tests on Docker (default driver) or Vagrant.
Travis run tests using Docker driver only.

Currently, tests are done on:
- Debian Jessie
- Ubuntu Trusty
- Ubuntu Xenial

and use:
- Ansible 2.0.x
- Ansible 2.1.x
- Ansible 2.2.x
- Ansible 2.3.x

### Running tests

#### Using Docker driver

```
$ tox
```

#### Using Vagrant driver

```
$ MOLECULE_DRIVER=vagrant tox
```

## Role Variables

### Default role variables

``` yaml
# General
#------------------------------------------------------------------------------

# Packages and repositories management
grafana_packages: "{{ _grafana_packages }}"
grafana_repository_cache_valid_time: 3600
grafana_repositories_keys: "{{ _grafana_repositories_keys }}"
grafana_repositories: "{{ _grafana_repositories }}"
grafana_system_dependencies: "{{ _grafana_system_dependencies | default([]) }}"

# Service management
grafana_service:
  name: 'grafana-server'
  state: 'enabled'
  enabled: True

# User and group management
grafana_user:
  name: 'grafana'
  group: 'grafana'
  home: '/usr/share/grafana'
grafana_group:
  name: 'grafana'

# Path_management
_grafana_paths:
  dirs:
    data:
      path: '/var/lib/grafana'
      user: "{{ grafana_user.name }}"
      group: "{{ grafana_group.name }}"
      mode: '0700'
    conf:
      path: '/etc/grafana'
      user: "{{ grafana_user.name }}"
      group: "{{ grafana_group.name }}"
      mode: '0700'
    log:
      path: '/var/log/grafana'
      user: "{{ grafana_user.name }}"
      group: "{{ grafana_group.name }}"
      mode: '0700'
    plugins:
      path: '/var/lib/grafana/plugins'
      user: "{{ grafana_user.name }}"
      group: "{{ grafana_group.name }}"
      mode: '0700'
    user_home:
      path: '/usr/share/grafana'
      user: "{{ grafana_user.name }}"
      group: "{{ grafana_group.name }}"
      mode: '0700'
  files:
    conf:
      path: '/etc/grafana/grafana.ini'
      user: 'root'
      group: 'root'
      mode: '0664'
    default:
      path: '/etc/default/grafana-server'
      user: 'root'
      group: 'root'
      mode: '0664'
    ldap:
      path: '/etc/grafana/ldap.toml'
      user: 'root'
      group: 'grafana'
      mode: '0640'
grafana_paths: "{{ _grafana_paths }}"

# Configuration
#------------------------------------------------------------------------------
grafana_max_open_files: 10000
grafana_restart_on_upgrade: True

grafana_app_mode: 'production'
grafana_instance_name: '${HOSTNAME}'

_grafana_environment:
  GRAFANA_USER: "{{ grafana_user.name }}"
  GRAFANA_GROUP: "{{ grafana_group.name }}"
  GRAFANA_HOME: "{{ grafana_paths.dirs.user_home.path }}"
  LOG_DIR: "{{ grafana_paths.dirs.log.path }}"
  DATA_DIR: "{{ grafana_paths.dirs.data.path }}"
  MAX_OPEN_FILES: "{{ grafana_max_open_files }}"
  CONF_DIR: "{{ grafana_paths.dirs.conf.path }}"
  CONF_FILE: "{{ grafana_paths.files.conf.path }}"
  RESTART_ON_UPGRADE: "{{ grafana_restart_on_upgrade }}"
  PLUGINS_DIR: "{{ grafana_paths.dirs.plugins.path }}"
grafana_environment: "{{ _grafana_environment }}"

_grafana_config:
  paths:
    data: "{{ grafana_paths.dirs.data.path }}"
    logs: "{{ grafana_paths.dirs.log.path }}"
    plugins: "{{ grafana_paths.dirs.plugins.path }}"
  server:
    protocol: 'http'
    http_addr: ''
    http_port: 3000
    domain: 'localhost'
    enforce_domain: False
    root_url: 'http://localhost:3000'
    router_logging: False
    static_root_path: 'public'
    enable_gzip: False
    cert_file: ''
    cert_key: ''
    socket: ''
  database:
    type: 'sqlite3'
    host: '127.0.0.1:3306'
    name: 'grafana'
    user: 'root'
    password: ''
    url: ''
    ssl_mode: 'disable'
    path: 'grafana.db'
    max_idle_conn: ''
    max_open_conn: ''
  session:
    provider: 'file'
    provider_config: 'sessions'
    cookie_name: 'grafana_sess'
    cookie_secure: False
    session_life_time: 86400
  data_proxy:
    logging: False
  analytics:
    reporting_enabled: True
    check_for_updates: True
    google_analytics_ua_id: ''
  security:
    admin_user: 'admin'
    admin_password: 'admin'
    secret_key: 'SW2YcwTIb9zpOOhoPsMm'
    login_remember_days: 7
    cookie_username: 'grafana_user'
    cookie_remember_name: 'grafana_remember'
    disable_gravatar: False
    data_source_proxy_whitelist: ''
  snapshots:
    external_enabled: True
    external_snapshot_url: 'https://snapshots-origin.raintank.io'
    external_snapshot_name: 'Publish to snapshot.raintank.io'
    snapshot_remove_expired: True
    snapshot_TTL_days: 90
  users:
    allow_sign_up: True
    allow_org_create: True
    auto_assign_org: True
    auto_assign_org_role: 'Viewer'
    login_hint: 'email or username'
    default_theme: 'dark'
  auth:
    disable_login_form: False
    disable_signout_menu: False
  auth.anonymous:
    enabled: False
    org_name: 'Main Org.'
    org_role: 'Viewer'
  auth.github:
    enabled: False
    allow_sign_up: True
    client_id: 'some_id'
    client_secret: 'some_secret'
    scopes: 'user:email,read:org'
    auth_url: 'https://github.com/login/oauth/authorize'
    token_url: 'https://github.com/login/oauth/access_token'
    api_url: 'https://api.github.com/user'
    team_ids: ''
    allowed_organizations: ''
  auth.google:
    enabled: False
    allow_sign_up: True
    client_id: 'some_client_id'
    client_secret: 'some_client_secret'
    scopes: 'https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email'
    auth_url: 'https://accounts.google.com/o/oauth2/auth'
    token_url: 'https://accounts.google.com/o/oauth2/token'
    api_url: 'https://www.googleapis.com/oauth2/v1/userinfo'
    allowed_domains: ''
  auth.generic_oauth:
    enabled: False
    name: 'OAuth'
    allow_sign_up: True
    client_id: 'some_id'
    client_secret: 'some_secret'
    scopes: 'user:email,read:org'
    auth_url: 'https://foo.bar/login/oauth/authorize'
    token_url: 'https://foo.bar/login/oauth/access_token'
    api_url: 'https://foo.bar/user'
    team_ids: ''
    allowed_organizations: ''
  auth.grafana_com:
    enabled: False
    allow_sign_up: True
    client_id: 'some_id'
    client_secret: 'some_secret'
    scopes: 'user:email'
    allowed_organizations: ''
  auth.proxy:
    enabled: False
    header_name: 'X-WEBAUTH-USER'
    header_property: 'username'
    auto_sign_up: True
    ldap_sync_ttl: 60
    whitelist: '192.168.1.1, 192.168.2.1'
  auth.basic:
    enabled: True
  auth.ldap:
    enabled: False
    config_file: '/etc/grafana/ldap.toml'
    allow_sign_up: True
  smtp:
    enabled: False
    host: localhost:25
    user: ''
    password: ''
    cert_file: ''
    key_file: ''
    skip_verify: False
    from_address: 'admin@grafana.localhost'
    from_name: 'Grafana'
  emails:
    welcome_email_on_sign_up: False
  log:
    mode: 'console file'
    level: 'info'
    filters: ''
  log.console:
    level: ''
    format: 'console'
  log.file:
    level: ''
    format: 'text'
    log_rotate: True
    max_lines: 1000000
    max_size_shift: 28
    daily_rotate: True
    max_days: 7
  log.syslog:
    level: ''
    format: 'text'
    network: ''
    address: ''
    facility: ''
    tag: ''
  event_publisher:
    enabled: False
    rabbitmq_url: 'amqp://localhost/'
    exchange: 'grafana_events'
  dashboards.json:
    enabled: False
    path: '/var/lib/grafana/dashboards'
  alerting:
    enabled: True
    execute_alerts: True
  metrics:
    enabled: True
    interval_seconds: 10
  metrics.graphite:
    address: ''
    prefix: 'prod.grafana.%(instance_name)s.'
  grafana_com:
    url: 'https://grafana.com'
  external_image_storage:
    provider: ''
  external_image_storage.s3:
    bucket_url: ''
    access_key: ''
    secret_key: ''
  external_image_storage.webdav:
    url: ''
    public_url: ''
    username: ''
    password: ''
grafana_config: "{{ _grafana_config }}"

_grafana_ldap_config:
  servers:
    host: '127.0.0.1'
    port: 389
    use_ssl: False
    start_tls: False
    ssl_skip_verify: False
    root_ca_cert: ''
    bind_dn: 'cn=admin,dc=grafana,dc=org'
    bind_password: 'grafana'
    search_filter: '(cn=%s)'
    search_base_dns:
      - 'dc=grafana,dc=org'
    group_search_filter: '(&(objectClass=posixGroup)(memberUid=%s))'
    group_search_filter_user_attribute: 'distinguishedName'
    group_search_base_dns:
      - 'ou=groups,dc=grafana,dc=org'
  attributes:
    name: 'givenName'
    surname: 'sn'
    username: 'cn'
    member_of: 'memberOf'
    email:  'email'
  group_mappings:
    - group_dn: 'cn=admins,dc=grafana,dc=org'
      org_role: 'Admin'
      org_id: 1
    - group_dn: 'cn=users,dc=grafana,dc=org'
      org_role: 'Editor'
      org_id: 1
    - group_dn: '*'
      org_role: 'Viewer'
      org_id: 1
grafana_ldap_config: "{{ _grafana_ldap_config }}"
```

## How manage ...

### Datasources

This role manage Grafana datasources using API.
Authentication is done by basic auth or API token.

Just configure `grafana_datasources` variable.

Example:
``` yaml
grafana_datasources:
  - id: 1
    orgId: 1
    name: 'test_datasource'
    type: 'graphite'
    access: 'proxy'
    url: 'http://mydatasource.com'
    password: ''
    user: ''
    database: ''
    basicAuth: False
    basicAuthUser: ''
    basicAuthPassword: ''
    isDefault: False
    jsonData: None
```

## Dependencies

None

## Example Playbook

``` yaml
- hosts: servers
  roles:
    - { role: infOpen.grafana }
```

## License

MIT

## Author Information

Alexandre Chaussier (for Infopen company)
- http://www.infopen.pro
- a.chaussier [at] infopen.pro
