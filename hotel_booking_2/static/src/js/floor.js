/** @odoo-module **/

import { Component } from "@odoo/owl";
// import { FloorScreen } from "hotel_booking_2.FloorScreen";
import { FloorScreen } from "@hotel_booking_2/js/FloorScreen/FloorScreen";


export class Playground extends Component {
    static template = "hotel_booking_2.playground";
    static components = { FloorScreen };

    setup() {
        
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
