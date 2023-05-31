/** @odoo-module alias=web_view_map.EditBar **/

    import { Component } from "@odoo/owl";

    const { useState } = owl;

    export class EditBar extends Component {
        static template = 'web_view_map.EditBar';

        setup() {
            super.setup();
            this.state = useState({ isColorPicker: false })
        }
    }
