/** @odoo-module alias=booking_view.MapScreen **/

    const { debounce } = require("@web/core/utils/timing");
    import { Component } from "@odoo/owl";
    import { ItemWidget } from "./ItemWidget";
    import { EditableItem } from "./EditableItem";
    import { EditBar } from "./EditBar";

    const { onPatched, onMounted, onWillUnmount, useRef, useState } = owl;

    export class MapScreen extends Component {
        static template = 'booking_view.MapScreen';
        static components = { ItemWidget, EditableItem, EditBar };
        /**
         * @param {Object} props
         * @param {Object} props.map
         */
        setup() {
            super.setup();
            const map = this.props.map ? this.props.map : this.props.maps[0];
            this.state = useState({
                selectedMapId: map.id,
                selectedItemId: null,
                isEditMode: false,
                mapBackground: map.background_color,
                mapMapScrollTop: 0,
            });
            this.mapMapRef = useRef('map-ref');
            onPatched(this.onPatched);
            onMounted(this.onMounted);
            onWillUnmount(this.onWillUnmount);
        }
        onPatched() {
            this.mapMapRef.el.style.background = this.state.mapBackground;
            this.state.mapMapScrollTop = this.mapMapRef.el.getBoundingClientRect().top;
        }
        onMounted() {
            // if (this.env.pos.item) {
            //     this.env.pos.unsetItem();
            // }
            // this.env.posbus.trigger('start-cash-control');
            // this.mapMapRef.el.style.background = this.state.mapBackground;
            // this.state.mapMapScrollTop = this.mapMapRef.el.getBoundingClientRect().top;
            // // call _itemLongpolling once then set interval of 5sec.
            // this._itemLongpolling();
            // this.itemLongpolling = setInterval(this._itemLongpolling.bind(this), 5000);
        }
        onWillUnmount() {
            clearInterval(this.itemLongpolling);
        }
        _computePinchHypo(ev, callbackFunction) {
            const touches = ev.touches;
            // If two pointers are down, check for pinch gestures
            if (touches.length === 2) {
                const deltaX = touches[0].pageX - touches[1].pageX;
                const deltaY = touches[0].pageY - touches[1].pageY;
                callbackFunction(Math.hypot(deltaX, deltaY))
            }
        }
        _onPinchStart(ev) {
            ev.currentTarget.style.setProperty('touch-action', 'none');
            this._computePinchHypo(ev, this.startPinch.bind(this));
        }
        _onPinchEnd(ev) {
            ev.currentTarget.style.removeProperty('touch-action');
        }
        _onPinchMove(ev) {
            debounce(this._computePinchHypo, 10, true)(ev, this.movePinch.bind(this));
        }
        _onDeselectItem() {
            this.state.selectedItemId = null;
        }
        async _createItemHelper(copyItem) {
            let newItem;
            if (copyItem) {
                newItem = Object.assign({}, copyItem);
                newItem.position_h += 10;
                newItem.position_v += 10;
            } else {
                newItem = {
                    position_v: 100,
                    position_h: 100,
                    width: 75,
                    height: 75,
                    shape: 'square',
                    capacity: 1,
                };
            }
            newItem.name = this._getNewItemName(newItem.name);
            delete newItem.id;
            newItem.map_id = [this.activeMap.id, ''];
            newItem.map = this.activeMap;
            try {
                await this._save(newItem);
                this.activeItems.push(newItem);
                return newItem;
            } catch (error) {
                throw error;
            }
        }
        _getNewItemName(name) {
            if (name) {
                const num = Number((name.match(/\d+/g) || [])[0] || 0);
                const str = name.replace(/\d+/g, '');
                const n = { num: num, str: str };
                n.num += 1;
                this._lastName = n;
            } else if (this._lastName) {
                this._lastName.num += 1;
            } else {
                this._lastName = { num: 1, str: 'T' };
            }
            return '' + this._lastName.str + this._lastName.num;
        }
        async _save(item) {
            const itemCopy = { ...item };
            delete itemCopy.map;
            const itemId = await this.rpc({
                model: 'hotel.map',
                method: 'create_from_ui',
                args: [itemCopy],
            });
            item.id = itemId;
            this.props.items_by_id[itemId] = item;
        }
        async _itemLongpolling() {
            if (this.state.isEditMode) {
                return;
            }
            try {
                // const result = await this.rpc({
                //     model: 'hotel.folio',
                //     method: 'get_items_order_count',
                //     args: [this.env.pos.config.id],
                // });
                // result.forEach((item) => {
                //     const item_obj = this.env.pos.items_by_id[item.id];
                //     const unsynced_orders = this.env.pos
                //         .getItemOrders(item_obj.id)
                //         .filter(
                //             (o) =>
                //                 o.server_id === undefined &&
                //                 (o.orderlines.length !== 0 || o.paymentlines.length !== 0) &&
                //                 // do not count the orders that are already finalized
                //                 !o.finalized
                //         ).length;
                //     item_obj.order_count = item.orders + unsynced_orders;
                // });
            } catch (error) {
                throw error;
            }
        }
        get activeMap() {
            return this.props.maps_by_id[this.state.selectedMapId];
        }
        get activeItems() {
            return this.activeMap.items;
        }
        get isMapEmpty() {
            return this.activeItems.length === 0;
        }
        get selectedItem() {
            return this.state.selectedItemId !== null
                ? this.props.items_by_id[this.state.selectedItemId]
                : false;
        }
        movePinch(hypot) {
            const delta = hypot / this.scalehypot ;
            const value = this.initalScale * delta;
            this.setScale(value);
        }
        startPinch(hypot) {
            this.scalehypot = hypot;
            this.initalScale = this.getScale();
        }
        getMapNode() {
            return this.el.querySelector('.map > .items, .map > .empty-map');
        }
        getScale() {
            const scale = this.getMapNode().style.getPropertyValue('--scale');
            const parsedScaleValue = parseFloat(scale);
            return isNaN(parsedScaleValue) ? 1 : parsedScaleValue;
        }
        setScale(value) {
            // a scale can't be a negative number
            if (value > 0) {
                this.getMapNode().style.setProperty('--scale', value);
            }
        }
        selectMap(map) {
            this.state.selectedMapId = map.id;
            this.state.mapBackground = this.activeMap.background_color;
            this.state.isEditMode = false;
            this.state.selectedItemId = null;
        }
        toggleEditMode() {
            this.state.isEditMode = !this.state.isEditMode;
            this.state.selectedItemId = null;
        }
        async onSelectItem(item) {
            if (this.state.isEditMode) {
                this.state.selectedItemId = item.id;
            } else {
                try {
                    if (this.env.pos.orderToTransfer) {
                        await this.env.pos.transferItem(item);
                    } else {
                        await this.env.pos.setItem(item);
                    }
                } catch (error) {
                    throw error;
                }
                const order = this.env.pos.get_order();
                this.showScreen(order.get_screen_data().name);
            }
        }
        async onSaveItem(item) {
            await this._save(item);
        }
        async createItem() {
            const newItem = await this._createItemHelper();
            if (newItem) {
                this.state.selectedItemId = newItem.id;
            }
        }
        async duplicateItem() {
            if (!this.selectedItem) return;
            const newItem = await this._createItemHelper(this.selectedItem);
            if (newItem) {
                this.state.selectedItemId = newItem.id;
            }
        }
        async renameItem() {
            const selectedItem = this.selectedItem;
            if (!selectedItem) return;
            const { confirmed, payload: newName } = await this.showPopup('TextInputPopup', {
                startingValue: selectedItem.name,
                title: this.env._t('Item Name ?'),
            });
            if (!confirmed) return;
            if (newName !== selectedItem.name) {
                selectedItem.name = newName;
                await this._save(selectedItem);
            }
        }
        async changeCapacityNum() {
            const selectedItem = this.selectedItem
            if (!selectedItem) return;
            const { confirmed, payload: inputNumber } = await this.showPopup('NumberPopup', {
                startingValue: selectedItem.capacity,
                cheap: true,
                title: this.env._t('Number of Capacity ?'),
                isInputSelected: true,
            });
            if (!confirmed) return;
            const newCapacityNum = parseInt(inputNumber, 10) || selectedItem.capacity;
            if (newCapacityNum !== selectedItem.capacity) {
                selectedItem.capacity = newCapacityNum;
                await this._save(selectedItem);
            }
        }
        async changeShape() {
            if (!this.selectedItem) return;
            this.selectedItem.shape = this.selectedItem.shape === 'square' ? 'round' : 'square';
            this.render();
            await this._save(this.selectedItem);
        }
        async setItemColor(color) {
            this.selectedItem.color = color;
            this.render();
            await this._save(this.selectedItem);
        }
        async setMapColor(color) {
            this.state.mapBackground = color;
            this.activeMap.background_color = color;
            try {
                await this.rpc({
                    model: 'hotel.map',
                    method: 'write',
                    args: [[this.activeMap.id], { background_color: color }],
                });
            } catch (error) {
                throw error;
            }
        }
        async deleteItem() {
            if (!this.selectedItem) return;
            const { confirmed } = await this.showPopup('ConfirmPopup', {
                title: this.env._t('Are you sure ?'),
                body: this.env._t('Removing a item cannot be undone'),
            });
            if (!confirmed) return;
            try {
                const originalSelectedItemId = this.state.selectedItemId;
                await this.rpc({
                    model: 'hotel.room',
                    method: 'create_from_ui',
                    args: [{ active: false, id: originalSelectedItemId }],
                });
                this.activeMap.items = this.activeItems.filter(
                    (item) => item.id !== originalSelectedItemId
                );
                // Value of an object can change inside async function call.
                //   Which means that in this code block, the value of `state.selectedItemId`
                //   before the await call can be different after the finishing the await call.
                // Since we wanted to disable the selected item after deletion, we should be
                //   setting the selectedItemId to null. However, we only do this if nothing
                //   else is selected during the rpc call.
                if (this.state.selectedItemId === originalSelectedItemId) {
                    this.state.selectedItemId = null;
                }
                delete this.env.pos.items_by_id[originalSelectedItemId];
                this.env.pos.TICKET_SCREEN_STATE.syncedOrders.cache = {};
            } catch (error) {
                throw error;
            }
        }
    }
