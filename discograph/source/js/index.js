!function(){
    var dg = {version: "0.1"};

import "color";
import "loading";
import "network/";
import "svg";
import "relations";
import "typeahead";
import "fsm";
import "init";

    if (typeof define === "function" && define.amd) define(dg);
    else if (typeof module === "object" && module.exports) module.exports = dg;
    this.dg = dg;
}();