#!/usr/bin/env python3

# entity_categories structures:
#
#   "<entity-category-uri>:" {
#       "attributes": [
#           "<attribute_name_1>": {
#               "onlyIfRequired": False,  # The <md:RequestedAttribute> MUST BE into SP metadata with isRequired='True'
#               "onlyIfRequested": False,  # The <md:RequestedAttribute MAY NOT BE into SP metadata
#           }
#       ],
#       "<attribute_name_2>": {
#           "onlyIfRequired": False,  # The <md:RequestedAttribute> MUST BE into SP metadata with isRequired='True'
#           "onlyIfRequested": False,  # The <md:RequestedAttribute MAY NOT BE into SP metadata
#       }
#   }

entity_categories = {
    "http://refeds.org/category/research-and-scholarship": {
        "attributes": {
            "eduPersonPrincipalName": {
                "onlyIfRequired": False,
                "onlyIfRequested": False,
            },
            "eduPersonTargetedID": {
                "onlyIfRequired": False,
                "onlyIfRequested": False,
            },
            "eduPersonScopedAffiliation": {
                "onlyIfRequired": False,
                "onlyIfRequested": False,
            }
        }
    },
    "http://www.geant.net/uri/dataprotection-code-of-conduct/v1": {
        "attributes": {
            "mail": {
                "onlyIfRequired": True,
                "onlyIfRequested": True,
            },
            "eduPersonPrincipalName": {
                "onlyIfRequired": True,
                "onlyIfRequested": True,
            },
            "displayName": {
                "onlyIfRequired": True,
                "onlyIfRequested": True,
            },
            "eduPersonAffiliation": {
                "onlyIfRequired": True,
                "onlyIfRequested": True,
            },
            "eduPersonOrcid": {
                "onlyIfRequired": True,
                "onlyIfRequested": True,
            },
            "sn": {
                "onlyIfRequired": True,
                "onlyIfRequested": True,
            },
            "givenName": {
                "onlyIfRequired": True,
                "onlyIfRequested": True,
            },
            "eduPersonEntitlement": {
                "onlyIfRequired": True,
                "onlyIfRequested": True,
            },
            "cn": {
                "onlyIfRequired": True,
                "onlyIfRequested": True,
            },
            "eduPersonOrgDN": {
                "onlyIfRequired": True,
                "onlyIfRequested": True,
            },
            "title": {
                "onlyIfRequired": True,
                "onlyIfRequested": True,
            },
            "telephoneNumber": {
                "onlyIfRequired": True,
                "onlyIfRequested": True,
            },
            "eduPersonOrgUnitDN": {
                "onlyIfRequired": True,
                "onlyIfRequested": True,
            },
            "schacPersonalTitle": {
                "onlyIfRequired": True,
                "onlyIfRequested": True,
            },
            "schacPersonalUniqueID": {
                "onlyIfRequired": True,
                "onlyIfRequested": True,
            },
            "schacPersonalUniqueCode": {
                "onlyIfRequired": True,
                "onlyIfRequested": True,
            },
            "schacHomeOrganization": {
                "onlyIfRequired": True,
                "onlyIfRequested": True,
            },
            "schacHomeOrganizationType": {
                "onlyIfRequired": True,
                "onlyIfRequested": True,
            },
            "schacUserPresenceID": {
                "onlyIfRequired": True,
                "onlyIfRequested": True,
            },
            "schacMotherTongue": {
                "onlyIfRequired": True,
                "onlyIfRequested": True,
            },
            "mobile": {
                "onlyIfRequired": True,
                "onlyIfRequested": True,
            },
            "preferredLanguage": {
                "onlyIfRequired": True,
                "onlyIfRequested": True,
            },
            "schacGender": {
                "onlyIfRequired": True,
                "onlyIfRequested": True,
            },
            "schacDateOfBirth": {
                "onlyIfRequired": True,
                "onlyIfRequested": True,
            },
            "schacPlaceOfBirth": {
                "onlyIfRequired": True,
                "onlyIfRequested": True,
            },
            "schacCountryOfCitizenship": {
                "onlyIfRequired": True,
                "onlyIfRequested": True,
            },
            "schacSn1": {
                "onlyIfRequired": True,
                "onlyIfRequested": True,
            },
            "schacSn2": {
                "onlyIfRequired": True,
                "onlyIfRequested": True,
            },
            "schacCountryOfResidence": {
                "onlyIfRequired": True,
                "onlyIfRequested": True,
            },
            "schacExpiryDate": {
                "onlyIfRequired": True,
                "onlyIfRequested": True,
            },
            "schacUserPrivateAttribute": {
                "onlyIfRequired": True,
                "onlyIfRequested": True,
            },
            "schacUserStatus": {
                "onlyIfRequired": True,
                "onlyIfRequested": True,
            },
            "schacProjectMembership": {
                "onlyIfRequired": True,
                "onlyIfRequested": True,
            },
            "schacProjectSpecificRole": {
                "onlyIfRequired": True,
                "onlyIfRequested": True,
            },
            "schacYearOfBirth": {
                "onlyIfRequired": True,
                "onlyIfRequested": True,
            },
            "eduPersonNickname": {
                "onlyIfRequired": True,
                "onlyIfRequested": True,
            },
            "eduPersonPrimaryAffiliation": {
                "onlyIfRequired": True,
                "onlyIfRequested": True,
            },
            "eduPersonPrimaryOrgUnitDN": {
                "onlyIfRequired": True,
                "onlyIfRequested": True,
            },
            "eduPersonAssurance": {
                "onlyIfRequired": True,
                "onlyIfRequested": True,
            },
            "eduPersonPrincipalNamePrior": {
                "onlyIfRequired": True,
                "onlyIfRequested": True,
            },
            "eduPersonUniqueId": {
                "onlyIfRequired": True,
                "onlyIfRequested": True,
            }
        }
    }
}
