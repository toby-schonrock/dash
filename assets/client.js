var dmcfuncs = window.dashMantineFunctions = window.dashMantineFunctions || {};

const formatter =new Intl.NumberFormat("en-UK", {notation: "compact"})
dmcfuncs.numberFormatter = function(value) {
    return formatter.format(value)
};

window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        fixCountrySelections: function(availableCountries, selectedCountries) {
            return selectedCountries.filter((country) => availableCountries.includes(country))
        }
    }
});