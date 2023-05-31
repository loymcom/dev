Map view is defined with ``<map />`` and these attributes:

- ``items_field`` (mandatory): name of one2many or many2many field
- ``item_values`` (optional): dictionary with values for a new item.
- ``onclick_method`` (optional): name of a python method to trigger when the user clicks on an item.
The (1) item_id and the (2) action context will be passed to the method.
If onclick_method is blank, open the item in form view.

.. code-block:: XML
    <map
        items_field="item_ids"
        item_values="{'field': 'value'}"
        onclick_method="map_method"
    />

Use case in ``hotel_map``
-------------------------

- hotel.folio form view: Click the button "Select Room".
- hotel.floor map view: Click on a room.
- hotel.folio form view: Room Lines has the selected room.

Implementation
--------------

We start with a button "Select Room".

.. code-block:: XML

    <record id="view_hotel_folio_form" model="ir.ui.view">
        <field name="name">hotel.folio.view.form</field>
        <field name="model">hotel.folio</field>
        <field name="inherit_id" ref="hotel.view_hotel_folio_form" />
        <field name="arch" type="xml">
            <field name="room_line_ids" position="before">
                <button class="btn btn-primary" name="action_view_floor_map_select_room" type="object">
                    Select Room
                </button>
            </field>
        </field>
    </record>

The button will call the method ``action_view_floor_map_select_room``.

.. code-block:: python

    _inherit = "hotel.folio"

    def action_view_floor_map_select_room(self):
        self.ensure_one()
        action = {
            "type": "ir.actions.act_window",
            "res_model": "hotel.floor",
            "views": [[self.env.ref("hotel_map.hotel_floor_view_map_select_room").id, "map"]],
            "context": {"folio_id": self.id},
        }
        return action

The method will return the map view ``hotel_floor_view_map_select_room`` with the context.

.. code-block:: XML

    <record id="hotel_floor_view_map_select_room" model="ir.ui.view">
        <field name="name">hotel.floor.view.map</field>
        <field name="model">hotel.floor</field>
        <field name="arch" type="xml">
            <map
                items_field="room_ids"
                item_values="{'room_categ_id': %(hotel_map.default_room_type)d}"
                onclick_method="action_reserve_room_view_folio"
            />
        </field>
    </record>

Clicking a room in the map view will call the method ``action_reserve_room_view_folio``.

.. code-block:: python

    def action_reserve_room_view_folio(self, room_id, context):
        self.ensure_one()

        # Reserve the room

        return {
            "name": hotel_folio.display_name,
            "type": "ir.actions.act_window",
            "views": [[False, "form"]],
            "res_model": "hotel.folio",
            "res_id": hotel_folio.id,
        }

Rooms may be configured in the floor map view, or in the room form view.

.. code-block:: XML

    <record id="view_hotel_room_form" model="ir.ui.view">
        <field name="name">hotel.room.view.form.inherit.hotel</field>
        <field name="model">hotel.room</field>
        <field name="inherit_id" ref="hotel.view_hotel_room_form" />
        <field name="arch" type="xml">
            <notebook position="inside">
                <page name="appearance" string="Appearance">
                    <group col="4" string="Appearance">
                        <field name="shape" />
                        <field name="position_h" />
                        <field name="position_v" />
                        <field name="width" />
                        <field name="height" />
                        <field name="capacity" />
                        <field name="color" />
                        <field name="active" widget="boolean_toggle" />
                    </group>
                </page>
            </notebook>
        </field>
    </record>
