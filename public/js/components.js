window.forceConfig = {
    worker: true,
    barnesHutOptimize: true
};

// window.handleChanges = function (newHash, oldHash) {
//     window.info.$data.currentOption = newHash;
//     generate(newHash);
// };

// $( document ).ready(function () {
//     hasher.init();
//     hasher.changed.add(window.handleChanges);
//     hasher.initialized.add(window.handleChanges);
// });

window.info = new Vue({
    el: '#info',
    data: {
        forceOn: false,
        componentMode: false,
        options: [],
        fullOptions: {},
        currentOption: "",
        currentTime: "",
        timeOptions: "",
        showAllLabels: false,
        selectedNode: null,
        selectedPath: null,
        basicInfo: {},
        links: {}
    },
    methods: {
        updateData: function (option) {
           this.currentOption = option;
           this.currentTime = "";

           let timeOpts = this.fullOptions["public/" + option];
           this.timeOptions = timeOpts.map(function(el){
                let splitVersion = el.split("/");
                splitVersion.shift();
                return splitVersion.join("/");
            });
           
           generate(option);
        },
        updateTime: function(newTime){
            this.currentTime = newTime;
            generate(newTime);
        },
        updateComponentMode: function () {
            this.componentMode = !this.componentMode;
        },
        updateShowAllLabels: function () {
            this.showAllLabels= !this.showAllLabels;
            generate(hasher.getHash());
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
        pathToString: function () {
            let res = "";
            this.selectedPath.forEach(function (o) {
                res += '->' + o.id;
            })

            res = res.slice(2);
            return res;
        },
        recompile: function () {
            $.ajax("/data", {
                success: function (data) {
                    console.log(data);
                    reloadOptions();
                }
            });
        }
    }
})
