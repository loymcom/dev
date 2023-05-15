from odoo import api, fields, models
from odoo.exceptions import UserError


class HotelRoom(models.Model):
    _inherit = "hotel.room"

    position_h = fields.Float('Horizontal Position', default=10,
        help="The table's horizontal position from the left side to the table's center, in pixels")
    position_v = fields.Float('Vertical Position', default=10,
        help="The table's vertical position from the top to the table's center, in pixels")
    width = fields.Float('Width', default=50, help="The table's width in pixels")
    height = fields.Float('Height', default=50, help="The table's height in pixels")
    color = fields.Char('Color', help="The table's color, expressed as a valid 'background' CSS property value")

    # restaurant.table is similar to hotel.room
    seats = fields.Integer('Seats', default=1, help="The default number of customer served at this table.")
    shape = fields.Selection([('square', 'Square'), ('round', 'Round')], string='Shape', required=True, default='square')

    capacity = fields.Integer(default=1)
    room_categ_id = fields.Many2one(default=lambda self: self._default_room_categ_id())

    def _default_room_categ_id(self):
        return self.env.ref("hotel_booking.default_room_type").id

    @api.model
    def create_from_ui(self, table):
        """ create or modify a table from the point of sale UI.
            table contains the table's fields. If it contains an
            id, it will modify the existing table. It then
            returns the id of the table.
        """
        if table.get('floor_id'):
            table['floor_id'] = table['floor_id'][0]

        sanitized_table = dict([(key, val) for key, val in table.items() if key in self._fields and val is not None])
        table_id = sanitized_table.pop('id', False)
        if table_id:
            self.browse(table_id).write(sanitized_table)
        else:
            table_id = self.create(sanitized_table).id
        return table_id

    @api.ondelete(at_uninstall=False)
    def _unlink_except_active_pos_session(self):
        confs = self.mapped('floor_id').mapped('pos_config_id').filtered(lambda c: c.is_table_management == True)
        opened_session = self.env['pos.session'].search([('config_id', 'in', confs.ids), ('state', '!=', 'closed')])
        if opened_session:
            error_msg = _("You cannot remove a table that is used in a PoS session, close the session(s) first.")
            if confs:
                raise UserError(error_msg)