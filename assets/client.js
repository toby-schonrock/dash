var dmcfuncs = window.dashMantineFunctions = window.dashMantineFunctions || {};

const formatter =new Intl.NumberFormat("en-UK", {notation: "compact"})
dmcfuncs.numberFormatter = function(value) {
    return formatter.format(value)
};