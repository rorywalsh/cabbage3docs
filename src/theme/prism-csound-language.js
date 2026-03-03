const opcodeNames = require('./csound-opcodes.generated.json');

const escapeRegex = (text) => text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

const makeWordRegex = (words) => {
    const escaped = words
        .filter(Boolean)
        .map((word) => String(word).trim())
        .filter(Boolean)
        .map(escapeRegex)
        .sort((a, b) => b.length - a.length);

    return new RegExp(`\\b(?:${escaped.join('|')})\\b`);
};

module.exports = function registerCsoundPrismLanguage(Prism) {
    if (Prism.languages.csound) {
        Prism.languages.csd = Prism.languages.csound;
        Prism.languages.orc = Prism.languages.csound;
        Prism.languages.sco = Prism.languages.csound;
        return;
    }

    const keywords = [
        'instr',
        'endin',
        'opcode',
        'endop',
        'if',
        'then',
        'elseif',
        'else',
        'endif',
        'until',
        'while',
        'do',
        'od',
        'goto',
        'igoto',
        'kgoto',
        'turnoff',
        'turnoff2',
        'return',
        'xin',
        'xout',
        'reinit',
        'rireturn',
        'event',
        'event_i',
        'schedule',
        'schedulek',
        'chnget',
        'chnset',
        'prints',
        'printks',
        'printf',
        'scoreline',
        'scoreline_i',
    ];

    const constants = [
        'sr',
        'kr',
        'ksmps',
        'nchnls',
        'nchnls_i',
        '0dbfs',
        'A4',
        'massign',
        'pgmassign',
    ];

    const cabbageWidgets = [
        'button',
        'checkbox',
        'combobox',
        'encoder',
        'hrange',
        'hslider',
        'numberbox',
        'rslider',
        'vrange',
        'vslider',
        'xypad',
        'csoundoutput',
        'filebutton',
        'form',
        'gentable',
        'groupbox',
        'image',
        'infobutton',
        'keyboard',
        'label',
        'line',
        'loadbutton',
        'soundfiler',
        'source',
        'stepper',
        'textbox',
        'texteditor',
        'table',
        'transport',
    ];

    const opcodeRegex = makeWordRegex(opcodeNames);

    Prism.languages.csound = {
        comment: [
            {
                pattern: /\/\*[\s\S]*?\*\//,
                greedy: true,
            },
            {
                pattern: /(^|[^\\]);.*/m,
                lookbehind: true,
                greedy: true,
            },
            {
                pattern: /(^|[^\\])\/\/.*/m,
                lookbehind: true,
                greedy: true,
            },
        ],
        preprocessor: {
            pattern: /^\s*#[A-Za-z_]+.*$/m,
            alias: 'property',
        },
        macro: {
            pattern: /\$[A-Za-z_][A-Za-z0-9_]*/,
            alias: 'variable',
        },
        tag: {
            pattern: /<\/?[A-Za-z][A-Za-z0-9]*>/,
            alias: 'keyword',
        },
        string: {
            pattern: /"(?:\\.|[^"\\])*"/,
            greedy: true,
        },
        number: /\b(?:\d+[Ee][+-]?\d+|\d+\.\d*|\d*\.\d+|\d+)\b/,
        widget: {
            pattern: makeWordRegex(cabbageWidgets),
            alias: 'class-name',
        },
        opcode: {
            pattern: opcodeRegex,
            alias: 'function',
        },
        keyword: makeWordRegex(keywords),
        constant: makeWordRegex(constants),
        variable: {
            pattern: /\b(?:[gikafSwV]|[A-Z])[A-Za-z_][A-Za-z0-9_]*(?:\[\])?\b/,
            alias: 'variable',
        },
        operator: /[-+*/%=!<>|&^]=?|\?|:/,
        punctuation: /[{}[\];(),.]/,
    };

    Prism.languages.csd = Prism.languages.csound;
    Prism.languages.orc = Prism.languages.csound;
    Prism.languages.sco = Prism.languages.csound;
};
