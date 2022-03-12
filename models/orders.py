# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, float_repr
from datetime import date
import time
# import fcntl
# import socket
# import struct
# import macpath
from uuid import getnode as get_mac
from odoo.exceptions import UserError, ValidationError


class AutomaticRehlaRecord(models.Model):
    _inherit = 'automatic.rehla.record'
    _order = 'id desc'

    end_date = fields.Date(string='Date', default=fields.Date.context_today, required=True)




    @api.onchange('start_date','end_date')
    def onchange_start_date(self):
        so_list = []
        self.op_lines = False
        for each_inv in self.env['sale.order'].search([('state', '=', 'draft'),('creation_date','>=',self.start_date),('creation_date','<=',self.end_date),]):
            amount_final = 0
            if each_inv:
                for sale_line in each_inv.order_line:
                    Vat_Custom = self.env['account.tax'].search(
                        [('name', '=', 'VAT 15%'), ('type_tax_use', '=', 'sale')])
                    cal_amount = sale_line.price_unit + each_inv.airport_additional + each_inv.transportation_aut
                    cal_total = 0
                    amount_final = cal_amount
                    if each_inv.percentage:
                        caliculate = cal_amount * each_inv.percentage / 100
                        revenue_tax = self.env['account.tax'].search(
                            [('name', '=', 'Tax&System Revenue'), ('type_tax_use', '=', 'sale')])
                        cal_total = cal_amount + caliculate
                        amount_final+=caliculate
                    Coupon_Tax = self.env['account.tax'].search(
                        [('name', '=', 'Coupon'), ('type_tax_use', '=', 'sale')])
                    if each_inv.coupon_value:
                        Coupon_Tax.amount = each_inv.coupon_value
                        cal_total = cal_total + Coupon_Tax.amount
                        amount_final = amount_final+Coupon_Tax.amount
                    else:
                        Coupon_Tax.amount = 0
                        cal_total = cal_total + Coupon_Tax.amount
                        amount_final = amount_final- Coupon_Tax.amount
                    if each_inv.vat_percentage:
                        caliculates = cal_total * each_inv.vat_percentage / 100
                        amount_final +=caliculates
            so_dict = (0, 0, {
                'partner_id': each_inv.partner_id.id,
                'sale_id': each_inv.id,
                'trip_id': each_inv.trip_id,
                'rehla_id': each_inv.rehla_id,
                'state': each_inv.state,
                'amount': each_inv.amount_total,
                'final_amount':amount_final
            })
            so_list.append(so_dict)

        self.op_lines = so_list
    def auto_confirm_all(self):
        super(AutomaticRehlaRecord, self).auto_confirm_all()
        self.write({'state': 'close'})
