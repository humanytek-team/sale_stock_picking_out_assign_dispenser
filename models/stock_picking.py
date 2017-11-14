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

        new_picking = super(StockPicking, self).create(vals)

        if new_picking.picking_type_code == 'outgoing':

            if new_picking.origin:

                SaleOrder = self.env['sale.order']
                generated_from_sale_order = SaleOrder.search([
                    ('name', '=', vals.get('origin'))])

                if generated_from_sale_order:

                    StockDispenser = self.env['stock.dispenser']
                    dispensers = StockDispenser.search([])
                    dispensers_activated_and_free = dispensers.filtered(
                        lambda dispenser: dispenser.active_and_free
                    )

                    if dispensers_activated_and_free:

                        dispenser_chosen = random.choice(
                            dispensers_activated_and_free)
                        new_picking.write(
                            {'dispenser_user_id': dispenser_chosen.id})
                        dispenser_chosen.active_and_free = False

                    else:

                        dispensers_without_assign = list()

                        for dispenser in dispensers:

                            dispenser_assigned = \
                                dispenser.stock_picking_ids.filtered(
                                    lambda p: p.picking_type_code ==
                                    'outgoing' and
                                    (p.state == 'partially_available' or
                                    p.state == 'assigned')
                                    )

                            if not dispenser.stock_picking_ids or \
                                    not dispenser_assigned:

                                dispensers_without_assign.append(dispenser.id)

                        if dispensers_without_assign:

                            dispenser_id_chosen = random.choice(
                                dispensers_without_assign)
                            new_picking.write(
                                {'dispenser_user_id': dispenser_id_chosen})

        return new_picking
