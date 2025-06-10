import logging
from datetime import date
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class ServiceOrder(models.Model):
    _name = "service.order"
    _description = "Service order."
    _rec_name = 'name'

    @api.model
    def create(self, vals):
        if not vals.get('name', False) or vals['name'] == _("New"):
            vals['name'] = self.env['ir.sequence'].sudo().next_by_code('service.order')
        
        return super(ServiceOrder, self).create(vals)\
        
    name = fields.Char(string="Order Reference", required=True, readonly=True, default=lambda self: _('New')), active = fields.Boolean(string="Active", default=True)

    customer_name = fields.Char(string="Customer Name", required=True)
    customer_phone = fields.Char(string="Customer Phone", required=True)
    memo = fields.Html(string="Memo")

    is_warranty = fields.Boolean(string="Is Warranty ?", default=False)
    previous_order_warranty = fields.Many2one(comodel_name="service.order", string="Previouse Order", tracking=True)
    warranty_end_date = fields.Datetime(string="Warranty End Date")

    @api.onchange("previous_order_warranty")
    def _onchanve_previous_order_warranty(self):
        if self.state == "agent_check" and self.previous_order_warranty.id:
            if self.previous_order_warranty.state != "done" :
                raise ValidationError("This Previous is not finished yet. Change the state to Done first!")
            
            if self.previous_order_warranty.warranty_end_date < fields.datetime.now():
                raise ValidationError("This service order warranty is expired")

            self.customer_name = self.previous_order_warranty.customer_name
            self.service_device_color_id = self.previous_order_warranty.service_device_color_id
            self.service_device_ram_id = self.previous_order_warranty.service_device_ram_id
            self.service_device_storage_id = self.previous_order_warranty.service_device_storage_id
            self.service_device_network = self.previous_order_warranty.service_device_network
            self.service_device_year = self.previous_order_warranty.service_device_year
            self.service_device_size = self.previous_order_warranty.service_device_size
            self.service_device_processor = self.previous_order_warranty.service_device_processor
            self.service_device_appelwatch_size = self.previous_order_warranty.service_device_appelwatch_size
            self.service_device_mac_processor = self.previous_order_warranty.service_device_mac_processor
            self.service_device_mac_size = self.previous_order_warranty.service_device_mac_size
            self.service_device_mac_touchbar = self.previous_order_warranty.service_device_mac_touchbar
            self.imei_number = self.previous_order_warranty.imei_number
            self.passkey = self.previous_order_warranty.passkey 

    order_date = fields.Datetime(string="Request Date", default=lambda self: fields.datetime.now())
    estimated_date = fields.Date(string="Estimated Date", tracking=True)
    done_date = fields.Datetime(string="Done Date")
    cancel_date = fields.Datetime(string="Cancel Date")

    service_device_id = fields.Many2one(
        comodel_name="service.management.device",
        string="Service Device",
        required=True)
    service_device_type = fields.Selection([], string="Type", related="service_device_id.device_type")
    service_device_color_id = fields.Many2one(comodel_name="service.management.device.color", string="Color")
    service_device_ram_id = fields.Many2one(comodel_name="service.management.device.ram", string="RAM")
    service_device_storage_id = fields.Many2one(comodel_name="service.management.device.storage", string="Storage")
    service_device_network = fields.Selection([("wifi_only", "Wifi Only"), ("cellular", "Cellular")], string="Network")
    service_device_year = fields.Char(string="Year")
    service_device_size = fields.Char(string="Size") # To be deleted soon
    service_device_processor = fields.Char(string="Processor") # To be deleted soon
    service_device_appelwatch_size = fields.Selection([
        ("38mm", "38mm"),
        ("40mm", "40mm"),
        ("41mm", "41mm"),
        ("42mm", "42mm"),
        ("44mm", "44mm"),
        ("45mm", "45mm"),
    ], string="Apple Watch Size")
    service_device_mac_processor = fields.Selection([
        ("intel_i3", "Intel i3"),
        ("intel_i5", "Intel i5"),
        ("intel_i7", "Intel i7"),
        ("intel_i9", "Intel i9"),
        ("m1", "M1"),
        ("m2", "M2"),
        ("m3", "M3")
    ], string="MacBook Processor")
    service_device_mac_size = fields.Selection([
        ("13inch", "13 inch"),
        ("12inch", "12 inch"),
        ("14inch", "14 inch"),
        ("15inch", "15 inch"),
        ("16inch", "16 inch"),
        ("17inch", "17 inch"),
    ], string="MacBook Size")
    service_device_mac_touchbar = fields.Boolean(string="With Touchbar ?")
    imei_number = fields.Char(string="IMEI Number")
    passkey = fields.Char(string="Passkey")

    @api.onchange("service_device_id")
    def _onchange_service_device_type(self):
        self.service_device_color_id = None
        self.service_device_ram_id = None
        self.service_device_storage_id = None
        self.service_device_network = None
        self.service_device_year = None
        self.service_device_size = None
        self.service_device_processor = None
        self.service_device_appelwatch_size = None
        self.service_device_mac_processor = None
        self.service_device_mac_size = None
        self.service_device_mac_touchbar = None

    cancel_note = fields.Char(string="Cancel Note", tracking=True)
    customer_note = fields.Char(string="Note For Customer", tracking=True)

    state = fields.Selection([
        ("agent_check", "Agent Check"),
        ("prepare_to_service_center", "Preparing To Service Center"),
        ("service_center_delivery", "Delivery To Service Center"),
        ("agent_delivery", "Delivery To Agent"),
        ("service_center", "Service Center"),
        ("service_center_resolved", "Service Center Resolved"),
        ("service_center_cancel", "Service Center Cancel"),
        ("service_center_waiting_sparepart", "Waiting For Sparepart (Service Center)"),
        ("service_center_customer_confirmation", "Customer Confirmation (Service Center)"),
        ("agent_waiting_sparepart", "Waiting For Sparepart (Agent)"),
        ("agent_customer_confirmation", "Customer Confirmation (Agent)"),
        ("recheck_from_service_center", "Re-Check From Service Center"),
        ("agent_resolved", "Agent Resolved"),
        ("cancel", "Cancel"),
        ("done", "Received By Customer")
    ], string="State", default='agent_check', tracking=True, required=True)

    service_order_checklist_ids = fields.One2many(
        comodel_name="service.order.checklist",
        inverse_name="service_order_id",
        string="Cheklist History"
    )

    service_order_sparepart_ids = fields.One2many(
        comodel_name="service.order.line.sparepart",
        inverse_name="service_order_id",
        string="Sparepart Used"
    )

    service_order_service_ids = fields.One2many(
        comodel_name="service.order.line.service",
        inverse_name="service_order_id",
        string="Services"
    )

    service_order_accessories_ids = fields.One2many(
        comodel_name="service.order.line.accessories",
        inverse_name="service_order_id",
        string="Accessories"
    )

    # Actions

    def action_mark_agent_waiting_for_sparepart(self):
        self.ensure_one()
        self.state = "agent_waiting_sparepart"
    
    def action_mark_agent_customer_confirmation(self):
        self.ensure_one()
        self.state = "agent_customer_confirmation"

    def action_continue_agent_check(self):
        self.ensure_one()
        self.state = "agent_check"

    def action_mark_agent_resolved(self):
        self.ensure_one() 
        self.state = "agent_resolved"

    def action_mark_as_cancel(self):
        self.ensure_one()

        if not self.cancel_note:
            raise ValidationError("Please fill Cancel Note first")

        self.state = "cancel"
        self.cancel_date = fields.datetime.now()

    def action_mark_as_done(self):
        self.ensure_one()

        if self.cancel_note:
            raise ValidationError("This service order can't be done. should be canceled. ")

        wizard_form = self.env.ref('service_management.service_order_done_wizard_view', False)
        if not wizard_form:
            raise ValidationError("View Not Found")
        return {
            'name'      : _('Confirmation'),
            'type'      : 'ir.actions.act_window',
            'res_model' : 'service.order.done.wizard',
            'view_id'   : wizard_form.id,
            'view_type' : 'form',
            'view_mode' : 'form',
            'target'    : 'new',
            'context'   : {'service_order_id': self.id},
        }

    def action_set_reference_name_by_request_date(self):
        self.ensure_one()
        reference_parts = self.name.split("/")
        if len(reference_parts) == 6:
            request_date_day = self.order_date.day
            request_date_month = self.order_date.month
            request_date_year = self.order_date.year
            reference_parts[2] = "{0:0=4d}".format(request_date_year)
            reference_parts[3] = "{0:0=2d}".format(request_date_month)
            reference_parts[4] = "{0:0=2d}".format(request_date_day)
            new_reference = "/".join(reference_parts)
            self.name = new_reference

    