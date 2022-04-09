#!/usr/bin/env python3

namespaces = {
    'xml': 'http://www.w3.org/XML/1998/namespace',
    'md': 'urn:oasis:names:tc:SAML:2.0:metadata',
    'mdrpi': 'urn:oasis:names:tc:SAML:metadata:rpi',
    'shibmd': 'urn:mace:shibboleth:metadata:1.0',
    'mdattr': 'urn:oasis:names:tc:SAML:metadata:attribute',
    'saml': 'urn:oasis:names:tc:SAML:2.0:assertion',
    'ds': 'http://www.w3.org/2000/09/xmldsig#',
    'mdui': 'urn:oasis:names:tc:SAML:metadata:ui',
    'remd': 'http://refeds.org/metadata'
}


# Return the value of 'entityID'
def get_entityID(EntityDescriptor):
    return EntityDescriptor.get('entityID')


# Return the value of 'registrationAuthority'
def get_RegistrationAuthority(EntityDescriptor):
    reg_info = EntityDescriptor.find("./md:Extensions/mdrpi:RegistrationInfo", namespaces)

    if reg_info is not None:
        return reg_info.get("registrationAuthority")
    else:
        return ''


# Returns the XML element if found or None
def has_EntityAttributes(EntityDescriptor, AttributeName, AttributeValue):
    return True if EntityDescriptor.find(
        f"./md:Extensions/mdattr:EntityAttributes/saml:Attribute[@Name='{AttributeName}'][saml:AttributeValue='{AttributeValue}']",
        namespaces) else False


# Returns True if 'persistent' is the preferred NameIDFormat for SP, otherwise return False
def sp_requests_persistent_nameid(EntityDescriptor):
    first_nameid_format = EntityDescriptor.find("./md:SPSSODescriptor/md:NameIDFormat", namespaces)
    if first_nameid_format is not None:
        return True if first_nameid_format.text == 'urn:oasis:names:tc:SAML:2.0:nameid-format:persistent' else False
    else:
        return False


# Return True if IdP support NameID 'persistent'
def idp_supports_persistent_nameid(EntityDescriptor):
    nameid_formats = EntityDescriptor.findall("./md:IDPSSODescriptor/md:NameIDFormat", namespaces)

    if nameid_formats is not None:
        for nameid in nameid_formats:
            if (nameid.text == 'urn:oasis:names:tc:SAML:2.0:nameid-format:persistent'):
                return True
            else:
                return False
    # All other cases
    return False


# Return a list of Required Attributes from the SP metadata
def get_required_attributes(EntityDescriptor):
    required_attributes_list = list()
    required_attrs = EntityDescriptor.findall(
        "./md:SPSSODescriptor/md:AttributeConsumingService/md:RequestedAttribute[@isRequired='true']", namespaces)
    if required_attrs is not None:
        for ra in required_attrs:
            required_attributes_list.append(ra.get('Name'))

    return required_attributes_list


def get_list_of_attributes_for_arp(attribute_list):
    result = ''

    for attribute in attribute_list:
        result = result + f"'{attribute}',"

    return result


# Return a list of Contacts on the SP metadata
def get_Sirtfi_Contacts(EntityDescriptor):
    contact_list = list()
    contacts = EntityDescriptor.findall(
        "./md:ContactPerson[@contactType='other' and @remd:contactType='http://refeds.org/metadata/contactType/security']/md:EmailAddress",
        namespaces)
    for ctc in contacts:
        if ctc is not None:
            if ctc.text.startswith("mailto:"):
                contact_list.append(ctc.text)
            else:
                contact_list.append("mailto:" + ctc.text)

    return contact_list
