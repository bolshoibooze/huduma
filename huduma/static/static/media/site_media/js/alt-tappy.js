// create an object named "app" which we can define methods on
var app = {
    // returns an array of each url to prefetch
    prefetchLinks: function(){
        // returns an array of each a.prefetch link's href
        var hrefs = $("a.prefetch").map(function(index, domElement){
            return $(this).attr("href");
        });
        // returns the array of hrefs without duplicates
        return $.unique(hrefs);
    },

    // adds a link tag to the document head for each of prefetchLinks()
    addPrefetchTags: function(){
        // for each prefetchLinks() ...
        this.prefetchLinks().each(function(index,Element){
            // create a link element...
            $("<link />", {
                // with rel=prefetch and href=Element...
                rel: "prefetch", href: Element
                // and append it to the end of the document head
            }).appendTo("head");            
        });
    },
}
