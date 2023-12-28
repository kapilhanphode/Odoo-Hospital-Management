from odoo import api,fields,models,_


class Opeartion(models.Model):
    _name = 'hospital.operation'
    _log_access = False
    _rec_name = 'doctor_id'
    _order = 'sequence, id'

    operation_name = fields.Char('Operation Name')
    doctor_id = fields.Many2one('res.users',string='Doctor')
    reference = fields.Reference([('hospital.patient', 'Patient'),
                                  ('patient.appointment','Appointment')],string='Record')
    sequence = fields.Integer('Sequence',default=10)

    @api.model
    def name_create(self, name):
        print('-----------------name',name)
        result = super().create({"operation_name": name, "value": float(name)})
        return result.name_get()[0]