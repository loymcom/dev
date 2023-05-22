/** @odoo-module **/

import { Component } from "@odoo/owl";
// import FloorScreen from "pos_restaurant.FloorScreen";  // Missing dependencies:     ['pos_restaurant.FloorScreen']
// import { FloorScreen } from "@pos_restaurant/js/Screens/FloorScreen/FloorScreen";

export class Playground extends Component {
    static template = "hotel_booking_2.playground";
    // static components = { FloorScreen };

    setup() {
        this.floor = {
            id: 1,
            name: "Floor 1",
            background_color: "orange",
            pos_config_id: 1,
            sequence: 1,
            table_ids: [],
        };
        this.isShown = true;
        this.mobileSearchBarIsShown = false;
    }
}
