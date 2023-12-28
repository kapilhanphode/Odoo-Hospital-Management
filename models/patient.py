from odoo import api,fields,models,_
from datetime import date
from odoo.exceptions import ValidationError
from dateutil import relativedelta


class Patient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = 'Hospital Patient Details'
    _rec_name = 'patient_name'

    patient_name = fields.Char('Patient Name',tracking=True,required=True)  #tracking=1,2,3,4
    gender = fields.Selection([('male','Male'),('female','Female')],'Gender')
    age = fields.Integer('Age',compute='_compute_age',inverse='_inverse_compute_age',search='_search_age')
    reference = fields.Char('Reference',readonly=True)
    active = fields.Boolean('Active',default=True)
    dob = fields.Date('Date of Birth')
    patient_image = fields.Image('Patient Image')
    tag_ids = fields.Many2many('patient.tag',string='Tags')
    test = fields.Char('Test')
    appointment_count = fields.Integer('Appointment Count', compute='_compute_appointment_count')
    appointment_ids = fields.One2many('patient.appointment','patient_id',string='Appointments')
    parent = fields.Char('Parent Name')
    marital_status = fields.Selection([('single','Single'),('married','Married')],'Marital Status')
    partner_name = fields.Char('Partner Name')
    is_birthday = fields.Boolean('Birthday',compute='_is_birthday',store=True)
    phone = fields.Char('Phone')
    email = fields.Char('Email')
    website = fields.Char('Website')

    def action_view_appointment(self):
        return {
            'name': _('Appointments'),
            'type': 'ir.actions.act_window',
            'res_model': 'patient.appointment',
            'view_mode': 'list,form',
            #'search_view_id': [self.env.ref('hr_holidays.view_search_hr_holidays_employee_type_report').id],
            'domain': [('patient_id','=',self.id)],
            'context': {'default_patient_id':self.id}
        }


    @api.depends('dob')
    def _is_birthday(self):
        for rec in self:
            today = date.today()
            if self.dob:
                print('today date',today)
                if today.day == rec.dob.day and today.month == rec.dob.month:
                    self.is_birthday = True
                    print('today date inside if', today)
                    print('today today Birthday')
                else:
                    self.is_birthday = False
            else:
                pass


    @api.ondelete(at_uninstall=False)
    def _check_appointments(self):
        for rec in self:
            if rec.appointment_ids:
                raise ValidationError("You cannot delete a patient with appointment!")

    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        for rec in self:
            rec.appointment_count = self.env['patient.appointment'].search_count([('patient_id','=',rec.id)])

    # @api.depends('appointment_ids')
    # def _compute_appointment_count(self):
    #     appointment_group = self.env['patient.appointment'].read_group(domain=[],fields=['patient_id'],groupby=['patient_id'])
    #     for appointment in appointment_group:
    #         patient_id = appointment.get('patient_id')[0]
    #         print('+++++++++++++++++++++++appointment',appointment)
    #         print('+++++++++++++++++++++++patient_id',patient_id)
    #         patient_rec = self.browse(patient_id)
    #         patient_rec.appointment_count = appointment['patient_id_count']
    #         self -= patient_rec
    #     self.appointment_count = 0

    @api.constrains('dob')
    def _check_dob(self):
        for rec in self:
            if rec.dob and rec.dob > fields.Date.today():
                raise ValidationError('The entered date is not Acceptable(Date of Birth is future date)')

    @api.depends('dob')
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.dob:
                rec.age = today.year - rec.dob.year - ((today.month, today.day) < (rec.dob.month, rec.dob.day))
            else:
                rec.age = 0
    @api.depends('age')
    def _inverse_compute_age(self):
        for rec in self:
            today = date.today()
            rec.dob = today - relativedelta.relativedelta(years=rec.age)

    def _search_age(self, operator, value):
        dob1 = date.today() - relativedelta.relativedelta(years=value)

        start_of_year = dob1.replace(day=1,month=1)
        end_of_year = dob1.replace(day=31,month=12)
        print('start', start_of_year)
        print('end',end_of_year)
        print('dob1',dob1)
        print('self.dob',self.dob)
        return [('dob','>=',start_of_year),('dob','<=',end_of_year)]

    @api.model
    def create(self, vals):
        vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(Patient, self).create(vals)

    def write(self,vals):
        print('write -------------vals',vals)
        if not self.test:
            vals['test'] = 'test121'
        else:
            print('present data-------------------')
        return super(Patient, self).write(vals)

    def name_get(self):
        patient_list = []
        for rec in self:
            name = '[' + rec.reference + '] ' + rec.patient_name
            patient_list.append((rec.id,name))
        return patient_list

    def action_test(self):
        print('click me------------------------')