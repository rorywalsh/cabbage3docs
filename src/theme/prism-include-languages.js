const prismIncludeLanguagesImport = require('@theme-original/prism-include-languages');
const registerCsoundPrismLanguage = require('./prism-csound-language');

module.exports = function prismIncludeLanguagesWithCsound(PrismObject) {
    const prismIncludeLanguages = prismIncludeLanguagesImport.default || prismIncludeLanguagesImport;
    prismIncludeLanguages(PrismObject);
    registerCsoundPrismLanguage(PrismObject);
};
