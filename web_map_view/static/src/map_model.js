/** @odoo-module */

import { KeepLast } from "@web/core/utils/concurrency";

export class MapModel {
    constructor(orm, resModel, fields, archInfo, domain) {
        this.orm = orm;
        this.resModel = resModel;
        this.fields = fields;
        const { itemsField } = archInfo;
        this.itemsField = itemsField;
        this.domain = domain;
        this.keepLast = new KeepLast();
        if (!(itemsField in this.fields)) {
            throw `items_field error: ${itemsField} is not a field of ${resModel}`;
        }
    }

    async load() {
        const { length, records } = await this.keepLast.add(
            this.orm.webSearchRead(
                this.resModel,
                this.domain,
                ["name", this.itemsField],
                {},
            )
        );
        this.recordsLength = length;

        this.maps = records;
    }
}
