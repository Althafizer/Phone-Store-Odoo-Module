from odoo import api, fields, models, _

class ServiceOrderChecklist(models.Model):
    _name = "service.order.checklist"
    _description = "Service order checklist line"

    @api.model
    def create(self, vals):
        if self.env.user:
            vals['asignee_user_id'] = self.env.user.id
        
        return super(ServiceOrderChecklist, self).create(vals)

    service_order_id = fields.Many2one(comodel_name="service.order")
    checklist_date = fields.Datetime(string="Checklist Date", default=lambda self: fields.datetime.now())
    asignee_user_id = fields.Many2one(comodel_name="res.users", string="Asignee")
    checklist_template_id = fields.Many2one(string="Checklist Template", comodel_name="service.order.checklist.template")

    @api.onchange("checklist_template_id")
    def on_change_checklist_template_id(self):
        if self.checklist_template_id:
            service_order_checklist_line_ids = []
            for line in self.checklist_template_id.service_order_checklist_line_ids:
                if line.component_id:
                    service_order_checklist_line_ids.append(
                        (0, 0, {'service_order_checklist_id': self.id, 'component_id': line.component_id.id})
                    )
            self.service_order_checklist_line_ids = service_order_checklist_line_ids

    service_order_checklist_line_ids = fields.One2many(
        comodel_name="service.order.checklist.line",
        inverse_name="service_order_checklist_id",
        string="Cheklists"
    )
    notes = fields.Text(string="Description", required=True)

class ServiceOrderChecklistLine(models.Model):
    _name = "service.order.checklist.line"
    _description = "Service order checklist line"

    service_order_checklist_id = fields.Many2one(comodel_name="service.order.checklist")
    component_id = fields.Many2one(comodel_name="service.management.component", string="Component")
    condition = fields.Selection([
        ("normal", "Normal"),
        ("trouble", "Trouble"),
        ("notifikasi_servis", "Notifikasi Servis")
    ], string="Condition", required=True)
    description = fields.Text(string="Description")


# Checklist Template
class ServiceOrderChecklistTemplate(models.Model):
    _name = "service.order.checklist.template"
    _description = "A list of checklist. Template for service order"
    _rec_name = 'name'

    name = fields.Char(string="Name", required=True)
    service_order_checklist_line_ids = fields.One2many(
        comodel_name="service.order.checklist.line.template",
        inverse_name="service_order_checklist_template_id",
        string="Cheklist Components"
    )
    active = fields.Boolean(string="Active", default=True)

class ServiceOrderChecklistLineTemplate(models.Model):
    _name = "service.order.checklist.line.template"
    _description = "A list of checklist. Template for service order"

    service_order_checklist_template_id = fields.Many2one(comodel_name="service.order.checklist.template")
    component_id = fields.Many2one(comodel_name="service.management.component")
