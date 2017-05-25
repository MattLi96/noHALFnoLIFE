window.info = new Vue({
    el: '#info',
    data: {
        currentTab: 0, 
        forceOn: false,
        componentMode: false,
        options: [],
        fullOptions: {},
        currentOption: "",
        currentTime: "",
        timeOptions: [],
        showAllLabels: false,
        selectedNode: null,
        selectedPath: null,
        basicInfo: {},
        links: {},
        searchTerm: ""
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

           $("#timeSlider").slider('setAttribute', 'max', this.timeOptions.length-1);
           $("#timeSlider").slider('setValue', 0);
           $("#timeSliderValLabel").text(formatDate(window.info.$data.timeOptions[0]))

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
        },
        search: searchNode,
        runNodeRemoval: function(){
            let sorted = window.s.graph.nodes().sort(function(x,y){
                return y.degree - x.degree;
            });

            sorted = sorted.map(function(x){ return x.id });

            let timeout = 15;
            let stopAfter = 15;

            let checkpt = sorted.length - stopAfter;

            function findStage(list){
                if(list.length === checkpt){
                    console.log("done")
                    return;
                }
                searchNode(list[0])
                setTimeout(function(){
                    console.log("nxet")
                    removeStage(list);
                }, timeout)
            }

            function removeStage(list){
                let remaining = list;
                let first = remaining.shift();

                //Get rid of first
                window.s.graph.dropNode(first);
                resetColors();

                setTimeout(function(){
                    console.log("nxet")
                    findStage(remaining);
                }, timeout)
            }

            findStage(sorted);
        }
    }
});