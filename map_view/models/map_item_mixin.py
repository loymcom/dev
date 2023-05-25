from odoo import fields, models


class MapItemMixin(models.AbstractModel):
    _name = "map.item.mixin"
    _description = "Item in a map"

    shape = fields.Selection([('square', 'Square'), ('round', 'Round')], string='Shape', required=True, default='square')
    position_h = fields.Float('Horizontal Position', default=10,
        help="The item's horizontal position from the left side to the item's center, in pixels")
    position_v = fields.Float('Vertical Position', default=10,
        help="The item's vertical position from the top to the item's center, in pixels")
    width = fields.Float('Width', default=50, help="The item's width in pixels")
    height = fields.Float('Height', default=50, help="The item's height in pixels")
    capacity = fields.Integer('Capacity', default=1, help="The capacity, e.g. beds in a room or seats at a table.")
    color = fields.Char('Color', help="The table's color, expressed as a valid 'background' CSS property value")
    active = fields.Boolean('Active', default=True, help='If false, the item is deactivated and will not be visible in the map.')
