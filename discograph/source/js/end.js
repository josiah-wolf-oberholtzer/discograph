    if (typeof define === "function" && define.amd) define(dg);
    else if (typeof module === "object" && module.exports) module.exports = dg;
    this.dg = dg;
}();