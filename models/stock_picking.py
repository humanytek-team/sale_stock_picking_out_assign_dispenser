# -*- coding: utf-8 -*-
###############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2017 Humanytek (<www.humanytek.com>).
#    Manuel Márquez <manuel@humanytek.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

import random

from openerp import api, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def create(self, vals):

        create_result = super(StockPicking, self).create(vals)
        picking_type_delivery_order = self.env.ref('stock.picking_type_out')

        if picking_type_delivery_order:
            if vals.get('origin') and \
                    vals.get('picking_type_id') == \
                    picking_type_delivery_order.id:

                SaleOrder = self.env['sale.order']
                generated_from_sale_order = SaleOrder.search([
                    ('name', '=', vals.get('origin'))])

                if generated_from_sale_order:
                    ResUsers = self.env['res.users']
                    group_stock_user = self.env.ref('stock.group_stock_user')
                    dispensers = ResUsers.search([
                        ('groups_id', 'in', group_stock_user.id),
                        ])

                    dispensers_without_assign = list()
                    for dispenser in dispensers:
                        dispenser_assigned = \
                            dispenser.stock_picking_ids.filtered(
                                lambda p: p.picking_type_id.id ==
                                picking_type_delivery_order.id and
                                (p.state == 'partially_available' or
                                p.state == 'assigned'))

                        if not dispenser.stock_picking_ids or \
                                not dispenser_assigned:

                            dispensers_without_assign.append(dispenser.id)

                    if dispensers_without_assign:
                        dispenser_id_chosen = random.choice(
                            dispensers_without_assign)
                        create_result.write(
                            {'dispenser_user_id': dispenser_id_chosen})

        return create_result
