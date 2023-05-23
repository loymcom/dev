/** @odoo-module */

import { XMLParser } from "@web/core/utils/xml";

export class BookingArchParser extends XMLParser {
    parse(arch) {
        const xmlDoc = this.parseXML(arch);
        const imageField = xmlDoc.getAttribute("image_field");
        const limit = xmlDoc.getAttribute("limit") || 80;
        const tooltipField = xmlDoc.getAttribute("tooltip_field");
        // const floorModel = xmlDoc.getAttribute("floor_model");
        // const itemModel = xmlDoc.getAttribute("item_model");
        return {
            imageField,
            limit,
            tooltipField,
            // floorModel,
            // itemModel,
        };
    }
}
