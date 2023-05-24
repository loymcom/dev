/** @odoo-module */

import { Component } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
// import { FloorScreen } from "./FloorScreen/FloorScreen";

export class MapRenderer extends Component {
    static template = "map_view.Renderer";
    // static components = { FloorScreen };

    setup() {
        this.action = useService("action");
    }

    onImageClick(resId) {
        this.action.switchView("form", { resId });
    }
}
