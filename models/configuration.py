from odoo import api, fields, models, _

class ServiceManagementDevice(models.Model):
    _name = "service.management.device"
    _description = "Devices"
    _rec_name = 'name'

    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string="Active", default=True)
    device_type = fields.Selection([
        ("iphone", "IPhone"),
        ("ipad", "IPad"),
        ("applewatch", "Apple Watch"),
        ("macbook", "MacBook"),
        ("airpods", "AirPods"),
        ("android", "Android"),
    ], string="Type", required=True)

class ServiceManagementDeviceColor(models.Model):
    _name = "service.management.device.color"
    _description = "Service Device Color"
    _rec_name = 'name'

    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string="Active", default=True)

class ServiceManagementDeviceRAM(models.Model):
    _name = "service.management.device.ram"
    _description = "Service Device RAM"
    _rec_name = 'name'

    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string="Active", default=True)

class ServiceManagementDeviceStorage(models.Model):
    _name = "service.management.device.storage"
    _description = "Service Device Storage"
    _rec_name = 'name'

    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string="Active", default=True)

class ServiceManagementService(models.Model):
    _name = "service.management.service"
    _description = "Service Management Service"
    _rec_name = 'name'

    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string="Active", default=True)

class ServiceManagementSparepart(models.Model):
    _name = "service.management.sparepart"
    _description = "Spareparts"
    _rec_name = 'name'

    # TODO: make constraint

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    active = fields.Boolean(string="Active", default=True)

class ServiceManagementAccessories(models.Model):
    _name = "service.management.accessories"
    _description = "Accessories"
    _rec_name = 'name'

    # TODO: make constraint

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    active = fields.Boolean(string="Active", default=True)

class ServiceManagementComponent(models.Model):
    _name = "service.management.component"
    _description = "Components"

    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string="Active", default=True)

class ServiceManagementCompany(models.Model):
    _name = "service.management.company"
    _description = "Service management company"
    _rec_name = 'name'

    name = fields.Char(string="Company Name", required=True)
    # related_company = fields.Many2one(string="Related Company", comodel_name="res.company", required=True)
    # company_type = fields.Selection([], string="Company Type", related="related_company.company_type", store=True)
    # pic_user_id = fields.Many2one(comodel_name="res.users", string="PIC", required=True)
    active = fields.Boolean(string="Active", default=True)
