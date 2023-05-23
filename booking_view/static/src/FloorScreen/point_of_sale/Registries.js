odoo.define('booking_view_pos.Registries', function(require) {
    'use strict';

    /**
     * This definition contains all the instances of ClassRegistry.
     */

    const ComponentRegistry = require('booking_view_pos.ComponentRegistry');
    const ClassRegistry = require('booking_view_pos.ClassRegistry');

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
