var dmcfuncs = window.dashMantineFunctions = window.dashMantineFunctions || {};

dmcfuncs.sciNotaFormatter = function(value) {
    if (value >= 1e6) {
        return `${value / 1e6}m`;
    } else if (value >= 1e3) {
        return `${value / 1e3}k`;
    }
    return value
};