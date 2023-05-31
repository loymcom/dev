/** @odoo-module */

import { Component } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { MapScreen } from "./MapScreen/MapScreen";

export class MapRenderer extends Component {
    static template = "web_view_map.Renderer";
    static components = { MapScreen };

    setup() {
        this.action = useService("action");
    }

    onImageClick(resId) {
        this.action.switchView("form", { resId });
    }
}
