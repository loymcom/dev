/** @odoo-module **/

import { Component } from "@odoo/owl";
// import { FloorScreen } from "hotel_booking_2.FloorScreen";
import { FloorScreen } from "@hotel_booking_2/js/FloorScreen/FloorScreen";


export class Playground extends Component {
    static template = "hotel_booking_2.floor";
    static components = { FloorScreen };

    setup() {
        this.hotel_folio_id = odoo.hotel_folio_id;
        this.floor = {
            id: 1,
            name: "Floor 1",
            background_color: "orange",
            pos_config_id: 1,
            sequence: 1,
            table_ids: [],
        };
        this.FloorScreen = this.floor;
        this.isShown = true;
        this.mobileSearchBarIsShown = false;
    }
}
