/** @odoo-module alias=web_view_map.EditableItem **/

    const { useListener } = require("@web/core/utils/hooks");
    import { Component } from "@odoo/owl";

    const { onMounted, onPatched } = owl;

    export class EditableItem extends Component {
        static template = 'web_view_map.EditableItem';

        setup() {
            super.setup();
            useListener('resize-end', this._onResizeEnd);
            useListener('drag-end', this._onDragEnd);
            onPatched(this._setElementStyle.bind(this));
            onMounted(this._setElementStyle.bind(this));
        }
        _setElementStyle() {
            const item = this.props.item;
            function unit(val) {
                return `${val}px`;
            }
            const style = {
                width: unit(item.width),
                height: unit(item.height),
                'line-height': unit(item.height),
                top: unit(item.position_v),
                left: unit(item.position_h),
                'border-radius': item.shape === 'round' ? unit(1000) : '3px',
            };
            if (item.color) {
                style.background = item.color;
            }
            if (item.height >= 150 && item.width >= 150) {
                style['font-size'] = '32px';
            }
            Object.assign(this.el.style, style);
        }
        _onResizeEnd(event) {
            const { size, loc } = event.detail;
            const item = this.props.item;
            item.width = size.width;
            item.height = size.height;
            item.position_v = loc.top;
            item.position_h = loc.left;
            this.props.onSaveItem(this.props.item);
        }
        _onDragEnd(event) {
            const { loc } = event.detail;
            const item = this.props.item;
            item.position_v = loc.top;
            item.position_h = loc.left;
            this.props.onSaveItem(this.props.item);
        }
    }
