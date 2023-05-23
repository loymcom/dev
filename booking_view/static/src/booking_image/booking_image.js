/** @odoo-module */

const { Component } = owl;
import { useTooltip } from "@web/core/tooltip/tooltip_hook";

export class BookingImage extends Component {
    setup() {
        useTooltip("tooltip", {
            tooltip: this.props.image[this.props.tooltipField],
        });
    }
    onClick() {
        this.props.onClick(this.props.image.id);
    }
}

BookingImage.template = "booking_view.BookingImage";
BookingImage.props = {
    image: { type: Object },
    className: { type: String },
    imageField: { type: String },
    tooltipField: { type: String },
    onClick: { type: Function },
};
