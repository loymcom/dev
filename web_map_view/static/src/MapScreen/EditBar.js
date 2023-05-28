/** @odoo-module alias=web_map_view.EditBar **/

    import { Component } from "@odoo/owl";

    const { useState } = owl;

    export class EditBar extends Component {
        static template = 'web_map_view.EditBar';

        setup() {
            super.setup();
            this.state = useState({ isColorPicker: false })
        }
    }
