var dmcfuncs = window.dashMantineFunctions = window.dashMantineFunctions || {};

const formatter =new Intl.NumberFormat("en-US", {notation: "compact"})
dmcfuncs.numberFormatter = function(value) {
    return formatter.format(value)
};

window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
		updateGraphKey: function(key) {
			return [[{"name": key}], key]
		}
    }
});
