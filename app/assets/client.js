var dmcfuncs = window.dashMantineFunctions = window.dashMantineFunctions || {};

const formatter =new Intl.NumberFormat("en-UK", {notation: "compact"})
dmcfuncs.numberFormatter = function(value) {
    return formatter.format(value)
};

window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        fixCountrySelections: function(availableCountries, selectedCountries) {
            return selectedCountries.filter((country) => availableCountries.includes(country))
        },

        updateURLFromInputs: function(key, selectedCountries) {
            const url = new URL(window.location.href);
            const currentUrlKey = url.searchParams.get('key');
            const currentUrlCountries = url.searchParams.getAll('country');
            if (key === currentUrlKey && currentUrlCountries.toString() === selectedCountries.toString()) {
                return window.dash_clientside.no_update;
            }

            url.searchParams.delete('key');
            url.searchParams.append('key', key);

            url.searchParams.delete('country');
            selectedCountries.forEach(country => url.searchParams.append('country', country));

            window.history.pushState({}, '', url.pathname + url.search); // updates the URL but doesn't trigger dcc.Location
            return window.dash_clientside.no_update; // no update to prevent trigger loop
        },

        updateInputsFromURL: function(search) {
            // alert("search triggerd")
            const urlParams = new URLSearchParams(search);
            key = urlParams.get('key');
            countrys = urlParams.getAll('country');
            if (!key) key = window.dash_clientside.no_update;
            if (!countrys || !countrys.length) countrys = window.dash_clientside.no_update;
            return [key, countrys];
        }
    }
});