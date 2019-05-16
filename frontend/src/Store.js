export var store = {
    state: {
        selectedCounter: "",
        selectedIsotope: ""
    },
    setSelectedCounter(counter) {
        this.state.selectedCounter = counter;
    },
    getSelectedCounter() {
        return this.state.selectedCounter
    },

    setSelectedIsotope(isotope) {
        this.state.selectedIsotope = isotope
    },

    getSelectedIsotope() {
        return this.state.selectedIsotope
    }
};
