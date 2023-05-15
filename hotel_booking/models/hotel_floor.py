from odoo import api, fields, models
from odoo.exceptions import UserError


class HotelFloor(models.Model):
    _inherit = "hotel.floor"

    active = fields.Boolean(default=True)
    background_color = fields.Char('Background Color', help='The background color of the floor in a html-compatible format', default='rgb(210, 210, 210)')
    background_image = fields.Binary('Background Image')
    room_ids = fields.One2many('hotel.room', 'floor_id', string='Rooms')

    # restaurant.floor is similar to hotel.floor
    table_ids = fields.One2many('hotel.room', 'floor_id', string='Rooms')
    pos_config_id = fields.Many2one('pos.config', string='Point of Sale')

    @api.ondelete(at_uninstall=False)
    def _unlink_except_active_pos_session(self):
        confs = self.mapped('pos_config_id').filtered(lambda c: c.is_table_management == True)
        opened_session = self.env['pos.session'].search([('config_id', 'in', confs.ids), ('state', '!=', 'closed')])
        if opened_session:
            error_msg = _("You cannot remove a floor that is used in a PoS session, close the session(s) first: \n")
            for floor in self:
                for session in opened_session:
                    if floor in session.config_id.floor_ids:
                        error_msg += _("Floor: %s - PoS Config: %s \n") % (floor.name, session.config_id.name)
            if confs:
                raise UserError(error_msg)

    def write(self, vals):
        for floor in self:
            if floor.pos_config_id.has_active_session and (vals.get('pos_config_id') or vals.get('active')) :
                raise UserError(
                    'Please close and validate the following open PoS Session before modifying this floor.\n'
                    'Open session: %s' % (' '.join(floor.pos_config_id.mapped('name')),))
            if vals.get('pos_config_id') and floor.pos_config_id.id and vals.get('pos_config_id') != floor.pos_config_id.id:
                raise UserError(_('The %s is already used in another Pos Config.', floor.name))
        return super(RestaurantFloor, self).write(vals)