odoo.define('booking_view.EditBar', function(require) {
    'use strict';

    const PosComponent = require('booking_view_pos.PosComponent');
    const Registries = require('booking_view_pos.Registries');

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
