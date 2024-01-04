from odoo import api,fields,models,_
from datetime import date
from odoo.exceptions import ValidationError
from dateutil import relativedelta
from datetime import date


class Patient(models.TransientModel):
    _name = 'cancel.patient.appointment'
    _description = 'Cancel Patient Appointment'

    @api.model
    def default_get(self, fields):
        res = super(Patient, self).default_get(fields)

        print('----------------------------contex',self.env.context.get('active_id'))
        if self.env.context.get('active_id'):
            res['appointment_id'] = self.env.context.get('active_id')
        return res

    appointment_id = fields.Many2one('patient.appointment',domain=[('state','=','draft')])
    cancellation_reason = fields.Text('Reason')
    cancel_date = fields.Datetime('Cancel Date',default=fields.Datetime.now)

    def cancel_patient_appointment(self):
        cancel_days = self.env['ir.config_parameter'].sudo().get_param('om_hospital.cancel_days')
        print('cancel_day-----------------------------',cancel_days)
        print('booking_day-----------------------------',self.appointment_id.booking_date)
        allowed_date = self.appointment_id.booking_date - relativedelta.relativedelta(days=int(cancel_days))
        print('allowed_date---------',allowed_date)
        print('date.today()---------',date.today())
        if allowed_date < date.today():
            raise ValidationError("You cannot cancel this appointment!")
        # if self.appointment_id.booking_date == fields.Date.today():
        #     raise ValidationError("You cannot cancel today's appointment!")

        query = """select patient_name from hospital_patient"""
        patient_name = self.env.cr.execute(query)
        print('++++++++++++++patient_name',patient_name)
        patients = self.env.cr.fetchall()
        print('++++++++++++++++++++++patient',patients)

        self.appointment_id.state = 'cancel'
        # return {
        #     'type': 'ir.actions.client',
        #     'tag': 'reload',
        # }

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'cancel.patient.appointment',
            'view_mode': 'form',
            'target': 'new',
            'res_id':self.id
        }