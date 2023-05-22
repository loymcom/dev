/** @odoo-module **/

import { Component } from "@odoo/owl";
import { FloorScreen } from "@hotel_booking_2/js/FloorScreen/FloorScreen";
import { useService } from "@web/core/utils/hooks";


export class HotelBooking extends Component {
    static template = "hotel_booking_2.hotel_booking_ui";
    static components = { FloorScreen };

    setup() {
        //
        // useService fails in hooks.js:192 const { services } = component.env; ENV IS MISSING, WHY???
        //
        // this.orm = useService("orm");
        // this.rpc = useService("rpc");
        this.hotel_folio_id = odoo.hotel_folio_id;
        this.load_server_data();
    }
    async load_server_data(){
        // const loadedData = await this.orm.call("hotel.folio", 'load_booking_data', [], {});
        // await this._processData(loadedData);
    }
    async _processData(loadedData) {
        this.floors = loadedData['hotel.floor'];
        this.loadHotelFloor();
    }
    loadHotelFloor() {
        // we do this in the front end due to the circular/recursive reference needed
        // Ignore floorplan features if no floor specified.

        // this.config.iface_floorplan = !!(this.floors && this.floors.length > 0);
        // if (this.config.iface_floorplan) {
            this.floors_by_id = {};
            this.tables_by_id = {};
            for (let floor of this.floors) {
                this.floors_by_id[floor.id] = floor;
                for (let table of floor.tables) {
                    this.tables_by_id[table.id] = table;
                    table.floor = floor;
                }
            }
        // }
    }
}
