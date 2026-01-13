var dmcfuncs = window.dashMantineFunctions = window.dashMantineFunctions || {};

dmcfuncs.sciNotaFormatter = function(value) {
    if (value >= 1e9) {
        return `${(value / 1e9).toPrecision(3)}b`;
    } else if (value >= 1e6) {
        return `${(value / 1e6).toPrecision(3)}m`;
    } else if (value >= 1e3) {
        return `${(value / 1e3).toPrecision(3)}k`;
    }
    return value
};