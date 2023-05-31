/** @odoo-module */

import { KeepLast } from "@web/core/utils/concurrency";

export class MapModel {
    constructor(orm, resModel, fields, archInfo, domain) {
        this.orm = orm;
        this.resModel = resModel;
        this.fields = fields;
        const { itemsField } = archInfo;
        this.itemsField = itemsField;
        // this.itemValues = itemValues;
        this.domain = domain;
        this.keepLast = new KeepLast();
        if (!(itemsField in this.fields)) {
            throw `items_field error: ${itemsField} is not a field of ${resModel}`;
        }
    }

    async load() {
        await this.loadMaps();
        await this.loadItems();
        await this.getById();
    }

    async loadMaps() {
        const { length, records } = await this.keepLast.add(
            this.orm.webSearchRead(
                this.resModel,
                this.domain,
                ["name", this.itemsField],
                {},
            )
        );
        // this.maps = [...records];  // Both cases: this=proxy, Target=MapModel, maps=Array
        // In MapScreen setup(), this=MapScreen, props.maps=Proxy Target=Array
        this.maps = records;  
        this.mapsLength = length;
    }

    async loadItems() {

        // 1. Get the model name of the items
        var { length, records } = await this.keepLast.add(
            this.orm.webSearchRead(
                "ir.model.fields",
                [["name", "=", `${this.itemsField}`], ["model", "=", `${this.resModel}`]],
                ["relation"],
                {},
            )
        );
        if (length != 1) {
            throw `loadItems error: ${this.resModel} ${this.itemsField} has ${length} relations, should have 1.`;
        }
        var itemsModelName = records[0]["relation"];

        // 2. Get the items
        var { length, records } = await this.keepLast.add(
            this.orm.webSearchRead(
                itemsModelName,
                [],
                ["id", "name", "shape", "position_h", "position_v", "width", "height", "capacity", "color", "active"],
                {},
            )
        );
        this.itemsLength = length;
        this.items = [...records];
    }

    async getById() {
        this.maps_by_id = {};
        this.items_by_id = {};
        for (let item of [...this.items]) {
            this.items_by_id[item.id] = item;
        }
        for (let map of [...this.maps]) {
            this.maps_by_id[map.id] = map;
            map.items = []
            for (let itemId of map[this.itemsField]) {
                // item -> map, map -> items
                this.items_by_id[itemId].map = map;
                map.items.push(this.items_by_id[itemId]);
            }
        }
    }
}
