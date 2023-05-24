/** @odoo-module */
import { useService } from "@web/core/utils/hooks";
const { Component } = owl;
import { BookingImage } from "./booking_image/booking_image";
import { FloorScreen } from "./FloorScreen/FloorScreen";

export class BookingRenderer extends Component {
    setup() {
        this.action = useService("action");
    }

    onImageClick(resId) {
        this.action.switchView("form", { resId });
    }
}

// BookingRenderer.components = { BookingImage };
BookingRenderer.components = { FloorScreen, BookingImage };
BookingRenderer.template = "booking_view.Renderer";
