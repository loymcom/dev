/** @odoo-module */
import { useService } from "@web/core/utils/hooks";
const { Component } = owl;
import { BookingImage } from "./booking_image/booking_image";

export class BookingRenderer extends Component {
    setup() {
        this.action = useService("action");
    }

    onImageClick(resId) {
        this.action.switchView("form", { resId });
    }
}

BookingRenderer.components = { BookingImage };
BookingRenderer.template = "booking_view.Renderer";
