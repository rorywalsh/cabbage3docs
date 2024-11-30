import type { SidebarsConfig } from '@docusaurus/plugin-content-docs';

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  // By default, Docusaurus generates a sidebar from the docs folder structure
  // tutorialSidebar: [{type: 'autogenerated', dirName: '.'}],

  // But you can create a sidebar manually

  docSidebar: [
    'intro',
    {
      type: 'doc',
      label: "Download and Install",
      id: 'download',
    },
    'cabbage3',
    {
      type: 'doc',
      label: "Using Cabbage 3",
      id: 'usingCabbage3',
    },
    {
      type: 'category',
      label: 'Widgets',
      items: ['cabbage_widgets/intro',
        'cabbage_widgets/button',
        'cabbage_widgets/combobox',
        'cabbage_widgets/gentable',
        'cabbage_widgets/groupbox',
        'cabbage_widgets/image',
        'cabbage_widgets/keyboard',
        'cabbage_widgets/label',
        'cabbage_widgets/optionButton',
        'cabbage_widgets/horizontalSlider',
        'cabbage_widgets/verticalSlider',
        'cabbage_widgets/rotarySlider'],
    },
    {
      type: 'doc',
      label: "Custom User Interfaces",
      id: 'customUIs',
    },
    {
      type: 'category',
      label: 'Opcodes',
      items: ['cabbage_opcodes/intro',
        'cabbage_opcodes/cabbageDump',
        'cabbage_opcodes/cabbageGetValue',
        'cabbage_opcodes/cabbageGet',
        'cabbage_opcodes/cabbageSet'],
    },
  ],

};

export default sidebars;
