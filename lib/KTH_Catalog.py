import ldap3
from ais.secrets import KTH_CATALOG_PW

def lookup_user(kth_id):
    server = ldap3.Server('ldap.sys.kth.se', port = 636, use_ssl = True)
    dn='uid=armada,ou=people,dc=kth,dc=se'
    base='ou=Addressbook,dc=kth,dc=se'
    con = ldap3.Connection(server, user=dn, password=KTH_CATALOG_PW)
    con.bind()
    con.search(search_base = base,
                             search_filter = '(ugKthid='+kth_id+')',
                             search_scope = ldap3.LEVEL,
                             attributes=['mail', 'givenName', 'sn'],
                             )
    user = con.entries[0]
    con.unbind()

    return dict(
                email=user.mail.value,
                first_name=user.givenName.value,
                last_name=user.sn.value
                )
