import ldap
from ais.secrets import KTH_CATALOG_PW

def lookup_user(kth_id):
    con = ldap.initialize('ldaps://ldap.sys.kth.se:636')
    dn='uid=armada,ou=people,dc=kth,dc=se'
    base='ou=Addressbook,dc=kth,dc=se'
    con.simple_bind(dn, KTH_CATALOG_PW)
    user=con.search_s(base, ldap.SCOPE_ONELEVEL, 'ugKthid='+kth_id)
    con.unbind()
    return dict(
                email=user[0][1]['mail'][0],
                first_name=user[0][1]['givenName'][0],
                last_name=user[0][1]['sn'][0]
                )
