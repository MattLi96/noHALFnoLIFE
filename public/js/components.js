/**
 * The Main Vue Component
 * Manages all of the functionality in the side panel
 */
window.info = new Vue({
    el: '#info',
    data: {
        currentTab: 0,                  // Which tab is active
        forceOn: false,                 // Turn on forces for the network graph
        componentMode: false,           // Only display connected component?
        options: [],                    // What other wiki options are there
        fullOptions: {},                // What are all of the options
        currentOption: "",              // Currently selected wiki
        currentTime: "",                // Currently selected time
        timeOptions: [],                // All possible times
        showAllLabels: false,           // Display node name labels
        selectedNode: null,             // Is there a node selected
        selectedPath: null,             // Is there a selected path
        basicInfo: {},                  // Basic information to display
        links: {},                      // Links - if loaded
        searchTerm: ""                  // What is being searched
    },
    methods: {
        /**
         * Changes the graph to display the new wiki selected
         * @param {string} option - The name of wiki to be displayed
         */
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
           $("#timeSlider").slider('setValue', this.timeOptions.length-1);
           $("#timeSliderValLabel").text(formatDate(window.info.$data.timeOptions[this.timeOptions.length-1]));

           generate(option);
        },

        /**
         * Changes the graph to display the current wiki at the selected time
         * @param {string} newTime - The time to be displayed
         */
        updateTime: function(newTime){
            this.currentTime = newTime;
            generate(newTime);
        },

        /**
         * Toggles the component mode setting
         */
        updateComponentMode: function () {
            this.componentMode = !this.componentMode;
        },

        /**
         * Toggles the show labels setting
         */
        updateShowAllLabels: function () {
            this.showAllLabels= !this.showAllLabels;
        },
        
        /**
         * Toggles the force on the graph
         */
        updateForce: function () {
            if (this.forceOn) {
                window.s.stopForceAtlas2();
            }
            else {
                window.s.startForceAtlas2(window.forceConfig);
            }
            this.forceOn = !this.forceOn;
        },

        /** 
         * Converts the curent selected path into a displayable string
         */
        pathToString: function () {
            let res = "";
            this.selectedPath.forEach(function (o) {
                res += '->' + o.id;
            })

            res = res.slice(2);
            return res;
        },

        /**
         * FOR USE ONLY WITH THE FULL NODE APP
         * Can call for a full recompile
         */
        recompile: function () {
            $.ajax("/data", {
                success: function (data) {
                    console.log(data);
                    reloadOptions();
                }
            });
        },

        /** Search for the given node */
        search: searchNode,

        /** 
         * Animate the Node Removal procedure:
         * Remove nodes one by one (ordered by largest degree)
         */
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