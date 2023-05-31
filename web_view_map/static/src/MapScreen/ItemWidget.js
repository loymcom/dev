/** @odoo-module alias=web_view_map.ItemWidget **/

    import { Component } from "@odoo/owl";

    /**
     * props: {
     *  onClick: callback,
     *  item: item object,
     * }
     */
    export class ItemWidget extends Component {
        static template = 'web_view_map.ItemWidget';

        setup() {
            owl.onMounted(this.onMounted);
        }
        onMounted() {
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
            // Object.assign(this.el.style, style);

            // const itemCover = this.el.querySelector('.item-cover');
            // Object.assign(itemCover.style, { height: `${Math.ceil(this.fill * 100)}%` });
        }
        get fill() {
            // const customerCount = this.env.pos.getCustomerCount(this.props.item.id);
            // return Math.min(1, Math.max(0, customerCount / this.props.item.capacity));
            return 1
        }
        get orderCount() {
            const item = this.props.item;
            return item.order_count !== undefined
                ? item.order_count
                : this.env.pos
                      .getItemOrders(item.id)
                      .filter(o => o.orderlines.length !== 0 || o.paymentlines.length !== 0).length;
        }
        get orderCountClass() {
            const countClass = { 'order-count': true }
            if (this.env.pos.config.iface_printers) {
                const notifications = this._getNotifications();
                countClass['notify-printing'] = notifications.printing;
                countClass['notify-skipped'] = notifications.skipped;
            }
            return countClass;
        }
        get customerCountDisplay() {
            return `${this.env.pos.getCustomerCount(this.props.item.id)}/${this.props.item.capacity}`;
        }
        _getNotifications() {
            const orders = this.env.pos.getItemOrders(this.props.item.id);

            let hasChangesCount = 0;
            let hasSkippedCount = 0;
            for (let i = 0; i < orders.length; i++) {
                if (orders[i].hasChangesToPrint()) {
                    hasChangesCount++;
                } else if (orders[i].hasSkippedChanges()) {
                    hasSkippedCount++;
                }
            }

            return hasChangesCount ? { printing: true } : hasSkippedCount ? { skipped: true } : {};
        }
    }
