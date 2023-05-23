/** @odoo-module */

import { registry } from "@web/core/registry";
import { LazyComponent } from "@web/core/assets";

const { Component, xml } = owl;

class AwesomeDashboardLoader extends Component {}

AwesomeDashboardLoader.components = { LazyComponent };
AwesomeDashboardLoader.template = xml`
<LazyComponent bundle="'hotel_booking.dashboard'" Component="'AwesomeDashboard'" props="props"/>
`;

registry.category("actions").add("hotel_booking.dashboard", AwesomeDashboardLoader);
