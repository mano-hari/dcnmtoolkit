from applications.VXLAN_EVPN_Fabric.credentials import URL, CERT, LOGIN, PASSWORD
from applications.VXLAN_EVPN_Fabric.fabric_data import FABRIC_EXTENSION, FABRIC_OVERLAY_EXT
from dcnmtoolkit import Session
import logging
import applications.VXLAN_EVPN_Fabric.json
import time

logging.getLogger(__name__)


def main(url=None, cert=None):
    """My Main"""
    session = Session(url, LOGIN, PASSWORD, logging_lvl='INFO', verify=cert)
    session.login()

    add_fab_ext(session)
    # del_fab_ext(session)


def add_fab_ext(session):
    for underlay in FABRIC_EXTENSION:
        url = '/rest/top-down/fabrics/%s/vrf-extension' % underlay['sourceFabric']
        resp = session.post(url, applications.VXLAN_EVPN_Fabric.json.dumps(underlay))
        time.sleep(10)
        logging.info('HTTP POST response %s' % resp)

    for overlay in FABRIC_OVERLAY_EXT:
        url = '/rest/top-down/fabrics/%s/vrf-extension' % overlay['sourceFabric']
        resp = session.post(url, applications.VXLAN_EVPN_Fabric.json.dumps(overlay))
        time.sleep(10)
        logging.info('HTTP POST response %s' % resp)


def del_fab_ext(session):
    fabric_ext = dict()
    fabric_ext_keys = dict.fromkeys(['sourceFabric', 'sourceSwitch', 'sourcePort', 'destFabric', 'destSwitch',
                                     'destPort', 'extensionType'])
    for underlay in FABRIC_EXTENSION:
        for key, value in underlay.iteritems():
            if key in fabric_ext_keys:
                fabric_ext[key] = value
        url = '/rest/top-down/fabrics/%s/vrf-extension' % fabric_ext['sourceFabric']
        resp = session.delete(url, applications.VXLAN_EVPN_Fabric.json.dumps(fabric_ext))
        logging.info('HTTP POST response %s' % resp)
        print resp.content

    for overlay in FABRIC_OVERLAY_EXT:
        for key, value in overlay.iteritems():
            if key in fabric_ext_keys:
                fabric_ext[key] = value
        url = '/rest/top-down/fabrics/%s/vrf-extension' % fabric_ext['sourceFabric']
        resp = session.delete(url, applications.VXLAN_EVPN_Fabric.json.dumps(fabric_ext))
        logging.info('HTTP POST response %s' % resp)


if __name__ == "__main__":
    main(url=URL['url2'], cert=CERT['cert2'])
