from odoo import api,fields,models
from datetime import date
from odoo.tools.safe_eval import safe_eval

class OdooPlayGround(models.Model):
    _name = 'odoo.playground'
    _description = 'Hospital Patient Details'


    DEFAULT_ENV_VARIABLES = """# Available variables:
    # - self: Currnet Object
    # - self.env: Odoo Environment on which the action is triggered"""

    model_id = fields.Many2one('ir.model','Model')
    code = fields.Text('Code',default=DEFAULT_ENV_VARIABLES)
    result = fields.Text('Result')

    def action_execute(self):
        try:
            if self.model_id:
                model = self.env[self.model_id.model]
            else:
                model = self
            self.result = safe_eval(self.code.strip(),{'self':model})
        except Exception as e:
            self.result = str(e)




