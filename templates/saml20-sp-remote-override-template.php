{% extends "base.php" %}
{% block body %}
{%- for item in sp_arp_list %}
/* ARP for {{item.sp_entityid}} */
$metadata['{{item.sp_entityid}}']['authproc'] = [
      {{ item.arp_priority }} => [
        'class' => 'core:AttributeLimit',
        {{ item.sp_attribute_list }}
      ],
    ],
];
{% endfor -%}
{% endblock %}