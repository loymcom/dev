/** @odoo-module */
import { useService } from "@web/core/utils/hooks";
// const { Component } = owl;
import { Component } from "@odoo/owl";
import { BookingImage } from "./booking_image/booking_image";
import { FloorScreen } from "./FloorScreen/FloorScreen";

export class BookingRenderer extends Component {
    static template = "booking_view.Renderer";
    static components = { FloorScreen, BookingImage };

    setup() {
        this.action = useService("action");
    }

    onImageClick(resId) {
        this.action.switchView("form", { resId });
    }
}
