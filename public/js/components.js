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

function formatDate(dateString){
    //Chop off the beginning
    dateString = dateString.substring(dateString.lastIndexOf("_")+1, dateString.length-1);
    //Remove the .json tail
    dateString = dateString.substring(0, dateString.lastIndexOf("."));
    let divide = dateString.split("-");

    dateString = divide[1] + "/" + divide[2] + "/" + divide[0] + " at " + divide[3];

    return dateString;
}

window.info = new Vue({
    el: '#info',
    data: {
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
        search: function(nodeName){            
            let found = (_.find(window.s.graph.nodes(), { 'id': nodeName }));

            if(found == undefined){
                alert("Node not found...")
            }
            else{
                colorNeighbors(found);
            }
        
        }
    }
})

$("#timeSlider").slider();
$("#timeSlider").on("slideStop", function(slideEvt) {
    let num = slideEvt.value
    window.info.updateTime(window.info.$data.timeOptions[num])
    $("#timeSliderValLabel").text(formatDate(window.info.$data.timeOptions[num]))
});