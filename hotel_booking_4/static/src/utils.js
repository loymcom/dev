/** @odoo-module **/

const { onMounted, onWillUnmount } = owl;

export function useInterval(func, ms) {
    let intervalId;
    onMounted(() => {
        intervalId = setInterval(func, ms);
    });

    onWillUnmount(() => {
        clearInterval(intervalId);
    });
}

