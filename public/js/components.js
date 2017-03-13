window.forceConfig = {
    worker: true,
    barnesHutOptimize: true
};

window.info = new Vue({
    el: '#info',
    data: {
        forceOn: false,
        componentMode: false,
        options: [],
        currentOption: "",
        selectedNode: null,
        selectedPath: null
    },
    methods: {
        updateData: function (option) {
            this.currentOption = option;
            generate(option);
        },
        updateComponentMode: function () {
            this.componentMode= !this.componentMode;
        },
        updateForce: function () {
            if (this.forceOn) {
                window.s.stopForceAtlas2();
            }
            else {
                window.s.startForceAtlas2(window.forceConfig);
            }
            this.forceOn = !this.forceOn;
        },
        pathToString: function(){
            let res = "";
            this.selectedPath.forEach(function(o){
                res+='->' + o.id;
            })

            res=res.slice(2);
            return res;
        }
    }
})
