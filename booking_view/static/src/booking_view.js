/** @odoo-module */

import { registry } from "@web/core/registry";
import { BookingController } from "./booking_controller";
import { BookingArchParser } from "./booking_arch_parser";
import { BookingModel } from "./booking_model";
import { BookingRenderer } from "./booking_renderer";

export const bookingView = {
    type: "booking",
    display_name: "Booking",
    icon: "fa fa-picture-o",
    multiRecord: true,
    Controller: BookingController,
    ArchParser: BookingArchParser,
    Model: BookingModel,
    Renderer: BookingRenderer,

    props(genericProps, view) {
        const { ArchParser } = view;
        const { arch } = genericProps;
        const archInfo = new ArchParser().parse(arch);

        return {
            ...genericProps,
            Model: view.Model,
            Renderer: view.Renderer,
            archInfo,
        };
    },
};

registry.category("views").add("booking", bookingView);
