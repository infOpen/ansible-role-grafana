"""
Role tests
"""

import pytest
from testinfra.utils.ansible_runner import AnsibleRunner

testinfra_hosts = AnsibleRunner('.molecule/ansible_inventory').get_hosts('all')


def test_repository_files(host):
    """
    Test repository files
    """

    if host.system_info.distribution in ['debian', 'ubuntu']:
        pytest.skip('Not apply to this distribution')

    repo_file = host.file(
        '/etc/apt/sources.list.d/packagecloud_io_grafana_stable_debian.list')

    assert repo_file.exists
    assert repo_file.is_file
    assert repo_file.user == 'root'
    assert repo_file.group == 'root'
    assert repo_file.mode == 0o644


def test_packages(host):
    """
    Test installed packages
    """

    assert host.package('grafana').is_installed


@pytest.mark.parametrize('path,user,group,mode', [
    ('/etc/grafana/grafana.ini', 'root', 'root', 0o664),
    ('/etc/grafana/ldap.toml', 'root', 'grafana', 0o640),
    ('/etc/default/grafana-server', 'root', 'root', 0o664),
])
def test_configuration_files(host, path, user, group, mode):
    """
    Tests if all configuration files
    """

    current_file = host.file(path)

    assert current_file.exists
    assert current_file.is_file
    assert current_file.user == user
    assert current_file.group == group
    assert current_file.mode == mode


def test_service(host):
    """
    Test Grafana service
    """

    # Waiting a jessie image with systemd management
    if host.system_info.codename == 'jessie':
        assert 'running' in host.check_output(
            '/etc/init.d/grafana-server status')
    else:
        assert host.service('grafana-server').is_running
        assert host.service('grafana-server').is_enabled


def test_socket(host):
    """
    Test Grafana socket
    """

    assert host.socket('tcp://:::3000').is_listening
