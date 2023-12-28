from  odoo import api,fields,models
from odoo.exceptions import ValidationError


class PatientAppointment(models.Model):
    _name = 'patient.appointment'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = 'Hospital Patient Appointment Details'
    _rec_name = 'patient_id'
    _order = 'id desc'

    patient_id = fields.Many2one('hospital.patient','Patient Name',ondelete='cascade')
    booking_date = fields.Date('Booking Date', default=fields.Date.context_today)
    appointment_time = fields.Datetime('Appointment Time',default=fields.Datetime.now)
    gender = fields.Selection(related='patient_id.gender',readonly=False)
    reference = fields.Char('Reference',help='Reference of Patient')
    prescription = fields.Html('Prescription')
    priority = fields.Selection([('0', 'Very Low'), ('1', 'Low'), ('2', 'Normal'), ('3', 'High')], string='Priority')
    state = fields.Selection([('draft', 'Draft'), ('in_consultation', 'In Consultation'), ('done', 'Done'), ('cancel', 'Cancel')],default='draft')
    doctor_id = fields.Many2one('res.users','Doctor')
    pharmacy_line_ids = fields.One2many('appointment.pharmacy.line','appointment_id','Pharmacy Line')
    hide_unit_price = fields.Boolean('Hide Sales Price')
    operation = fields.Many2one('hospital.operation','Operation')
    progress = fields.Integer('Progress',compute='_compute_progress')
    duration = fields.Float('Duration')
    company_id = fields.Many2one('res.company',string='Company',default=lambda self:self.env.company)
    currency_id = fields.Many2one(comodel_name='res.currency', related='company_id.currency_id')

    def action_send_email(self):
        template = self.env.ref('om_hospital.mail_template_patient_appointment')
        print('template',template)
        for rec in self:
            if rec.patient_id.email:
                #email_values = {'subject':'Test OM Hospital'}
                print('send email')
                template.send_mail(rec.id,force_send=True)#,email_values=email_values
            else:
                raise ValidationError('No Email found of this user')

    @api.model
    def create(self,vals):
        res = super(PatientAppointment, self).create(vals)
        print('++++++++++++++++++++res',res)
        sr_no = 0
        for line in res.pharmacy_line_ids:
            print('++++++++++++++++++++++line',line.product_id.name)
            sr_no+=1
            line.sr_no = sr_no
        return res

    def write(self,vals):
        res = super(PatientAppointment, self).write(vals)
        print('++++++++++++++++++++++res write',res)
        sr_no = 0
        for line in self.pharmacy_line_ids:
            print('++++++++++++++++++++++line', line.product_id.name)
            sr_no += 1
            line.sr_no = sr_no
        return res

    def action_notification(self):
        action = self.env.ref('om_hospital.action_hospital_patient_appointment')
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'type': 'success',
                'sticky': False,
                'message': '%s',
                'links': [{
                    'label':self.patient_id.patient_name,
                    'url': f'#action={action.id}&id={self.id}&model=patient.appointment'
                }],
                'sticky':True,
                'next':{
                    'type':'ir.actions.act_window',
                    'res_model':'hospital.patient',
                    'res_id':self.patient_id.id,
                    'views':[(False,'form')]
                }
            }
        }

    def action_share_whatsapp(self):
        print('hello hello')
        msg = 'Hi %s' % self.patient_id.patient_name
        whatsapp_api_url = 'https://api.whatsapp.com/send?phone=%s&text=%s' % (self.patient_id.phone,msg)
        self.message_post(body=msg,subject='Whats app message')
        return {
            'type': 'ir.actions.act_url',
            'url': whatsapp_api_url,
            # 'target':'self'
        }


    @api.depends('state')
    def _compute_progress(self):
        for rec in self:
            if rec.state == 'draft':
                progress = '25'
            elif rec.state == 'in_consultation':
                progress = '50'
            elif rec.state == 'done':
                progress = '100'
            else:
                progress = 0
            rec.progress = progress


    @api.onchange('patient_id')
    def onchange_patient_id(self):
        self.reference = self.patient_id.reference

    def object_test(self):
        print('-----------------------------object test')
        return{
            'type':'ir.actions.act_url',
            'url':'https://www.odoo.com',
            #'target':'self'
        }
        # return {
        #     'effect': {
        #         'fadeout': 'slow',
        #         'message': "Click Successful",
        #          'type': 'rainbow_man',
        #     }
        # }

    def action_in_consultation(self):
        for rec in self:
            if rec.state == 'draft':
                rec.state = 'in_consultation'

    def action_mark_as_done(self):
        for rec in self:
            rec.state = 'done'

    def action_cancel(self):
        for rec in self:
            action = rec.env.ref('om_hospital.action_cancel_patient_appointment').read()[0]
            return action

    def action_reset_to_draft(self):
        for rec in self:
            rec.state = 'draft'

    def unlink(self):
        for rec in self:
            print('unlink---------------')
            if rec.state != 'draft':
                raise ValidationError('You Can only Delete Appointment in Draft State!')
            return super(PatientAppointment, rec).unlink()




class AppointmentPharmacyLine(models.Model):
    _name = 'appointment.pharmacy.line'

    product_id = fields.Many2one('product.product',required=True)
    price_unit = fields.Float('Price',related='product_id.list_price')
    qty = fields.Integer('Quantity')
    appointment_id = fields.Many2one('patient.appointment','Appointment')
    currency_id = fields.Many2one('res.currency',related='appointment_id.currency_id')
    price_subtotal = fields.Monetary('Subtotal',compute='_compute_price_subtotal')
    sr_no = fields.Integer('Sr.no.',readonly=1)

    @api.depends('price_unit','qty')
    def _compute_price_subtotal(self):
        for rec in self:
            rec.price_subtotal = rec.price_unit * rec.qty