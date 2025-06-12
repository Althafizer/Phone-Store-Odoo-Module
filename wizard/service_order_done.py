from odoo import api, models, fields, tools
from odoo.exceptions import ValidationError, UserError

from datetime import timedelta


class ServiceOrderDone(models.TransientModel):
    _name = 'service.order.done.wizard'

    warranty_type = fields.Selection([
        ("7d", "7 Days"),
        ("14d", "14 Days"),
        ("30d", "30 Days"),
        ("90d", "90 Days"),
        ("6m", "6 Months"),
        ("1y", "1 Year"),
        ("custom", "Custom"),
    ], string="Warranty Type", required=True, default="30d")
    warranty_end_date = fields.Datetime(
        string="Warranty End Date",
        required=True,
        default=lambda self: fields.datetime.now()+timedelta(days=30)
    )

    @api.onchange("warranty_type")
    def _onchange_warranty_type(self):
        if self.warranty_type == "7d":
            self.warranty_end_date = fields.datetime.now()+timedelta(days=7)
        if self.warranty_type == "14d":
            self.warranty_end_date = fields.datetime.now()+timedelta(days=14)
        elif self.warranty_type == "30d":
            self.warranty_end_date = fields.datetime.now()+timedelta(days=30)
        elif self.warranty_type == "90d":
            self.warranty_end_date = fields.datetime.now()+timedelta(days=90)
        elif self.warranty_type == "6m":
            self.warranty_end_date = fields.datetime.now()+timedelta(days=180)
        elif self.warranty_type == "1y":
            self.warranty_end_date = fields.datetime.now()+timedelta(days=365)

    def done(self):
        self.ensure_one()

        service_order_id = self.env['service.order'].sudo().browse(self._context.get('service_order_id'))
        if not service_order_id:
            raise ValidationError("Invalid Service Order")
        
        service_order_id.state = "done"
        service_order_id.warranty_end_date = self.warranty_end_date
        service_order_id.done_date = fields.datetime.now()
        