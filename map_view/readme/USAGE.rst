Here is the implementation in ``hotel_map``:

hotel.room view

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

hotel.folio view with button will return action_view_hotel_floor_map

.. code-block:: XML

    <record id="view_hotel_folio_form" model="ir.ui.view">
        <field name="name">hotel.folio.view.form</field>
        <field name="model">hotel.folio</field>
        <field name="inherit_id" ref="hotel.view_hotel_folio_form" />
        <field name="arch" type="xml">
            <field name="room_line_ids" position="before">
                <button class="btn btn-primary" name="action_view_hotel_floor_map" type="action">
                    Select Room
                </button>
            </field>
        </field>
    </record>

hotel.folio method action_view_hotel_floor_map will return view "hotel_map.hotel_floor_view_map_action_folio_add_room"

.. code-block:: python

    _inherit = "hotel.folio"

    def action_view_hotel_floor_map(self):
        self.ensure_one()
        action = {
            "type": "ir.actions.act_window",
            "res_model": "hotel.floor",
            "views": [[self.env.ref("hotel_map.hotel_floor_view_map_action_folio_add_room").id, "map2"]],
            "context": {"folio_id": self.id},  # folio.room.line field
        }
        return action

View hotel_floor_view_map_action_folio_add_room

.. code-block:: XML

    <record id="hotel_floor_view_map_action_folio_add_room" model="ir.ui.view">
        <field name="name">hotel.floor.view.map</field>
        <field name="model">hotel.floor</field>
        <field name="arch" type="xml">
            <map2
                items_field="room_ids"
                create_item_values="{'room_categ_id': 'hotel_map.default_room_type'}"
                onclick_item_method="action_folio_add_room"
            />
        </field>
    </record>
