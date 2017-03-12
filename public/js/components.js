window.forceConfig = {
    worker: true,
    barnesHutOptimize: true
};

window.info = new Vue({
    el: '#info',
    data: {
        forceOn: false,
        options: [],
        currentOption: ""
    },
    methods: {
        updateData: function (option) {
            this.currentOption = option;
            generate(option);
        },
        updateForce: function () {
            if (this.forceOn) {
                window.s.stopForceAtlas2();
            }
            else {
                window.s.startForceAtlas2(window.forceConfig);
            }
            this.forceOn = !this.forceOn;
        }
    }
})