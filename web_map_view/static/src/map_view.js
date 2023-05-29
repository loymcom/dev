/** @odoo-module */

import { registry } from "@web/core/registry";
import { MapController } from "./map_controller";
import { MapArchParser } from "./map_arch_parser";
import { MapModel } from "./map_model";
import { MapRenderer } from "./map_renderer";
import { MapScreen } from "./MapScreen/MapScreen";

export const mapView = {
    type: "map",
    display_name: "Map",
    icon: "fa fa-picture-o",
    multiRecord: true,
    Controller: MapController,
    ArchParser: MapArchParser,
    Model: MapModel,
    // Renderer: MapRenderer,
    Renderer: MapScreen,

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

registry.category("views").add("map", mapView);
