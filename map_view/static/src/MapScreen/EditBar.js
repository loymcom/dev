/** @odoo-module alias=booking_view.EditBar **/

    import { Component } from "@odoo/owl";

    const { useState } = owl;

    export class EditBar extends Component {
        static template = 'booking_view.EditBar';

        setup() {
            super.setup();
            this.state = useState({ isColorPicker: false })
        }
    }
