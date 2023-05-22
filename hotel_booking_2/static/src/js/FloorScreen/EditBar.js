odoo.define('hotel_booking_2.EditBar', function(require) {
    'use strict';

    const PosComponent = require('hotel_booking_2.PosComponent');
    const Registries = require('hotel_booking_2.Registries');

    const { useState } = owl;

    class EditBar extends PosComponent {
        setup() {
            super.setup();
            this.state = useState({ isColorPicker: false })
        }
    }
    EditBar.template = 'EditBar';

    Registries.Component.add(EditBar);

    return EditBar;
});
