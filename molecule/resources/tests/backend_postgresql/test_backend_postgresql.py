debian_os = ['debian', 'ubuntu']
rhel_os = ['redhat', 'centos', 'ol', 'rocky', 'almalinux']
archlinux_os = ['arch']


def test_package(host):
    if host.system_info.distribution.lower() in debian_os + rhel_os:
        p = host.package('pdns-backend-pgsql')
        assert p.is_installed


def test_config(host):
    with host.sudo():
        f = None
        if host.system_info.distribution.lower() in debian_os + archlinux_os:
            f = host.file('/etc/powerdns/pdns.conf')
        if host.system_info.distribution.lower() in rhel_os:
            f = host.file('/etc/pdns/pdns.conf')

        dbname = host.check_output('hostname -s').replace('.', '_')
        user= 'powerdns-' + dbname

        assert f.exists
        assert f.contains('launch+=gpgsql')
        assert f.contains('gpgsql-host=postgresql')
        assert f.contains('gpgsql-password=powerdns')
        assert f.contains('gpgsql-dbname=' + dbname)
        assert f.contains('gpgsql-user=' + user)


def test_database_tables(host):
    dbname = host.check_output('hostname -s').replace('.', '_')

    cmd = host.run(
        f'psql --username="pdns" --host="postgresql" --dbname="{dbname}" --no-password --tuples-only --no-align --command="SELECT DISTINCT table_name FROM information_schema.tables WHERE table_schema = \'public\' AND table_type = \'BASE TABLE\';"'
    )

    for table in [ 'domains', 'records', 'supermasters', 'comments',
            'domainmetadata', 'cryptokeys', 'tsigkeys' ]:
        assert table in cmd.stdout
