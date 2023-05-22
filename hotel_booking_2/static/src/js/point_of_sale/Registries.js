odoo.define('hotel_booking_2.Registries', function(require) {
    'use strict';

    /**
     * This definition contains all the instances of ClassRegistry.
     */

    const ComponentRegistry = require('hotel_booking_2.ComponentRegistry');
    const ClassRegistry = require('hotel_booking_2.ClassRegistry');

    class ModelRegistry extends ClassRegistry {
        add(baseClass) {
            super.add(baseClass);
            /**
             * Introduce a static method (`create`) to each base class that can be
             * conveniently use to create an instance of the extended version
             * of the class.
             */
            baseClass.create = (...args) => {
                const ExtendedClass = this.get(baseClass);
                return new ExtendedClass(...args);
            }
        }
    }

    return { Component: new ComponentRegistry(), Model: new ModelRegistry() };
});
