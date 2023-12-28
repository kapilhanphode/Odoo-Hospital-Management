from odoo import api,fields,models,_
from datetime import date

class PatientTag(models.Model):
    _name = 'patient.tag'
    _description = 'Hospital Patient Tag'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Name',required=True)
    active = fields.Boolean('Active',default=True)
    color = fields.Integer('Color',copy=False)
    color_2 = fields.Char('Color2')
    sequence = fields.Integer('Sequence')

    _sql_constraints = [
        ('unique_name', 'unique (name)', 'Tag Name must be unique!'),
        ('check_sequence', 'CHECK(sequence>=0)', 'Sequence must be 0 or Greater than 0')
    ]

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('name'):
            default['name'] = _("%s (copy)") % (self.name)
        project = super(PatientTag, self).copy(default)
        return project

