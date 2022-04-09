#!/usr/bin/env python3

# simpleSAMLphp Attribute Release Policy - SSP-ARP.

# Press Maiusc+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Lo script python SSP-ARP dovrà:
# 1) elaborare sia file di metadata composti (<EntitiesDescriptor>) che singoli (<EntityDescriptor>)
# 2) elaborare solo i <SPSSODescriptor> di cui dovrà raccogliere:
#    1) Dell'elemento XML <mdrpi:RegistrationInfo>, l'attributo XML "registrationAuthority"
#    2) Dell'elemento XML <mdattr:EntityAttributes>, gli attributi XML "Name" e "NameFormat" dell'elemento <saml:Attribute>
#       e l'elemento XML <saml:AttributeValue> all'interno di <saml:Attribute>
#    3) L'elemento XML <md:NameIDFormat> per stabilire se rilasciare o meno l'eduPersonTargetedID in mancanza del "persistent" NameIDFormat
#    4) Di ogni elemento XML "<md:AttributeConsumingService>", il valore di "<md:ServiceName>" per la lingua inglese - Utile per un commento pre-filtro
#    4) Dell'elemento XML <md:RequestedAttribute>, gli attributi "Name" e "isRequired" per stabilire cosa rilasciare
#    5) Dell'elemento XML <md:ContactPerson>, gli attributi "contactType" e "remd:contactType" per stabilire se è attivo il SIRTFI
#       e, eventualmente, i valori degli elementi XML interni "<md:GivenName>" e "<md:EmailAddress>" per contattare chi di dovere.
#
# Potrebbe essere interessante inserire i contatti presenti nei metadata in una riga di commento sulla risorsa (forse)

import argparse
import sys
import xml.etree.ElementTree as ET

from jinja2 import Environment, FileSystemLoader, select_autoescape

import attribute_map
import ec_arp
import utils

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    if not attribute_map.oid2name:
        sys.exit("!!! Attribute Map dictionary into 'attribute_map.py' is not exist or is empty !!!")
    elif not ec_arp.entity_categories:
        sys.exit("!!! Entity Categories into 'ec_arp.py' is not exist or is empty !!!")
    else:
        parser = argparse.ArgumentParser(
            description='Generate the "saml20-sp-remote-override.php" implementing the ARP for SSP SPs')
        parser.add_argument("-in", "--input", required=True, metavar="/path/input/fed-md.xml", nargs=1,
                            help="Full Path of Fed XML metadata used as input")
        parser.add_argument("--idp", required=True, metavar="entityID-IdP", nargs=1,
                            help="entityID of the IdP who wants the SSP-ARP")
        parser.add_argument("-out", "--output", metavar="/path/output/ssp-arp.php", nargs=1,
                            help="Full Path of saml20-sp-remote-override.php")
        parser.add_argument("--sp", metavar="entityID-SP", help="Elaborate the ARP for a specific SP")
        parser.add_argument("-d", "--debug", action='store_true', help="Print debug things")
        args = parser.parse_args()

        if args.debug:
            print(f"Arguments:")
            print(f"input Federation metadata: {args.input}")
            print(f"input IDP entityID: {args.idp}")
            print(f"output SSP ARP: {args.output or 'SSP ARP will be printed'}")
            print(f"output SSP ARP: {args.sp or 'SP not provided, the script will consider all SPs on metadata'}")

        inputfile = args.input[0]
        entityid_idp = args.idp[0]
        output_php_arp = args.output[0] if args.output else None
        sp = args.sp[0] if args.sp else None

        # ARP SP List
        sp_arp_list = list()

        env = Environment(
            loader=FileSystemLoader("templates"),
            autoescape=select_autoescape(),
            auto_reload=False
        )
        template = env.get_template("saml20-sp-remote-override-template.php")

        tree = ET.parse(inputfile)
        root = tree.getroot()

        idps = root.findall("./md:EntityDescriptor[md:IDPSSODescriptor]", utils.namespaces)
        sps = root.findall("./md:EntityDescriptor[md:SPSSODescriptor]", utils.namespaces)

        # IDPSSODescriptor
        for EntityDescriptor in idps:

            # Get entityID IdP
            idp_entityID = utils.get_entityID(EntityDescriptor)

            if idp_entityID != entityid_idp: continue

            if args.debug: print(f"IDP: {idp_entityID}")

            # Get RegistrationAuthority
            idp_regAuth = utils.get_RegistrationAuthority(EntityDescriptor)

            # Get RS EC
            idp_rs = utils.has_EntityAttributes(EntityDescriptor, 'http://macedir.org/entity-category-support',
                                                'http://refeds.org/category/research-and-scholarship')

            # Get COCO EC
            idp_coco = utils.has_EntityAttributes(EntityDescriptor, 'http://macedir.org/entity-category-support',
                                                  'http://www.geant.net/uri/dataprotection-code-of-conduct/v1')

            # Get SIRTFI
            idp_sirtfi = utils.has_EntityAttributes(EntityDescriptor,
                                                    'urn:oasis:names:tc:SAML:attribute:assurance-certification',
                                                    'https://refeds.org/sirtfi')

            # Discover is 'persistent' NameID is the preferred one
            idp_persistent_nameid = utils.idp_supports_persistent_nameid(EntityDescriptor)

            if args.debug: print(
                f"{idp_entityID} supports: RS=>{idp_rs}, COCO=>{idp_coco}, SIRTFI=>{idp_sirtfi}, persistent NameID=>{idp_persistent_nameid}")

            # SPSSODescriptor
            for EntityDescriptor in sps:

                # Get SP entityID
                sp_entityID = utils.get_entityID(EntityDescriptor)

                # Get RegistrationAuthority
                sp_regAuth = utils.get_RegistrationAuthority(EntityDescriptor)

                # Get RS EC
                sp_rs = utils.has_EntityAttributes(EntityDescriptor, 'http://macedir.org/entity-category',
                                                   'http://refeds.org/category/research-and-scholarship')

                # Get COCO EC
                # sp_coco = utils.has_EntityAttributes(EntityDescriptor, 'http://macedir.org/entity-category',
                #                                'http://www.geant.net/uri/dataprotection-code-of-conduct/v1')

                # Get SIRTFI
                sp_sirtfi = utils.has_EntityAttributes(EntityDescriptor,
                                                       'urn:oasis:names:tc:SAML:attribute:assurance-certification',
                                                       'https://refeds.org/sirtfi')

                # Get SP required attributes
                sp_required_attributes = utils.get_required_attributes(EntityDescriptor)
                if args.debug: print(f"sp_required_attributes: {sp_required_attributes}")

                # Convert OID to Name attributes
                o2n = attribute_map.oid2name
                sp_attrs_list = []
                for attr in sp_required_attributes:
                    sp_attrs_list.append(o2n[attr])

                # 1) If SP implement RS and IdP support it: releases all set of attributes
                if sp_rs and idp_rs:
                    sp_attrs_list = ['eduPersonPrincipalName', 'eduPersonTargetedID', 'eduPersonScopedAffiliation',
                                     'mail', 'displayName', 'givenName', 'sn']

                # 2) If SP is not member of the federation: remove all required attributes except eduPersonScopedAffiliation
                # 2) If SP implements RS, but IdP does not support it: remove all required attributes except eduPersonScopedAffiliation
                # 2) If SP implements CoCo, but IdP does not support it: remove all required attributes except eduPersonScopedAffiliation
                # 2) If IdP supports RS, but SP does not implement it: remove all required attributes except eduPersonScopedAffiliation
                # 2) If IdP supports CoCo, but SP does not implement it: remove all required attributes except eduPersonScopedAffiliation
                elif sp_regAuth != 'http://www.idem.garr.it/':
                    sp_attrs_list = ['eduPersonScopedAffiliation']

                # 3) Otherwise release all attributes required only

                # Discover if SP prefers 'persistent' NameID from IdP
                sp_requests_persistent_nameid = utils.sp_requests_persistent_nameid(EntityDescriptor)
                if args.debug:
                    print(f"{sp_entityID} requests persistent NameID? {sp_requests_persistent_nameid}")
                # Add 'eduPersonTargetedID' if SP does not have 'persistent' as first <md:NameIDFormat>
                if sp_requests_persistent_nameid is False: sp_attrs_list.append('eduPersonTargetedID')

                if args.debug:
                    print(f"IDP:{entityid_idp}, SP:{sp_entityID}, sp_regAuth:{sp_regAuth}")
                    print(f"Attributes:{sp_attrs_list}")

                sp_arp_dict = {
                    'sp_entityid': sp_entityID,
                    'arp_priority': '51',
                    'sp_attribute_list': utils.get_list_of_attributes_for_arp(sp_attrs_list)
                }
                sp_arp_list.append(sp_arp_dict)

        if output_php_arp is None:
            print(template.render(sp_arp_list=sp_arp_list))
        else:
            with open(output_php_arp, 'w') as f:
                f.write(template.render(sp_arp_list=sp_arp_list))
