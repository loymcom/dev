import { registry } from '@odoo/owl';
import { makeEnv } from "@odoo/owl/dist/owl.env";
import BookingApp from "./components/booking_app.js";

registry.category("main_components").add("BookingApp", {
    Component: BookingApp,
    props: {},
    env: makeEnv(),
});
