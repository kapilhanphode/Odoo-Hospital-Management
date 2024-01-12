# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Hospital Management',
    'version' : '1.0.0',
    'summary': 'Hospital Management Summary',
    'sequence': -100,
    'description': """
Hospital Management By Kapil.
    """,
    'author':'Kapil',
    'category': '',
    'website': 'https://www.odoo.com/app/invoicing',
    'images' : [],
    'depends' : ['mail','product'],
    'data': [
        'security/ir.model.access.csv',
        'data/patient_tag_data.xml',
        'data/sequence_data.xml',
        'data/patient.tag.csv',
        'data/mail_template_data.xml',
        'wizard/cancel_patient_appointment.xml',
        'views/patient_menu.xml',
        'views/female_patient.xml',
        'views/male_patient.xml',
        'views/patient_appointment.xml',
        'views/patient_tag.xml',
        'views/odoo_playground.xml',
        'views/res_config_settings_views.xml',
        'views/operation.xml',
    ],
    'demo': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,

}
