/** @odoo-module */

import { XMLParser } from "@web/core/utils/xml";

export class MapArchParser extends XMLParser {
    parse(arch) {
        const xmlDoc = this.parseXML(arch);
        const itemsField = xmlDoc.getAttribute("items_field");
        const itemValues = xmlDoc.getAttribute("item_values");
        return {
            itemsField,
            itemValues,
        };
    }
}